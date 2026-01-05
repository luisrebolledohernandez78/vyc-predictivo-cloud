async function ping() {
  const res = await fetch("http://127.0.0.1:8000/api/health/");
  const data = await res.json();
  document.getElementById("out").textContent = JSON.stringify(data, null, 2);
}

ping();
