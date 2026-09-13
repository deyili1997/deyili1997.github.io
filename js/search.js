(() => {
  const form = document.getElementById('note-search');
  if (!form) return;

  const input = document.getElementById('search-query');
  const status = document.getElementById('search-status');
  const results = document.getElementById('search-results');
  const resultsSection = document.getElementById('search-results-section');
  let indexPromise;
  let requestId = 0;

  const normalize = (value) => String(value || '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLocaleLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, ' ')
    .trim();

  function loadIndex() {
    if (indexPromise) return indexPromise;
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 15000);
    indexPromise = fetch(form.dataset.index, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error('Search index unavailable');
        return response.json();
      })
      .then((items) => {
        if (!Array.isArray(items)) throw new Error('Invalid search index');
        return items.map((item) => {
          if (typeof item.title !== 'string' || typeof item.url !== 'string') {
            throw new Error('Invalid search entry');
          }
          const url = new URL(item.url, window.location.origin);
          if (url.origin !== window.location.origin) throw new Error('Invalid search URL');
          return {
            ...item,
            url: url.href,
            normalizedTitle: normalize(item.title),
            normalizedTags: normalize(Array.isArray(item.tags) ? item.tags.join(' ') : ''),
            normalizedDescription: normalize(item.description)
          };
        });
      })
      .catch((error) => {
        indexPromise = undefined;
        throw error;
      })
      .finally(() => window.clearTimeout(timeout));
    return indexPromise;
  }

  async function search(query) {
    const currentRequest = ++requestId;
    results.replaceChildren();
    resultsSection.hidden = true;
    const normalizedQuery = normalize(query);
    if (!normalizedQuery) {
      status.textContent = 'Enter a search term to find notes.';
      return;
    }

    status.textContent = 'Searching…';
    try {
      const items = await loadIndex();
      if (currentRequest !== requestId) return;
      const terms = normalizedQuery.split(/\s+/);
      const matches = items.map((item) => {
        const text = `${item.normalizedTitle} ${item.normalizedTags} ${item.normalizedDescription}`;
        if (!terms.every((term) => text.includes(term))) return null;
        const score = (item.normalizedTitle.includes(normalizedQuery) ? 10 : 0)
          + terms.reduce((total, term) => total
            + (item.normalizedTitle.includes(term) ? 3 : 0)
            + (item.normalizedTags.includes(term) ? 1 : 0), 0);
        return { item, score };
      }).filter(Boolean).sort((a, b) => b.score - a.score || a.item.title.localeCompare(b.item.title));

      const fragment = document.createDocumentFragment();
      for (const { item } of matches) {
        const result = document.createElement('li');
        const link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.title;
        result.append(link);
        if (item.description) {
          const description = document.createElement('p');
          description.textContent = item.description;
          result.append(description);
        }
        fragment.append(result);
      }
      results.append(fragment);
      resultsSection.hidden = matches.length === 0;
      status.textContent = matches.length
        ? `${matches.length} ${matches.length === 1 ? 'note' : 'notes'} found for “${query}”.`
        : `No notes found for “${query}”. Try a broader term or browse the topic index.`;
    } catch (_) {
      if (currentRequest !== requestId) return;
      status.textContent = 'Search is temporarily unavailable. Please try again or browse the topic index above.';
    }
  }

  function searchFromUrl() {
    const query = (new URLSearchParams(window.location.search).get('q') || '').slice(0, 200);
    input.value = query;
    if (query) search(query);
    else {
      ++requestId;
      results.replaceChildren();
      resultsSection.hidden = true;
      status.textContent = '';
    }
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const query = input.value.trim().slice(0, 200);
    input.value = query;
    const url = new URL(window.location.href);
    if (query) url.searchParams.set('q', query);
    else url.searchParams.delete('q');
    if (url.href !== window.location.href) window.history.pushState(null, '', url);
    search(query);
  });
  window.addEventListener('popstate', searchFromUrl);
  searchFromUrl();
})();
