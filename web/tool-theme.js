/* Connect standalone tools to the wiki appearance preference. */
(() => {
  if (/Qaroshi_(18_19|20|21_23)_/.test(location.pathname)) document.documentElement.classList.add('qaroshi-new-tool');
  const theme = window.QaroshiTheme;
  if (!theme) return;
  function sync() {
    const dark = document.documentElement.dataset.theme === 'dark';
    document.body.classList.toggle('dark', dark);
    document.body.dataset.theme = dark ? 'dark' : 'light';
    document.documentElement.dataset.dark = String(dark);
  }
  window.addEventListener('qaroshi-theme-change', sync);
  const bar = document.createElement('div');
  bar.className = 'qaroshi-tool-bar';
  bar.innerHTML = '<a href="index.html">Qaroshi Wiki</a><label>Appearance <select aria-label="Appearance"><option value="system">System</option><option value="light">Light</option><option value="dark">Dark</option></select></label>';
  document.body.prepend(bar);
  // Keep legacy controls in the DOM for their existing event handlers.
  document.querySelectorAll('button#theme, button#themeBtn, button#themeToggle, button#darkbtn').forEach(button => { button.hidden = true; button.style.display = 'none'; });
  theme.bind(bar.querySelector('select'));
})();
