/** 
 * Admin Frontend Logic
 * Handles API calls, JWT management, and dynamic rendering.
 */

const API_BASE = 'http://localhost:5000/api'; // Update for production

const AdminApp = {
    // Auth Management
    setToken(token) {
        localStorage.setItem('cv_admin_token', token);
    },

    getToken() {
        return localStorage.getItem('cv_admin_token');
    },

    logout() {
        localStorage.removeItem('cv_admin_token');
        window.location.href = 'login.html';
    },

    isAuthenticated() {
        const token = this.getToken();
        if (!token) return false;

        // Basic check for JWT expiration if needed
        // For now, just check presence
        return true;
    },

    // API Wrapper
    async request(endpoint, options = {}) {
        const url = `${API_BASE}${endpoint}`;
        const token = this.getToken();

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, { ...options, headers });

            if (response.status === 401) {
                this.logout();
                return null;
            }

            return await response.json();
        } catch (error) {
            console.error('API Request Error:', error);
            return { error: 'Network error' };
        }
    },

    // UI Helpers
    showToast(message, type = 'success') {
        // Implementation for a premium toast notification
        console.log(`[${type}] ${message}`);
    }
};

// Check auth on load for protected pages
if (window.location.pathname.includes('dashboard.html') ||
    window.location.pathname.includes('portfolio.html') &&
    !window.location.pathname.includes('login.html')) {
    if (!AdminApp.isAuthenticated()) {
        window.location.href = 'login.html';
    }
}
