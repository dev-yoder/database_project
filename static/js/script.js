document.addEventListener("DOMContentLoaded", async () => {
  const data = await fetch("/sample_data.json").then((res) => res.json());
  console.log("Fetched data:", data); // Add this line to log the fetched data

  if (document.getElementById("customer-table")) {
    populateCustomerTable(data);
  }

  if (document.getElementById("area-container")) {
    populateAreaBreakdown(data);
  }
});


  
  function populateCustomerTable(data) {
    const customerTable = document.getElementById("customer-table");
  
    data.areas.forEach((area) => {
      area.customers.forEach((customer) => {
        const row = document.createElement("tr");
  
        const idCell = document.createElement("td");
        idCell.textContent = customer.id;
        row.appendChild(idCell);
  
        const nameCell = document.createElement("td");
        nameCell.textContent = customer.name;
        nameCell.addEventListener("dblclick", () => showCustomerDetails(customer));
        row.appendChild(nameCell);
  
        const areaCell = document.createElement("td");
        areaCell.textContent = area.name;
        row.appendChild(areaCell);
  
        customerTable.appendChild(row);
      });
    });
  }
  
  function populateAreaBreakdown(data) {
    const areaContainer = document.getElementById("area-container");
  
    data.areas.forEach((area) => {
      const areaColumn = document.createElement("div");
      areaColumn.className = "col";
  
      const areaTitle = document.createElement("h4");
      areaTitle.textContent = area.name;
      areaColumn.appendChild(areaTitle);
  
      populateCustomerNames(areaColumn, area.customers);
      areaContainer.appendChild(areaColumn);
    });
  }
  
  function populateCustomerNames(areaColumn, customers) {
    for (const customer of customers) {
      const customerName = document.createElement("div");
      customerName.className = "customer-name";
      customerName.textContent = customer.name;
      customerName.addEventListener("dblclick", () => showCustomerDetails(customer));
      areaColumn.appendChild(customerName);
    }
  }
  
  function showCustomerDetails(customer) {
    const customerDetails = `Name: ${customer.name}\nAddress: ${customer.address}\nInstallation Status: ${customer.installation_status}`;
    window.open().document.write(`<pre>${customerDetails}</pre>`);
  }
  