import mongoose from 'mongoose';

const menuItemSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, 'Please provide menu item name'],
        trim: true,
    },
    description: {
        type: String,
        trim: true,
    },
    price: {
        type: Number,
        required: [true, 'Please provide price'],
    },
    category: {
        type: String,
        enum: ['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Beverages', 'Desserts'],
        default: 'Snacks',
    },
    veg: {
        type: Boolean,
        default: false,
    },
    cafeteria: {
        type: String,
        trim: true,
    },
    image: String,
    available: {
        type: Boolean,
        default: true,
    },
    createdAt: {
        type: Date,
        default: Date.now,
    },
}, { timestamps: true });

export default mongoose.model('MenuItem', menuItemSchema);
