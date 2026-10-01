const cards = [...document.querySelectorAll(".font-card")];
const search = document.querySelector("#font-search");
const collection = document.querySelector("#font-collection");

if (search && collection) {
  document.querySelector(".catalog-tools").hidden = false;
  const filter = () => {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    for (const card of cards) {
      card.hidden = !(card.dataset.search.includes(query) &&
        (collection.value === "all" || card.dataset.collection === collection.value));
      if (!card.hidden) visible++;
    }
    document.querySelector("#catalog-count").textContent = `${visible} ${visible === 1 ? "font" : "fonts"}`;
    document.querySelector(".empty-state").hidden = visible !== 0;
  };
  search.addEventListener("input", filter);
  collection.addEventListener("change", filter);
}
