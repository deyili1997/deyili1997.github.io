/* Keep links to /tags/?tag=... useful alongside the static topic index. */
(() => {
  const query = new URLSearchParams(window.location.search).get('tag');
  if (!query || window.location.hash) return;

  const topic = Array.from(document.querySelectorAll('[data-topic]')).find(
    (section) => section.dataset.topic.toLocaleLowerCase() === query.toLocaleLowerCase()
  );
  if (!topic) return;

  const heading = topic.querySelector('h2');
  if (!heading) return;
  const url = new URL(window.location.href);
  url.hash = heading.id;
  window.history.replaceState(null, '', url);
  heading.scrollIntoView();
})();
