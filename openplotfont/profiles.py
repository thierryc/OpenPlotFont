"""Draft 0.4 pen profiles, explicit centerline fallback and bound appearance.

Authoring controls are never interpreted as force, depth, or recovered timing.
The native dialect retains progression without pretending it is linear easing.
"""
import copy
import hashlib
import json
import math

CHANNELS = ('width', 'height', 'angle', 'strokePosition', 'progressionIn', 'progressionOut')
MODELS = ('linear-ellipse-v1', 'glyphs4-v1')


def appearance_binding(operation):
    """Bind the preview to geometry and every operative profile field."""
    profile = {k: v for k, v in operation['penProfile'].items() if k != 'appearance'}
    data = {'closed': operation['closed'], 'commands': operation['commands'], 'penProfile': profile}
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                                    allow_nan=False).encode('utf-8')).hexdigest()


def segment_count(operation):
    commands = operation['commands']
    return len(commands)-1 + int(operation['closed'] and commands[-1][-2:] != commands[0][-2:])


def validate_profile(operation, version, at):
    # Import lazily to keep the validator's shared primitives in one module.
    from .validation import require, object_at, array_at, number, path_record
    require(version == '0.4', at, 'penProfile requires version 0.4')
    require(operation.get('kind', 'stroke') == 'stroke', at, 'penProfile is unsupported on fills')
    p = object_at(operation['penProfile'], at)
    require(set(p) <= {'version','model','defaults','points','style','appearance'}, at, 'unknown profile field')
    require(p.get('version') == '1', at+'.version', 'unsupported pen profile version')
    require(p.get('model') in MODELS, at+'.model', 'unsupported pen profile model')
    defaults = object_at(p.get('defaults'), at+'.defaults')
    require(set(defaults) == set(CHANNELS), at+'.defaults', 'all six resolved channel defaults are required')

    def channels(values, where, optional):
        require(set(values) <= set(CHANNELS), where, 'unknown pen channel')
        for key, value in values.items():
            require((optional and value is None) or number(value), where+'.'+key, 'expected finite channel or inherited null')
            if value is None:
                continue
            if key in ('width','height'):
                require(value > 0, where+'.'+key, 'footprint diameter must be positive')
            if key == 'strokePosition':
                require(-1 <= value <= 1, where+'.'+key, 'placement must be between -1 and 1')
    channels(defaults, at+'.defaults', False)
    points = array_at(p.get('points'), at+'.points')
    require(len(points) <= 100000, at, 'too many pen points')
    previous = (-1, -1)
    for i, point in enumerate(points):
        where = f'{at}.points[{i}]'
        object_at(point, where)
        require(set(point) == {'segment','t','values'}, where, 'expected segment, t and values')
        segment, t = point['segment'], point['t']
        require(type(segment) is int and 0 <= segment < segment_count(operation), where+'.segment', 'invalid segment reference')
        require(number(t) and 0 <= t <= 1, where+'.t', 'expected Bezier parameter between 0 and 1')
        require((segment,t) > previous, where, 'pen points must be unique and in trajectory order')
        previous = (segment,t)
        channels(object_at(point['values'], where+'.values'), where+'.values', True)
    style = object_at(p.get('style'), at+'.style')
    require(set(style) == {'capStart','capEnd','join'}, at+'.style', 'expected capStart, capEnd and join')
    require(all(style[k] in ('round','butt','square') for k in ('capStart','capEnd')), at+'.style', 'unsupported cap')
    require(style['join'] in ('round','bevel','miter'), at+'.style', 'unsupported join')
    if p['model'] == 'linear-ellipse-v1':
        require(defaults['progressionIn'] == defaults['progressionOut'] == 0 and
                all(all(q['values'].get(k) in (None,0) for k in ('progressionIn','progressionOut')) for q in points),
                at, 'linear-ellipse-v1 requires zero progression; use glyphs4-v1 for native controls')
    if p['model'] == 'glyphs4-v1':
        require('appearance' in p, at, 'glyphs4-v1 requires a bound native appearance reference')
    if 'appearance' in p:
        a = object_at(p['appearance'], at+'.appearance')
        require(set(a) == {'source','bindingSha256','fillRule','contours'}, at+'.appearance', 'invalid appearance fields')
        require(isinstance(a['source'],str) and 0 < len(a['source']) <= 200, at+'.appearance.source', 'expected source renderer identity')
        require(a['fillRule'] == 'nonzero', at+'.appearance.fillRule', 'native appearance uses nonzero compound contours')
        require(a['bindingSha256'] == appearance_binding(operation), at+'.appearance.bindingSha256',
                'stale appearance: geometry or profile changed; regenerate it')
        contours = array_at(a['contours'], at+'.appearance.contours')
        require(1 <= len(contours) <= 10000, at, 'appearance needs closed contours')
        for i, contour in enumerate(contours):
            path_record(contour, f'{at}.appearance.contours[{i}]')
            require(contour['closed'], at, 'appearance contour must be closed')
            require(set(contour) == {'closed','commands'}, at, 'appearance contours cannot carry drawing operations or profiles')


def centerlines(font):
    """Explicit lossy 0.3 projection; retain layout and every XY drawing value."""
    from .validation import validate
    validate(font)
    result = copy.deepcopy(font)
    removed = 0
    for glyph in result['glyphs']:
        for operation in glyph['strokes']:
            removed += int(operation.pop('penProfile', None) is not None)
    result['version'] = '0.3'
    if removed:
        result.setdefault('metadata', {}).setdefault('exportWarnings', []).append(
            f'Explicit centerlines-only export: removed {removed} pen profiles and appearance references; variation is not retained.')
    return validate(result)


def curve_segments(operation):
    start = operation['commands'][0][1:]
    origin = start
    for command in operation['commands'][1:]:
        yield [origin, *[command[i:i+2] for i in range(1,len(command),2)]]
        origin = command[-2:]
    if operation['closed'] and origin != start:
        yield [origin, start]


def bezier(points, t):
    work = [list(p) for p in points]
    while len(work) > 1:
        work = [[a+(b-a)*t for a,b in zip(p,q)] for p,q in zip(work,work[1:])]
    return work[0]


def samples(operation, max_step=2., max_samples=100000):
    """Preview sampling; not a machine flattening or physical error guarantee."""
    count = 0
    for i, points in enumerate(curve_segments(operation)):
        length = sum(math.dist(a,b) for a,b in zip(points,points[1:]))
        n = max(1, math.ceil(length/max_step))
        count += n+1
        if count > max_samples:
            from .validation import ValidationError
            raise ValidationError('profile preview exceeds sample limit')
        for j in range(n+1):
            t = j/n
            tangent = bezier([[len(points[:-1])*(b-a) for a,b in zip(p,q)] for p,q in zip(points,points[1:])],t)
            yield i, t, bezier(points,t), tangent


def linear_values(profile, segment, t):
    """Linear channels in segment-index + Bezier-t; angles are unwrapped degrees."""
    x = segment+t
    controls = [(q['segment']+q['t'], {k:q['values'].get(k) if q['values'].get(k) is not None else profile['defaults'][k]
                                    for k in CHANNELS}) for q in profile['points']]
    if not controls:
        return dict(profile['defaults'])
    left = next((q for q in reversed(controls) if q[0] <= x), controls[0])
    right = next((q for q in controls if q[0] >= x), controls[-1])
    u = (x-left[0])/(right[0]-left[0]) if right[0] != left[0] else 0
    return {k:left[1][k]+u*(right[1][k]-left[1][k]) for k in CHANNELS}


def linear_appearance(operation, step=2.):
    """Reference ellipse sweep, sampled at <= step FU control-polygon spacing.

    This is a bounded preview approximation, not native Glyphs interpolation.
    """
    from .validation import ValidationError
    profile = operation['penProfile']
    if profile['style'] != {'capStart':'round','capEnd':'round','join':'round'}:
        raise ValidationError('linear profile preview currently supports round caps/joins only')
    contours = []
    for segment,t,xy,tangent in samples(operation,step,max_samples=10000):
        v = linear_values(profile,segment,t)
        theta = math.atan2(tangent[1],tangent[0])
        nx,ny = -math.sin(theta),math.cos(theta)
        offset = -v['strokePosition']*v['width']/2
        cx,cy = xy[0]+nx*offset,xy[1]+ny*offset
        angle = theta+math.radians(v['angle'])
        # Width is normal to the path, height is along its tangent at angle=0.
        points = []
        for i in range(48):
            a = i*math.tau/48
            u,w = v['height']/2*math.cos(a),v['width']/2*math.sin(a)
            points.append([cx+u*math.cos(angle)-w*math.sin(angle),cy+u*math.sin(angle)+w*math.cos(angle)])
        contours.append({'closed':True,'commands':[['M',*points[0]], *[['L',*p] for p in points[1:]]]})
    return contours
