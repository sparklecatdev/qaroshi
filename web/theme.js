/* Shared appearance preference for the wiki and Academy. */
(() => {
  const key = 'qaroshi-theme';
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  let preference = 'system';
  try { preference = localStorage.getItem(key) || 'system'; } catch (_) {}
  if (!['system', 'light', 'dark'].includes(preference)) preference = 'system';
  const controls = new Set();
  function apply() {
    document.documentElement.dataset.theme = preference === 'system' ? (media.matches ? 'dark' : 'light') : preference;
    controls.forEach(control => { control.value = preference; });
  }
  function set(value) {
    if (!['system', 'light', 'dark'].includes(value)) return;
    preference = value;
    try { if (value === 'system') localStorage.removeItem(key); else localStorage.setItem(key, value); } catch (_) {}
    apply();
  }
  window.QaroshiTheme = { bind(control) { controls.add(control); control.addEventListener('change', () => set(control.value)); apply(); } };
  media.addEventListener('change', apply);
  window.addEventListener('storage', event => {
    if (event.key !== key && event.key !== null) return;
    const value = event.key === null ? null : event.newValue;
    preference = value === 'light' || value === 'dark' ? value : 'system';
    apply();
  });
  apply();
})();
