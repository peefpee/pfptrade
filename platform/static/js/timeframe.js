document.addEventListener('DOMContentLoaded', () => {
  const timeframeSelect = document.getElementById('timeframeSelect');
  if (!timeframeSelect) return console.error('Timeframe select not found');

  timeframeSelect.addEventListener('change', function () {
    const params = new URLSearchParams(window.location.search);
    params.set('timeframe', this.value);
    window.location.search = params.toString();
  });
});
