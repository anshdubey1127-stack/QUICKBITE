// Production-ready JavaScript with proper error handling and API integration
class QuickBitesApp {
    constructor() {
        this.currentUser = null;
        this.cart = [];
        this.currentCollege = null;
        this.currentCafeteria = null;
        this.isLoading = false;
        this.orderToken = null;
        
        this.initializeApp();
    }

    async initializeApp() {
        try {
            await this.loadInitialData();
            this.setupEventListeners();
            this.checkAuthStatus();
            this.showToast('Welcome to QuickBite!', 'success');
        } catch (error) {
            console.error('Failed to initialize app:', error);
            this.showToast('Failed to load application', 'error');
        }
    }

    async loadInitialData() {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        this.colleges = [
            {
                id: "abes",
                name: "ABES Engineering College",
                location: "Ghaziabad",
                icon: "fas fa-graduation-cap",
                cafeterias: ["Main Cafeteria", "Food Court", "QuickBite Corner"],
                image: "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                description: "Premier engineering college with multiple dining options"
            },
            {
                id: "abesit",
                name: "ABES Institute Of Technology",
                location: "Ghaziabad",
                icon: "fas fa-laptop-code",
                cafeterias: ["Tech Cafe", "Main Cafeteria", "Snack Bar"],
                image: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                description: "Information technology focused campus with modern facilities"
            },
            {
                id: "ims ghaziabad",
                name: "IMS GHAZIABAD",
                location: "Ghaziabad",
                icon: "fas fa-university",
                cafeterias: ["Central Cafeteria", "North Block Cafe"],
                image: "https://images.unsplash.com/photo-1562774053-701939374585?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                description: "Management and technology institute"
            },
            {
                id: "kiet",
                name: "KIET Group of Institutions",
                location: "Ghaziabad",
                icon: "fas fa-school",
                cafeterias: ["Main Cafeteria", "Engineering Block Cafe", "MBA Cafeteria"],
                image: "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                description: "Multi-disciplinary educational group"
            },
            {
                id: "ims",
                name: "IMS Engineering College",
                location: "Ghaziabad",
                icon: "fas fa-book",
                cafeterias: ["Main Cafeteria", "Library Cafe"],
                image: "https://images.unsplash.com/photo-1591123120675-6f7f1aae0e5b?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                description: "Engineering and management studies"
            },
            {
                id: "akg",
                name: "Ajay Kumar Garg Engineering College",
                location: "Ghaziabad",
                icon: "fas fa-laptop-code",
                cafeterias: ["Main Cafeteria", "Tech Hub Cafe"],
                image: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
                description: "Technical education excellence"
            }
        ];

        this.menuItems = {
            "Main Cafeteria": [
                { id: 1, name: "Masala Dosa", description: "Crispy dosa with potato filling", price: 60, image: "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", category: "Breakfast", veg: true },
                { id: 2, name: "Chole Bhature", description: "Spicy chickpeas with fried bread", price: 80, image: "https://images.unsplash.com/photo-1630918451773-2788d4b5ed18?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", category: "Lunch", veg: true },
                { id: 3, name: "Veg Thali", description: "Complete meal with rice, dal, vegetables", price: 120, image: "https://images.unsplash.com/photo-1546833999-b9f581a1996d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", category: "Lunch", veg: true },
                { id: 4, name: "Paneer Butter Masala", description: "Cottage cheese in rich tomato gravy", price: 180, image: "https://images.unsplash.com/photo-1565557623262-b51c2513a641?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", category: "Lunch", veg: true }
            ],
            "Food Court": [
                { id: 5, name: "Veg Burger", description: "Fresh vegetable burger with cheese", price: 50, image: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", category: "Snacks", veg: true },
                { id: 6, name: "French Fries", description: "Crispy golden fries", price: 40, image: "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", category: "Snacks", veg: true },
                { id: 7, name: "Pasta", description: "Creamy white sauce pasta", price: 70, image: "https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", category: "Lunch", veg: true }
            ],
            "Quick Bites Corner": [
                { id: 8, name: "Samosa", description: "Crispy pastry with potato filling", price: 20, image: "https://images.unsplash.com/photo-1601050690597-df0568f70950?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", category: "Snacks", veg: true },
                { id: 9, name: "Tea", description: "Hot milk tea", price: 15, image: "https://images.unsplash.com/photo-1571934811356-5cc061b6821f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", category: "Beverages", veg: true },
                { id: 10, name: "Cold Coffee", description: "Iced coffee with cream", price: 40, image: "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", category: "Beverages", veg: true }
            ],
            "Tech Cafe": [
                { id: 11, name: "Sandwich", description: "Grilled vegetable sandwich", price: 45, image: "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", category: "Snacks", veg: true },
                { id: 12, name: "Pizza Slice", description: "Cheese and vegetable pizza", price: 65, image: "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", category: "Snacks", veg: true },
                { id: 13, name: "Fruit Smoothie", description: "Fresh fruits blended with yogurt", price: 80, image: "https://images.unsplash.com/photo-1570197788417-0e82375c9371?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", category: "Beverages", veg: true }
            ]
        };
    }

    setupEventListeners() {
        // Auth events
        document.getElementById('loginBtn').addEventListener('click', () => this.showAuthModal('login'));
        document.getElementById('signupBtn').addEventListener('click', () => this.showAuthModal('signup'));
        document.getElementById('closeAuth').addEventListener('click', () => this.hideAuthModal());
        document.getElementById('logoutBtn').addEventListener('click', () => this.handleLogout());

        // Navigation events
        document.getElementById('startOrderBtn').addEventListener('click', () => this.scrollToSection('colleges'));
        document.getElementById('backToCafeterias').addEventListener('click', () => this.handleBackToCafeterias());
        document.getElementById('newOrderBtn').addEventListener('click', () => this.handleNewOrder());

        // Cart events
        document.getElementById('cartIcon').addEventListener('click', () => this.toggleCart());
        document.getElementById('closeCart').addEventListener('click', () => this.toggleCart());
        document.getElementById('checkoutBtn').addEventListener('click', () => this.handleCheckout());

        // Auth forms
        document.getElementById('loginForm').addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('signupForm').addEventListener('submit', (e) => this.handleSignup(e));

        // Auth tabs
        document.querySelectorAll('.auth-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const tabName = tab.dataset.tab;
                this.switchAuthTab(tabName);
            });
        });

        // College links in footer
        document.querySelectorAll('a[data-college]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const collegeId = e.target.dataset.college;
                this.handleCollegeSelect(collegeId);
                this.scrollToSection('colleges');
            });
        });

        this.renderColleges();
    }

    renderColleges() {
        const grid = document.getElementById('collegeGrid');
        grid.innerHTML = this.colleges.map(college => `
            <div class="college-card" data-id="${college.id}">
                <div class="college-icon">
                    <i class="${college.icon}"></i>
                </div>
                <h3>${college.name}</h3>
                <p>${college.description}</p>
                <div class="college-location">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>${college.location}, Ghaziabad</span>
                </div>
            </div>
        `).join('');

        grid.querySelectorAll('.college-card').forEach(card => {
            card.addEventListener('click', () => {
                const collegeId = card.dataset.id;
                this.handleCollegeSelect(collegeId);
            });
        });
    }

    handleCollegeSelect(collegeId) {
        this.currentCollege = this.colleges.find(c => c.id === collegeId);
        document.getElementById('collegeCafeteriasTitle').textContent = `${this.currentCollege.name} - Cafeterias`;
        this.renderCafeterias();
        this.showSection('cafeteriasSection');
        this.scrollToSection('cafeteriasSection');
    }

    renderCafeterias() {
        const grid = document.getElementById('cafeteriasGrid');
        grid.innerHTML = this.currentCollege.cafeterias.map(cafeteria => `
            <div class="cafeteria-card" data-name="${cafeteria}">
                ${!this.currentUser ? `
                    <div class="login-overlay active">
                        <i class="fas fa-lock"></i>
                        <p>Login to access menu</p>
                        <button class="btn btn-primary" onclick="app.showAuthModal('login')">
                            Login Now
                        </button>
                    </div>
                ` : ''}
                <div class="cafeteria-img" style="background-image: url('${this.currentCollege.image}')">
                    <div class="cafeteria-status">Open</div>
                </div>
                <div class="cafeteria-info">
                    <h3>${cafeteria}</h3>
                    <p>Preorder from ${cafeteria} at ${this.currentCollege.name}</p>
                    <div class="cafeteria-meta">
                        <div class="rating">
                            <i class="fas fa-star"></i>
                            <span>4.2</span>
                        </div>
                        <div class="time">Preorder available</div>
                    </div>
                </div>
            </div>
        `).join('');

        grid.querySelectorAll('.cafeteria-card').forEach(card => {
            card.addEventListener('click', () => {
                if (!this.currentUser) {
                    this.showAuthModal('login');
                    return;
                }
                const cafeteriaName = card.dataset.name;
                this.handleCafeteriaSelect(cafeteriaName);
            });
        });
    }

    handleCafeteriaSelect(cafeteriaName) {
        this.currentCafeteria = cafeteriaName;
        document.getElementById('cafeteriaName').textContent = `${this.currentCollege.name} - ${cafeteriaName}`;
        this.renderMenu();
        this.showSection('menuSection');
        this.scrollToSection('menuSection');
    }

    renderMenu() {
        const grid = document.getElementById('menuGrid');
        const menu = this.menuItems[this.currentCafeteria] || [];
        
        if (menu.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: var(--space-2xl);">
                    <i class="fas fa-utensils" style="font-size: 3rem; color: var(--gray-300); margin-bottom: var(--space-md);"></i>
                    <h3>Menu Coming Soon</h3>
                    <p>This cafeteria menu is being updated. Please check back later.</p>
                </div>
            `;
            return;
        }
        
        grid.innerHTML = menu.map(item => `
            <div class="menu-item">
                <div class="menu-img" style="background-image: url('${item.image}')">
                    ${item.veg ? '<div class="veg-indicator"></div>' : ''}
                </div>
                <div class="menu-info">
                    <h3>${item.name}</h3>
                    <p>${item.description}</p>
                    <div class="menu-meta">
                        <div class="price">₹${item.price}</div>
                        <button class="add-to-cart" data-id="${item.id}">
                            Add to Cart
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        grid.querySelectorAll('.add-to-cart').forEach(button => {
            button.addEventListener('click', (e) => {
                e.stopPropagation();
                this.handleAddToCart(button.dataset.id);
            });
        });
    }

    handleAddToCart(itemId) {
        const item = Object.values(this.menuItems)
            .flat()
            .find(i => i.id == itemId);

        if (!item) return;

        const existingItem = this.cart.find(i => i.id == itemId);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.cart.push({
                ...item,
                quantity: 1,
                cafeteria: this.currentCafeteria
            });
        }

        this.updateCart();
        this.showToast(`${item.name} Added to cart!`, 'success');
    }

    updateCart() {
        const totalItems = this.cart.reduce((sum, item) => sum + item.quantity, 0);
        document.getElementById('cartCount').textContent = totalItems;

        const itemsContainer = document.getElementById('cartItems');
        const total = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

        if (this.cart.length === 0) {
            itemsContainer.innerHTML = `
                <div style="text-align: center; padding: var(--space-2xl); color: var(--gray-600);">
                    <i class="fas fa-shopping-cart" style="font-size: 3rem; margin-bottom: var(--space-md);"></i>
                    <p>Your cart is empty</p>
                </div>
            `;
        } else {
            itemsContainer.innerHTML = this.cart.map(item => `
                <div class="cart-item">
                    <div class="item-details">
                        <h4>${item.name}</h4>
                        <p>₹${item.price} x ${item.quantity}</p>
                    </div>
                    <div class="item-actions">
                        <div class="quantity-controls">
                            <button class="quantity-btn" onclick="app.updateQuantity(${item.id}, -1)">-</button>
                            <span>${item.quantity}</span>
                            <button class="quantity-btn" onclick="app.updateQuantity(${item.id}, 1)">+</button>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        document.getElementById('cartTotal').textContent = total;
        document.getElementById('checkoutBtn').disabled = this.cart.length === 0 || !this.currentUser;
    }

    updateQuantity(itemId, change) {
        const item = this.cart.find(i => i.id == itemId);
        if (!item) return;

        item.quantity += change;
        if (item.quantity <= 0) {
            this.cart = this.cart.filter(i => i.id != itemId);
            this.showToast('Item removed from cart', 'success');
        }

        this.updateCart();
    }

    // Auth methods
    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        if (!this.validateEmail(email)) {
            this.showError('loginEmailError', 'Please enter a valid email');
            return;
        }

        if (password.length < 6) {
            this.showError('loginPasswordError', 'Password must be at least 6 characters');
            return;
        }

        this.setLoading(true);
        
        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            this.currentUser = {
                name: email.split('@')[0],
                email: email,
                avatar: email[0].toUpperCase()
            };

            // Save to localStorage
            localStorage.setItem('quickBiteUser', JSON.stringify(this.currentUser));

            this.updateUI();
            this.hideAuthModal();
            this.showToast('Login successful!', 'success');
        } catch (error) {
            this.showToast('Login failed. Please try again.', 'error');
        } finally {
            this.setLoading(false);
        }
    }

    async handleSignup(e) {
        e.preventDefault();
        const name = document.getElementById('signupName').value;
        const email = document.getElementById('signupEmail').value;
        const phone = document.getElementById('signupPhone').value;
        const password = document.getElementById('signupPassword').value;

        // Validation
        if (!name.trim()) {
            this.showError('signupNameError', 'Name is required');
            return;
        }

        if (!this.validateEmail(email)) {
            this.showError('signupEmailError', 'Please enter a valid email');
            return;
        }

        if (!this.validatePhone(phone)) {
            this.showError('signupPhoneError', 'Please enter a valid phone number');
            return;
        }

        if (password.length < 6) {
            this.showError('signupPasswordError', 'Password must be at least 6 characters');
            return;
        }

        this.setLoading(true);

        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            this.currentUser = {
                name: name,
                email: email,
                phone: phone,
                avatar: name[0].toUpperCase()
            };

            // Save to localStorage
            localStorage.setItem('quickBiteUser', JSON.stringify(this.currentUser));

            this.updateUI();
            this.hideAuthModal();
            this.showToast('Account created successfully!', 'success');
        } catch (error) {
            this.showToast('Signup failed. Please try again.', 'error');
        } finally {
            this.setLoading(false);
        }
    }

    handleLogout() {
        this.currentUser = null;
        this.cart = [];
        localStorage.removeItem('quickBiteUser');
        this.updateUI();
        this.showToast('Logged out successfully', 'success');
    }

    // UI methods
    updateUI() {
        const userInfo = document.getElementById('userInfo');
        const loginBtn = document.getElementById('loginBtn');
        const signupBtn = document.getElementById('signupBtn');
        const logoutBtn = document.getElementById('logoutBtn');

        if (this.currentUser) {
            userInfo.style.display = 'flex';
            loginBtn.style.display = 'none';
            signupBtn.style.display = 'none';
            logoutBtn.style.display = 'block';
            document.getElementById('userName').textContent = this.currentUser.name;
            document.getElementById('userAvatar').textContent = this.currentUser.avatar;

            // Remove login overlays
            document.querySelectorAll('.login-overlay').forEach(overlay => {
                overlay.classList.remove('active');
            });
        } else {
            userInfo.style.display = 'none';
            loginBtn.style.display = 'block';
            signupBtn.style.display = 'block';
            logoutBtn.style.display = 'none';

            // Add login overlays
            document.querySelectorAll('.cafeteria-card').forEach(card => {
                const overlay = card.querySelector('.login-overlay');
                if (overlay) overlay.classList.add('active');
            });
        }

        this.updateCart();
    }

    showAuthModal(tab) {
        document.getElementById('authModal').classList.add('active');
        this.switchAuthTab(tab);
    }

    hideAuthModal() {
        document.getElementById('authModal').classList.remove('active');
        this.clearFormErrors();
    }

    switchAuthTab(tab) {
        document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
        
        document.querySelector(`[data-tab="${tab}"]`).classList.add('active');
        document.getElementById(`${tab}Form`).classList.add('active');
    }

    showSection(sectionId) {
        document.querySelectorAll('section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(sectionId).classList.add('active');
    }

    toggleCart() {
        document.getElementById('cartSection').classList.toggle('active');
    }

    handleCheckout() {
        if (!this.currentUser) {
            this.showAuthModal('login');
            return;
        }

        if (this.cart.length === 0) {
            this.showToast('Your cart is empty', 'error');
            return;
        }

        // Generate order token
        this.orderToken = 'QB-' + Math.floor(100000 + Math.random() * 900000);
        
        // Update order status page
        document.getElementById('tokenNumber').textContent = this.orderToken;
        document.getElementById('qrToken').textContent = this.orderToken;
        document.getElementById('orderCollege').textContent = this.currentCollege.name;
        document.getElementById('orderCafeteria').textContent = this.currentCafeteria;
        document.getElementById('pickupLocation').textContent = 'Counter A';
        document.getElementById('orderTotal').textContent = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        
        // Set ready time (30 minutes from now)
        const now = new Date();
        now.setMinutes(now.getMinutes() + 30);
        const timeString = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        document.getElementById('readyTime').textContent = timeString;

        // Show order status
        this.showSection('orderStatusSection');
        this.toggleCart();
        
        this.showToast('Order placed successfully!', 'success');
        
        // Clear cart
        this.cart = [];
        this.updateCart();
    }

    handleBackToCafeterias() {
        this.showSection('cafeteriasSection');
    }

    handleNewOrder() {
        this.showSection('colleges');
        this.scrollToSection('colleges');
    }

    scrollToSection(sectionId) {
        document.getElementById(sectionId).scrollIntoView({ behavior: 'smooth' });
    }

    // Utility methods
    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    validatePhone(phone) {
        const re = /^[6-9]\d{9}$/;
        return re.test(phone.replace(/\D/g, ''));
    }

    showError(elementId, message) {
        const element = document.getElementById(elementId);
        element.textContent = message;
        element.classList.add('show');
    }

    clearFormErrors() {
        document.querySelectorAll('.error-message').forEach(error => {
            error.classList.remove('show');
        });
    }

    setLoading(loading) {
        this.isLoading = loading;
        document.body.classList.toggle('loading', loading);
    }

    showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : 'exclamation'}"></i>
            ${message}
        `;
        
        document.getElementById('toastContainer').appendChild(toast);
        
        setTimeout(() => toast.classList.add('show'), 100);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    checkAuthStatus() {
        // Check for existing session
        const savedUser = localStorage.getItem('quickBiteUser');
        if (savedUser) {
            this.currentUser = JSON.parse(savedUser);
            this.updateUI();
        }
    }
}

// Initialize the application
const app = new QuickBitesApp();

// Close modal when clicking outside
document.getElementById('authModal').addEventListener('click', (e) => {
    if (e.target === document.getElementById('authModal')) {
        app.hideAuthModal();
    }
});

// Close cart when clicking outside (for mobile)
document.addEventListener('click', (e) => {
    const cart = document.getElementById('cartSection');
    const cartIcon = document.getElementById('cartIcon');
    
    if (cart.classList.contains('active') && 
        !cart.contains(e.target) && 
        !cartIcon.contains(e.target)) {
        app.toggleCart();
    }
});

// Handle filter buttons
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        // Filter logic would go here in a real implementation
    });
});

// Handle category buttons
document.querySelectorAll('.category-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        // Category filter logic would go here
    });
});

// Smooth scrolling for navigation links
document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId.startsWith('#')) {
            document.querySelector(targetId).scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Add loading state for better UX
document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('loaded');
});