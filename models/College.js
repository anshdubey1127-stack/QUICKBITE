import mongoose from 'mongoose';

const collegeSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, 'Please provide college name'],
        unique: true,
        trim: true,
    },
    location: {
        type: String,
        required: [true, 'Please provide location'],
        trim: true,
    },
    icon: String,
    image: String,
    description: String,
    cafeterias: [{
        type: String,
        trim: true,
    }],
    createdAt: {
        type: Date,
        default: Date.now,
    },
}, { timestamps: true });

export default mongoose.model('College', collegeSchema);
