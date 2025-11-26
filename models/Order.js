import mongoose from 'mongoose';

const orderSchema = new mongoose.Schema({
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true,
    },
    items: [{
        menuItem: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'MenuItem',
            required: true,
        },
        quantity: {
            type: Number,
            required: true,
            default: 1,
        },
        price: Number,
    }],
    college: String,
    cafeteria: String,
    totalPrice: {
        type: Number,
        required: true,
    },
    status: {
        type: String,
        enum: ['Pending', 'Confirmed', 'Preparing', 'Ready', 'Completed', 'Cancelled'],
        default: 'Pending',
    },
    notes: {
        type: String,
        trim: true,
    },
    orderToken: {
        type: String,
        unique: true,
    },
    createdAt: {
        type: Date,
        default: Date.now,
    },
    completedAt: Date,
}, { timestamps: true });

export default mongoose.model('Order', orderSchema);
