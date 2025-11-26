import express from 'express';
import MenuItem from '../models/MenuItem.js';

const router = express.Router();

// Get all menu items
router.get('/', async (req, res) => {
    try {
        const { cafeteria, category, veg } = req.query;
        const filter = {};

        if (cafeteria) filter.cafeteria = cafeteria;
        if (category) filter.category = category;
        if (veg !== undefined) filter.veg = veg === 'true';

        const items = await MenuItem.find(filter);
        res.status(200).json({
            success: true,
            data: items
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
});

// Get single menu item
router.get('/:id', async (req, res) => {
    try {
        const item = await MenuItem.findById(req.params.id);
        if (!item) {
            return res.status(404).json({
                success: false,
                message: 'Menu item not found'
            });
        }
        res.status(200).json({
            success: true,
            data: item
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
});

// Create menu item (Admin)
router.post('/', async (req, res) => {
    try {
        const item = await MenuItem.create(req.body);
        res.status(201).json({
            success: true,
            data: item
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
});

// Update menu item (Admin)
router.put('/:id', async (req, res) => {
    try {
        const item = await MenuItem.findByIdAndUpdate(
            req.params.id,
            req.body,
            { new: true, runValidators: true }
        );
        res.status(200).json({
            success: true,
            data: item
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
});

export default router;
