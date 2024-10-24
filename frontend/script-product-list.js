// Updated product data with items found in India
const products = [
    { srNo: 1, timestamp: '2024-10-19 14:30', itemName: 'Lays Classic Salted', quantity: 20 },
    { srNo: 2, timestamp: '2024-10-19 15:00', itemName: 'Parachute Coconut Oil', quantity: 15 },
    { srNo: 3, timestamp: '2024-10-19 15:30', itemName: 'Himalaya Face Wash', quantity: 30 },
    { srNo: 4, timestamp: '2024-10-19 16:00', itemName: 'Dove Shampoo', quantity: 10 },
    { srNo: 5, timestamp: '2024-10-19 16:30', itemName: 'Nivea Body Lotion', quantity: 25 },
    { srNo: 6, timestamp: '2024-10-19 17:00', itemName: 'Almonds (Badam)', quantity: 18 },
    { srNo: 7, timestamp: '2024-10-19 17:30', itemName: 'Tata Salt', quantity: 22 },
    { srNo: 8, timestamp: '2024-10-19 18:00', itemName: 'Apples (Shimla)', quantity: 12 },
    { srNo: 9, timestamp: '2024-10-19 18:30', itemName: 'Bananas', quantity: 16 },
    { srNo: 10, timestamp: '2024-10-19 19:00', itemName: 'Tomatoes', quantity: 27 }
];

// Populate the product table
function loadProductList() {
    const tableBody = document.getElementById('productList');
    tableBody.innerHTML = ''; // Clear existing rows

    products.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${product.srNo}</td>
            <td>${product.timestamp}</td>
            <td>${product.itemName}</td>
            <td>${product.quantity}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Load the table on page load
window.onload = loadProductList;
