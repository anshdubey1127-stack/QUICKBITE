// API Configuration and Helper Functions
const API_BASE_URL = 'http://localhost:5000/api';

// Store authentication token
let authToken = localStorage.getItem('token') || null;

/**
 * Set Authorization Header
 */
function getAuthHeader() {
    return authToken ? {
        'Authorization': `Bearer ${authToken}`
    } : {};
}

/**
 * Make API Request
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
        ...options.headers
    };

    try {
        const response = await fetch(url, {
            ...options,
            headers
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'API Error');
        }

        return data;
    } catch (error) {
        console.error(`API Error (${endpoint}):`, error);
        throw error;
    }
}

/**
 * Authentication API Functions
 */
const AuthAPI = {
    signup: async (userData) => {
        const response = await apiRequest('/auth/signup', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
        if (response.success) {
            authToken = response.token;
            localStorage.setItem('token', authToken);
            localStorage.setItem('user', JSON.stringify(response.user));
        }
        return response;
    },

    login: async (email, password) => {
        const response = await apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        if (response.success) {
            authToken = response.token;
            localStorage.setItem('token', authToken);
            localStorage.setItem('user', JSON.stringify(response.user));
        }
        return response;
    },

    verify: async () => {
        try {
            return await apiRequest('/auth/verify', {
                method: 'POST'
            });
        } catch (error) {
            authToken = null;
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            throw error;
        }
    },

    logout: () => {
        authToken = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    },

    getCurrentUser: () => {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    }
};

/**
 * College API Functions
 */
const CollegeAPI = {
    getAll: async () => {
        const response = await apiRequest('/colleges');
        return response.data;
    },

    getById: async (id) => {
        const response = await apiRequest(`/colleges/${id}`);
        return response.data;
    },

    create: async (collegeData) => {
        const response = await apiRequest('/colleges', {
            method: 'POST',
            body: JSON.stringify(collegeData)
        });
        return response.data;
    },

    update: async (id, collegeData) => {
        const response = await apiRequest(`/colleges/${id}`, {
            method: 'PUT',
            body: JSON.stringify(collegeData)
        });
        return response.data;
    }
};

/**
 * Menu API Functions
 */
const MenuAPI = {
    getAll: async (filters = {}) => {
        let url = '/menu';
        const params = new URLSearchParams(filters);
        if (Object.keys(filters).length > 0) {
            url += `?${params.toString()}`;
        }
        const response = await apiRequest(url);
        return response.data;
    },

    getById: async (id) => {
        const response = await apiRequest(`/menu/${id}`);
        return response.data;
    },

    getByCafeteria: async (cafeteria) => {
        return MenuAPI.getAll({ cafeteria });
    },

    getByCategory: async (category) => {
        return MenuAPI.getAll({ category });
    },

    getVegetarian: async () => {
        return MenuAPI.getAll({ veg: true });
    },

    create: async (itemData) => {
        const response = await apiRequest('/menu', {
            method: 'POST',
            body: JSON.stringify(itemData)
        });
        return response.data;
    },

    update: async (id, itemData) => {
        const response = await apiRequest(`/menu/${id}`, {
            method: 'PUT',
            body: JSON.stringify(itemData)
        });
        return response.data;
    }
};

/**
 * Order API Functions
 */
const OrderAPI = {
    create: async (orderData) => {
        const response = await apiRequest('/orders', {
            method: 'POST',
            body: JSON.stringify(orderData)
        });
        return response.data;
    },

    getById: async (id) => {
        const response = await apiRequest(`/orders/${id}`);
        return response.data;
    },

    getUserOrders: async (userId) => {
        const response = await apiRequest(`/orders/user/${userId}`);
        return response.data;
    },

    updateStatus: async (id, status) => {
        const response = await apiRequest(`/orders/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ status })
        });
        return response.data;
    },

    cancel: async (id) => {
        const response = await apiRequest(`/orders/${id}`, {
            method: 'DELETE'
        });
        return response.data;
    }
};

/**
 * Example Usage in Frontend
 */

/*
// Login
async function handleLogin(email, password) {
    try {
        const result = await AuthAPI.login(email, password);
        console.log('Login successful:', result.user);
    } catch (error) {
        console.error('Login failed:', error);
    }
}

// Get all colleges
async function displayColleges() {
    try {
        const colleges = await CollegeAPI.getAll();
        console.log('Colleges:', colleges);
    } catch (error) {
        console.error('Failed to load colleges:', error);
    }
}

// Get menu for specific cafeteria
async function displayMenuItems(cafeteria) {
    try {
        const items = await MenuAPI.getByCafeteria(cafeteria);
        console.log('Menu items:', items);
    } catch (error) {
        console.error('Failed to load menu:', error);
    }
}

// Place an order
async function placeOrder(orderData) {
    try {
        const order = await OrderAPI.create(orderData);
        console.log('Order placed:', order.orderToken);
    } catch (error) {
        console.error('Failed to place order:', error);
    }
}

// Get user's orders
async function getUserOrders(userId) {
    try {
        const orders = await OrderAPI.getUserOrders(userId);
        console.log('User orders:', orders);
    } catch (error) {
        console.error('Failed to load orders:', error);
    }
}
*/

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AuthAPI, CollegeAPI, MenuAPI, OrderAPI, apiRequest };
}
