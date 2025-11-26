import dotenv from 'dotenv';
import connectDB from './config/database.js';
import College from './models/College.js';
import MenuItem from './models/MenuItem.js';

dotenv.config();

const seedDatabase = async () => {
    try {
        await connectDB();
        console.log('Connected to MongoDB');

        // Clear existing data
        await College.deleteMany({});
        await MenuItem.deleteMany({});
        console.log('Cleared existing data');

        // Seed colleges
        const colleges = await College.insertMany([
            {
                name: "ABES Engineering College",
                location: "Ghaziabad",
                icon: "fas fa-graduation-cap",
                cafeterias: ["Main Cafeteria", "Food Court", "QuickBite Corner"],
                image: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                description: "Premier engineering college with multiple dining options"
            },
            {
                name: "ABES Institute Of Technology",
                location: "Ghaziabad",
                icon: "fas fa-laptop-code",
                cafeterias: ["Tech Cafe", "Main Cafeteria", "Snack Bar"],
                image: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                description: "Information technology focused campus with modern facilities"
            },
            {
                name: "IMS GHAZIABAD",
                location: "Ghaziabad",
                icon: "fas fa-university",
                cafeterias: ["Central Cafeteria", "North Block Cafe"],
                image: "https://images.unsplash.com/photo-1562774053-701939374585?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                description: "Management and technology institute"
            },
            {
                name: "KIET Group of Institutions",
                location: "Ghaziabad",
                icon: "fas fa-school",
                cafeterias: ["Main Cafeteria", "Engineering Block Cafe", "MBA Cafeteria"],
                image: "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                description: "Multi-disciplinary educational group"
            },
            {
                name: "IMS Engineering College",
                location: "Ghaziabad",
                icon: "fas fa-book",
                cafeterias: ["Main Cafeteria", "Library Cafe"],
                image: "https://images.unsplash.com/photo-1591123120675-6f7f1aae0e5b?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                description: "Engineering and management studies"
            },
            {
                name: "Ajay Kumar Garg Engineering College",
                location: "Ghaziabad",
                icon: "fas fa-laptop-code",
                cafeterias: ["Main Cafeteria", "Tech Hub Cafe"],
                image: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                description: "Technical education excellence"
            }
        ]);
        console.log(`${colleges.length} colleges seeded`);

        // Seed menu items
        const menuItems = await MenuItem.insertMany([
            {
                name: "Masala Dosa",
                description: "Crispy dosa with potato filling",
                price: 60,
                category: "Breakfast",
                veg: true,
                cafeteria: "Main Cafeteria",
                image: "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                available: true
            },
            {
                name: "Chole Bhature",
                description: "Spicy chickpeas with fried bread",
                price: 80,
                category: "Lunch",
                veg: true,
                cafeteria: "Main Cafeteria",
                image: "https://images.unsplash.com/photo-1630918451773-2788d4b5ed18?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                available: true
            },
            {
                name: "Veg Thali",
                description: "Complete meal with rice, dal, vegetables",
                price: 120,
                category: "Lunch",
                veg: true,
                cafeteria: "Main Cafeteria",
                image: "https://images.unsplash.com/photo-1546833999-b9f581a1996d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                available: true
            },
            {
                name: "Paneer Butter Masala",
                description: "Cottage cheese in rich tomato gravy",
                price: 180,
                category: "Lunch",
                veg: true,
                cafeteria: "Main Cafeteria",
                image: "https://images.unsplash.com/photo-1565557623262-b51c2513a641?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                available: true
            },
            {
                name: "Veg Burger",
                description: "Fresh vegetable burger with cheese",
                price: 50,
                category: "Snacks",
                veg: true,
                cafeteria: "Food Court",
                image: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                available: true
            },
            {
                name: "French Fries",
                description: "Crispy golden fries",
                price: 40,
                category: "Snacks",
                veg: true,
                cafeteria: "Food Court",
                image: "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                available: true
            },
            {
                name: "Pasta",
                description: "Creamy white sauce pasta",
                price: 70,
                category: "Lunch",
                veg: true,
                cafeteria: "Food Court",
                image: "https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                available: true
            },
            {
                name: "Samosa",
                description: "Crispy pastry with potato filling",
                price: 20,
                category: "Snacks",
                veg: true,
                cafeteria: "QuickBite Corner",
                image: "https://images.unsplash.com/photo-1601050690597-df0568f70950?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                available: true
            }
        ]);
        console.log(`${menuItems.length} menu items seeded`);

        console.log('Database seeded successfully!');
        process.exit(0);
    } catch (error) {
        console.error('Error seeding database:', error);
        process.exit(1);
    }
};

seedDatabase();
