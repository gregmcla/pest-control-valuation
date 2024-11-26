const express = require('express');
const app = express();

app.use(express.json());

// Simple valuation endpoint
app.post('/api/valuate', (req, res) => {
    try {
        const { revenue, ebitda, retention } = req.body;
        
        // Basic valuation logic
        const multiple = 4 + (retention > 80 ? 1 : 0);
        const value = (ebitda * multiple) + (revenue * 0.5);
        
        res.json({
            value,
            metrics: {
                multiple,
                revenueMultiple: (value / revenue).toFixed(2),
                riskScore: Math.min(Math.round((retention / 10) + (ebitda / revenue * 10)), 10)
            }
        });
    } catch (error) {
        res.status(400).json({ error: 'Invalid input data' });
    }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));