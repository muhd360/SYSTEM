// Sample data for IR-based parcel counting
const parcelCountData = [
    { totalParcels: 150, category: 'Perishable Products', passQty: 30, notPassQty: 20 },
    { totalParcels: 150, category: 'Electronics', passQty: 40, notPassQty: 30 },
    { totalParcels: 150, category: 'Beauty & Care Products', passQty: 35, notPassQty: 25 },
    { totalParcels: 150, category: 'Stationery Items', passQty: 25, notPassQty: 35 }
];

// Populate the parcel counting table
function loadParcelCountList() {
    const tableBody = document.getElementById('parcelCountList');
    tableBody.innerHTML = ''; // Clear existing rows

    parcelCountData.forEach(parcel => {
        const rowGroup = document.createElement('tr');
        rowGroup.innerHTML = `
            <td rowspan="2">${parcel.totalParcels}</td>
            <td rowspan="2">${parcel.category}</td>
            <td rowspan="2">${parcel.passQty + parcel.notPassQty}</td>
            <td>Pass</td>
            <td>${parcel.passQty}</td>
        `;
        tableBody.appendChild(rowGroup);

        const rowGroup2 = document.createElement('tr');
        rowGroup2.innerHTML = `
            <td>Not Pass</td>
            <td>${parcel.notPassQty}</td>
        `;
        tableBody.appendChild(rowGroup2);
    });
}

// Load the parcel counting table on page load
window.onload = loadParcelCountList;
