(() => {
  const form = document.querySelector('form[data-rwe-filters]');
  const list = document.querySelector('[data-rwe-paper-list]');
  if (!form || !list) return;

  const search = form.querySelector('#rwe-paper-search');
  const topic = form.querySelector('#rwe-paper-topic');
  const sort = form.querySelector('#rwe-paper-sort');
  const reset = form.querySelector('[data-rwe-reset]');
  const status = document.querySelector('[data-rwe-results]');
  const empty = document.querySelector('[data-rwe-empty]');
  if (!search || !topic || !sort || !reset) return;

  const normalize = (value) => String(value || '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, ' ')
    .trim();

  function readTopics(value) {
    try {
      const topics = JSON.parse(value || '[]');
      return Array.isArray(topics) ? topics.filter((item) => typeof item === 'string') : [];
    } catch (_) {
      return [];
    }
  }

  // Cache text before filtering hides entries, and retain source order for ties.
  const papers = Array.from(list.children)
    .filter((element) => element.matches('[data-rwe-paper]'))
    .map((element, index) => {
      const year = Number(element.dataset.paperYear);
      const date = Date.parse(element.dataset.readingDate || '');
      return {
        element,
        index,
        text: normalize(element.innerText || element.textContent),
        topics: readTopics(element.dataset.readingTopics),
        year: Number.isFinite(year) && year > 0 ? year : -Infinity,
        date: Number.isFinite(date) ? date : -Infinity
      };
    });

  function update() {
    const terms = normalize(search.value).split(' ').filter(Boolean);
    const key = sort.value === 'published' ? 'year' : 'date';
    const ordered = papers.slice().sort((a, b) => b[key] - a[key] || a.index - b.index);
    const fragment = document.createDocumentFragment();
    let matches = 0;

    for (const paper of ordered) {
      const visible = terms.every((term) => paper.text.includes(term))
        && (!topic.value || paper.topics.includes(topic.value));
      paper.element.hidden = !visible;
      if (visible) matches += 1;
      fragment.append(paper.element);
    }

    list.append(fragment);
    if (status) status.textContent = `${matches} of ${papers.length} paper ${papers.length === 1 ? 'note' : 'notes'}`;
    if (empty) empty.hidden = matches !== 0;
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    update();
  });
  search.addEventListener('input', update);
  topic.addEventListener('change', update);
  sort.addEventListener('change', update);
  reset.addEventListener('click', () => {
    search.value = '';
    topic.value = '';
    sort.value = 'added';
    update();
    search.focus();
  });

  update();
  form.hidden = false;
})();
