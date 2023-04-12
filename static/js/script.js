document.addEventListener('DOMContentLoaded', function() {
  fetchData();
});

async function fetchData() {
  const response = await fetch('/area_data');
  const data = await response.json();
  console.log(data);

  const area_breakdown = document.getElementById('area_breakdown');
  area_breakdown.innerHTML = '';

  for (const area of data) {
    const option = document.createElement('option');
    option.value = area.id;
    option.textContent = area.name;
    area_breakdown.appendChild(option);
  }
}

function changeArea() {
  const area_breakdown = document.getElementById('area_breakdown');
  const selectedAreaId = area_breakdown.value;
  console.log(`Selected Area ID: ${selectedAreaId}`);
}
