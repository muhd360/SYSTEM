// Sample OCR output data
const ocrOutput = [
    { srNo: 1, brandName: 'Lays', itemDetails: 'Chips', packSize: 'Small' },
    { srNo: 2, brandName: 'Dove', itemDetails: 'Shampoo', packSize: 'Medium' },
    { srNo: 3, brandName: 'Himalaya', itemDetails: 'Face Wash', packSize: 'Big' },
    { srNo: 4, brandName: 'Parachute', itemDetails: 'Oil', packSize: 'Medium' },
    { srNo: 5, brandName: 'Nivea', itemDetails: 'Body Lotion', packSize: 'Big' },
    { srNo: 6, brandName: 'Tata', itemDetails: 'Salt', packSize: 'Small' },
    { srNo: 7, brandName: 'Britannia', itemDetails: 'Biscuits', packSize: 'Medium' },
    { srNo: 8, brandName: 'Patanjali', itemDetails: 'Aloe Vera Gel', packSize: 'Small' },
    { srNo: 9, brandName: 'Colgate', itemDetails: 'Toothpaste', packSize: 'Medium' },
    { srNo: 10, brandName: 'Amul', itemDetails: 'Butter', packSize: 'Small' }
];

// Populate the OCR output table
function loadOcrOutputList() {
    const tableBody = document.getElementById('ocrOutputList');
    tableBody.innerHTML = ''; // Clear existing rows

    ocrOutput.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${product.srNo}</td>
            <td>${product.brandName}</td>
            <td>${product.itemDetails}</td>
            <td>${product.packSize}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Load the OCR output table on page load
window.onload = loadOcrOutputList;
