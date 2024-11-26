
document.getElementById('valuationForm').addEventListener('submit', function(e) {
    e.preventDefault();
    calculateValuation();
});

function calculateValuation() {
    // Get input values
    const annualRevenue = parseFloat(document.getElementById('annualRevenue').value);
    const ebitda = parseFloat(document.getElementById('ebitda').value);
    const recurringRevenue = parseFloat(document.getElementById('recurringRevenue').value);
    const customerCount = parseInt(document.getElementById('customerCount').value);
    const customerRetention = parseFloat(document.getElementById('customerRetention').value);
    const yearsInBusiness = parseInt(document.getElementById('yearsInBusiness').value);
    const equipmentValue = parseFloat(document.getElementById('equipmentValue').value);
    const vehicleCount = parseInt(document.getElementById('vehicleCount').value);

    // Calculate multiple valuation methods
    const ebitdaMultiple = calculateEBITDAMultiple(ebitda, customerRetention, recurringRevenue);
    const revenueMultiple = calculateRevenueMultiple(annualRevenue, recurringRevenue);
    const assetValuation = calculateAssetValue(equipmentValue, vehicleCount);
    const customerValueMultiple = calculateCustomerValue(customerCount, customerRetention);

    // Weight the different valuation methods
    const finalValuation = (
        (ebitdaMultiple * 0.4) +
        (revenueMultiple * 0.3) +
        (assetValuation * 0.1) +
        (customerValueMultiple * 0.2)
    );

    displayResults(finalValuation, {
        ebitdaValue: ebitdaMultiple,
        revenueValue: revenueMultiple,
        assetValue: assetValuation,
        customerValue: customerValueMultiple
    });
}

function calculateEBITDAMultiple(ebitda, retention, recurring) {
    const baseMultiple = 4;
    let multiple = baseMultiple;
    
    if (retention > 85) multiple += 0.5;
    if (recurring > 70) multiple += 0.5;
    
    return ebitda * multiple;
}

function calculateRevenueMultiple(revenue, recurring) {
    const baseMultiple = 1;
    let multiple = baseMultiple + (recurring / 100);
    return revenue * multiple;
}

function calculateAssetValue(equipment, vehicles) {
    return equipment + (vehicles * 25000); // Average vehicle value
}

function calculateCustomerValue(customers, retention) {
    const averageCustomerValue = 500;
    return customers * averageCustomerValue * (retention / 100);
}

function displayResults(finalValue, breakdown) {
    const results = document.getElementById('results');
    const valuationResult = document.getElementById('valuationResult');
    const valuationBreakdown = document.getElementById('valuationBreakdown');

    valuationResult.innerHTML = `Estimated Business Value: $${finalValue.toLocaleString()}`;
    
    valuationBreakdown.innerHTML = `
        <p>Valuation Breakdown:</p>
        <ul>
            <li>EBITDA-Based Value: $${breakdown.ebitdaValue.toLocaleString()}</li>
            <li>Revenue-Based Value: $${breakdown.revenueValue.toLocaleString()}</li>
            <li>Asset-Based Value: $${breakdown.assetValue.toLocaleString()}</li>
            <li>Customer Value: $${breakdown.customerValue.toLocaleString()}</li>
        </ul>
    `;

    results.classList.remove('hidden');
}