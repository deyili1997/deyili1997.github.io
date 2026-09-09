// Keep wide tables and mathematical displays within the article on small screens.
document.querySelectorAll('.study-content table').forEach(table => {
  if (table.parentElement.classList.contains('table-container')) return;
  const wrapper = document.createElement('div');
  wrapper.className = 'table-container';
  wrapper.tabIndex = 0;
  wrapper.setAttribute('role', 'region');
  wrapper.setAttribute('aria-label', 'Scrollable table');
  table.before(wrapper);
  wrapper.append(table);
});
const diagrams = document.querySelectorAll('.mermaid');
if (diagrams.length) {
  try {
    const { default: mermaid } = await import('https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs');
    mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'default', flowchart: { htmlLabels: false }, fontFamily: 'Inter, sans-serif' });
    await mermaid.run({ nodes: diagrams });
  } catch (error) {
    console.warn('Diagram rendering unavailable; diagram text remains readable.', error);
  }
}
