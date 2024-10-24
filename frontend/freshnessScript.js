// Sample data for freshness detection
const freshnessData = [
    { srNo: 1, name: 'Apple', mfgDate: '2024-10-10', consumedByDate: '2024-10-25', visualAnalysis: 'Excellent Condition' },
    { srNo: 2, name: 'Banana', mfgDate: '2024-10-12', consumedByDate: '2024-10-20', visualAnalysis: 'Good Condition' },
    { srNo: 3, name: 'Tomato', mfgDate: '2024-10-08', consumedByDate: '2024-10-18', visualAnalysis: 'Bad Condition' },
    { srNo: 4, name: 'Carrot', mfgDate: '2024-10-05', consumedByDate: '2024-10-22', visualAnalysis: 'Good Condition' },
    { srNo: 5, name: 'Cabbage', mfgDate: '2024-10-01', consumedByDate: '2024-10-15', visualAnalysis: 'Bad Condition' },
    { srNo: 6, name: 'Grapes', mfgDate: '2024-10-11', consumedByDate: '2024-10-21', visualAnalysis: 'Excellent Condition' },
    { srNo: 7, name: 'Potato', mfgDate: '2024-09-30', consumedByDate: '2024-10-20', visualAnalysis: 'Good Condition' },
    { srNo: 8, name: 'Onion', mfgDate: '2024-10-02', consumedByDate: '2024-10-19', visualAnalysis: 'Good Condition' },
    { srNo: 9, name: 'Mango', mfgDate: '2024-10-09', consumedByDate: '2024-10-24', visualAnalysis: 'Excellent Condition' },
    { srNo: 10, name: 'Spinach', mfgDate: '2024-10-06', consumedByDate: '2024-10-13', visualAnalysis: 'Bad Condition' }
];

// Populate the freshness detection table
function loadFreshnessList() {
    const tableBody = document.getElementById('freshnessList');
    tableBody.innerHTML = ''; // Clear existing rows

    freshnessData.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${product.srNo}</td>
            <td>${product.name}</td>
            <td>${product.mfgDate}</td>
            <td>${product.consumedByDate}</td>
            <td>${product.visualAnalysis}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Load the freshness detection table on page load
window.onload = loadFreshnessList;
