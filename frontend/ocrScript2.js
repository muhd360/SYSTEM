// Sample OCR output data for OCR Output 2
const ocrOutput2 = [
    { srNo: 1, productName: 'Parle G', mrp: 10, mfgDate: '2024-01-15', expiryDate: '2024-11-15' },
    { srNo: 2, productName: 'Lifebuoy Soap', mrp: 25, mfgDate: '2023-12-01', expiryDate: '2024-12-01' },
    { srNo: 3, productName: 'Bournvita', mrp: 250, mfgDate: '2023-06-10', expiryDate: '2025-06-10' },
    { srNo: 4, productName: 'Amul Butter', mrp: 45, mfgDate: '2024-09-01', expiryDate: '2024-12-01' },
    { srNo: 5, productName: 'Tata Tea', mrp: 120, mfgDate: '2023-11-20', expiryDate: '2025-11-20' },
    { srNo: 6, productName: 'Britannia Cheese', mrp: 80, mfgDate: '2024-02-05', expiryDate: '2024-11-30' },
    { srNo: 7, productName: 'Himalaya Shampoo', mrp: 180, mfgDate: '2024-03-01', expiryDate: '2025-03-01' },
    { srNo: 8, productName: 'Colgate Toothpaste', mrp: 50, mfgDate: '2024-04-01', expiryDate: '2026-04-01' },
    { srNo: 9, productName: 'Nestle Milk', mrp: 60, mfgDate: '2024-10-01', expiryDate: '2024-12-01' },
    { srNo: 10, productName: 'Dove Soap', mrp: 40, mfgDate: '2023-08-15', expiryDate: '2024-08-15' }
];

// Function to calculate days remaining until expiry
function calculateShelfLife(expiryDate) {
    const currentDate = new Date();
    const expiry = new Date(expiryDate);
    const timeDiff = expiry - currentDate;
    const daysLeft = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));
    return daysLeft > 0 ? `${daysLeft} days` : 'Expired';
}

// Populate the OCR output 2 table
function loadOcrOutputList2() {
    const tableBody = document.getElementById('ocrOutputList2');
    tableBody.innerHTML = ''; // Clear existing rows

    ocrOutput2.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${product.srNo}</td>
            <td>${product.productName}</td>
            <td>₹${product.mrp}</td>
            <td>${product.mfgDate}</td>
            <td>${product.expiryDate}</td>
            <td>${calculateShelfLife(product.expiryDate)}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Load the OCR output 2 table on page load
window.onload = loadOcrOutputList2;
