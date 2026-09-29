const frame = document.getElementById('demo-frame');
const viewport = document.querySelector('.demo-viewport');
if (frame && viewport) {
  const fit = () => {
    frame.style.transform = `scale(${viewport.clientWidth / 1280})`;
  };
  fit();
  new ResizeObserver(fit).observe(viewport);
}
for (const button of document.querySelectorAll('[data-demo-action]')) {
  button.addEventListener('click', () => {
    frame.contentWindow?.postMessage(
      { type: 'demo-control', action: button.dataset.demoAction },
      window.location.origin
    );
  });
}
