
const mongoose = require('mongoose');

const valuationSchema = new mongoose.Schema({
    annualRevenue: {
        type: Number,
        required: true
    },
    ebitda: {
        type: Number,
        required: true
    },
    recurringRevenue: {
        type: Number,
        required: true,
        min: 0,
        max: 100
    },
    customerCount: {
        type: Number,
        required: true
    },
    customerRetention: {
        type: Number,
        required: true,
        min: 0,
        max: 100
    },
    yearsInBusiness: {
        type: Number,
        required: true
    },
    equipmentValue: {
        type: Number,
        required: true
    },
    vehicleCount: {
        type: Number,
        required: true
    },
    calculatedValue: {
        type: Number,
        required: true
    },
    valuationDate: {
        type: Date,
        default: Date.now
    }
});

module.exports = mongoose.model('Valuation', valuationSchema);