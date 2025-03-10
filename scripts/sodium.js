window.loadLibsodium = async () => {
  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = src;
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  await loadScript('https://cdn.jsdelivr.net/npm/libsodium@0.7.15/dist/modules/libsodium.min.js');
  await loadScript('https://cdn.jsdelivr.net/npm/libsodium-wrappers@0.7.15/dist/modules/libsodium-wrappers.min.js');
  await sodium.ready;
}