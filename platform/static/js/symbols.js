fetch(symbolsurl)
  .then(res => res.json())
  .then(data => {
    console.log("Symbols data received:", data.symbols);
    const select = document.getElementById('symbolSelect');
    select.innerHTML = ''; // Clear placeholder

    const placeholder = document.createElement('option');
    placeholder.disabled = true;
    placeholder.selected = true;
    placeholder.textContent = 'Pick a Symbol';
    select.appendChild(placeholder);

    data.symbols.sort().forEach(symbol => {
      const option = document.createElement('option');
      option.value = symbol;
      option.textContent = symbol;
      select.appendChild(option);
    });

    // Turn into searchable dropdown
    new TomSelect('#symbolSelect', {
      create: false,
      placeholder: 'Pick a Symbol...',
      sortField: { field: 'text', direction: 'asc' },
    });

    // Handle change
    select.addEventListener('change', function () {
      const params = new URLSearchParams(window.location.search);
      params.set('symbol', this.value);
      window.location.search = params.toString();
    });
  })
  .catch(err => console.error("Error loading symbols:", err));
