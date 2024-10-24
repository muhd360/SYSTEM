// Sample data for parcel defect detection
const parcelData = [
    { srNo: 1, packageId: 'PKG001', defect: 'No' },
    { srNo: 2, packageId: 'PKG002', defect: 'Yes' },
    { srNo: 3, packageId: 'PKG003', defect: 'No' },
    { srNo: 4, packageId: 'PKG004', defect: 'Yes' },
    { srNo: 5, packageId: 'PKG005', defect: 'No' },
    { srNo: 6, packageId: 'PKG006', defect: 'No' },
    { srNo: 7, packageId: 'PKG007', defect: 'Yes' },
    { srNo: 8, packageId: 'PKG008', defect: 'No' },
    { srNo: 9, packageId: 'PKG009', defect: 'Yes' },
    { srNo: 10, packageId: 'PKG010', defect: 'No' }
];

// Populate the parcel defect detection table
function loadParcelDefectList() {
    const tableBody = document.getElementById('parcelDefectList');
    tableBody.innerHTML = ''; // Clear existing rows

    parcelData.forEach(parcel => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${parcel.srNo}</td>
            <td>${parcel.packageId}</td>
            <td>${parcel.defect}</td>
        `;
        // Apply different background colors based on defect status
        row.style.backgroundColor = parcel.defect === 'Yes' ? '#ffebee' : '#e8f5e9';
        tableBody.appendChild(row);
    });
}

// Load the parcel defect detection table on page load
window.onload = loadParcelDefectList;
