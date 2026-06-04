export function formatDate(date) {
  return new Date(date).toLocaleDateString("en-US", {
    year: "numeric", month: "long", day: "numeric",
  });
}
export function debounce(fn, delay = 400) {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), delay); };
}
export function buildPageTree(pages) {
  const map = {};
  const roots = [];
  pages.forEach((p) => { map[p.id] = { ...p, children: [] }; });
  pages.forEach((p) => {
    if (p.parentId && map[p.parentId]) map[p.parentId].children.push(map[p.id]);
    else roots.push(map[p.id]);
  });
  return roots;
}
