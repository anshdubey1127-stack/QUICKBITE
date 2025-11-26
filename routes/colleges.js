import express from 'express';
import College from '../models/College.js';

const router = express.Router();

// Get all colleges
router.get('/', async (req, res) => {
    try {
        const colleges = await College.find();
        res.status(200).json({
            success: true,
            data: colleges
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
});

// Get single college
router.get('/:id', async (req, res) => {
    try {
        const college = await College.findById(req.params.id);
        if (!college) {
            return res.status(404).json({
                success: false,
                message: 'College not found'
            });
        }
        res.status(200).json({
            success: true,
            data: college
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
});

// Create college (Admin)
router.post('/', async (req, res) => {
    try {
        const college = await College.create(req.body);
        res.status(201).json({
            success: true,
            data: college
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
});

// Update college (Admin)
router.put('/:id', async (req, res) => {
    try {
        const college = await College.findByIdAndUpdate(
            req.params.id,
            req.body,
            { new: true, runValidators: true }
        );
        res.status(200).json({
            success: true,
            data: college
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
});

export default router;
