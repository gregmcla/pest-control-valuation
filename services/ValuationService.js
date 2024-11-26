
class ValuationService {
    calculateEBITDAMultiple(ebitda, retention, recurring) {
        const baseMultiple = 4;
        let multiple = baseMultiple;
        
        if (retention > 85) multiple += 0.5;
        if (recurring > 70) multiple += 0.5;
        
        return ebitda * multiple;
    }

    calculateRevenueMultiple(revenue, recurring) {
        const baseMultiple = 1;
        let multiple = baseMultiple + (recurring / 100);
        return revenue * multiple;
    }

    calculateAssetValue(equipment, vehicles) {
        return equipment + (vehicles * 25000);
    }

    calculateCustomerValue(customers, retention) {
        const averageCustomerValue = 500;
        return customers * averageCustomerValue * (retention / 100);
    }

    async calculateValuation(data) {
        this.validateInput(data);

        const ebitdaMultiple = this.calculateEBITDAMultiple(
            data.ebitda,
            data.customerRetention,
            data.recurringRevenue
        );

        const revenueMultiple = this.calculateRevenueMultiple(
            data.annualRevenue,
            data.recurringRevenue
        );

        const assetValuation = this.calculateAssetValue(
            data.equipmentValue,
            data.vehicleCount
        );

        const customerValueMultiple = this.calculateCustomerValue(
            data.customerCount,
            data.customerRetention
        );

        const finalValuation = (
            (ebitdaMultiple * 0.4) +
            (revenueMultiple * 0.3) +
            (assetValuation * 0.1) +
            (customerValueMultiple * 0.2)
        );

        return {
            finalValuation,
            breakdown: {
                ebitdaValue: ebitdaMultiple,
                revenueValue: revenueMultiple,
                assetValue: assetValuation,
                customerValue: customerValueMultiple
            }
        };
    }

    validateInput(data) {
        const requiredFields = [
            'annualRevenue',
            'ebitda',
            'recurringRevenue',
            'customerCount',
            'customerRetention',
            'yearsInBusiness',
            'equipmentValue',
            'vehicleCount'
        ];

        for (const field of requiredFields) {
            if (!data[field] && data[field] !== 0) {
                throw new Error(`Missing required field: ${field}`);
            }
            if (typeof data[field] !== 'number') {
                throw new Error(`${field} must be a number`);
            }
        }

        if (data.customerRetention < 0 || data.customerRetention > 100) {
            throw new Error('Customer retention must be between 0 and 100');
        }

        if (data.recurringRevenue < 0 || data.recurringRevenue > 100) {
            throw new Error('Recurring revenue percentage must be between 0 and 100');
        }
    }
}

module.exports = ValuationService;