
const ValuationService = require('../services/ValuationService');

module.exports = async (req, res) => {
    try {
        const valuationService = new ValuationService();
        const result = await valuationService.calculateValuation(req.body);
        res.json(result);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
};