
const express = require('express');
const router = express.Router();
const ValuationService = require('../services/ValuationService');
const Valuation = require('../models/Valuation');

router.post('/calculate', async (req, res) => {
    try {
        const valuationService = new ValuationService();
        const result = await valuationService.calculateValuation(req.body);
        
        // Save valuation to database
        const valuation = new Valuation({
            ...req.body,
            calculatedValue: result.finalValuation
        });
        await valuation.save();

        res.json(result);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

router.get('/history', async (req, res) => {
    try {
        const valuations = await Valuation.find()
            .sort({ valuationDate: -1 })
            .limit(10);
        res.json(valuations);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;