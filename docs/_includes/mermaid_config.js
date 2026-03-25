// Mermaid post-processing for Jekyll (converts <pre><code class="language-mermaid"> to <div class="mermaid">)
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('pre code.language-mermaid').forEach(function(codeEl) {
    var pre = codeEl.parentElement;
    var div = document.createElement('div');
    div.classList.add('mermaid');
    div.textContent = codeEl.textContent;
    pre.parentNode.replaceChild(div, pre);
  });
  if (typeof mermaid !== 'undefined') {
    mermaid.initialize({ startOnLoad: false, theme: 'default' });
    mermaid.run();
  }
});
