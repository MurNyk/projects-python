// static/script.js

async function fetchTime() {
    const response = await fetch('/current_time');
    const data = await response.json();
    document.getElementById('time').textContent = data.current_time;
  }
  
  // Обновлять время каждые 1000 мс (1 секунда)
  setInterval(fetchTime, 1000);