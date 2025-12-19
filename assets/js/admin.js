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

        const isFormData = options.body instanceof FormData;
        const headers = { ...options.headers };

        if (!isFormData) {
            headers['Content-Type'] = 'application/json';
        }

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        this.showLoader();
        try {
            const response = await fetch(url, { ...options, headers });
            this.hideLoader();

            if (response.status === 401) {
                this.logout();
                return null;
            }

            return await response.json();
        } catch (error) {
            this.hideLoader();
            console.error('API Request Error:', error);
            return { error: 'Network error' };
        }
    },

    // UI Helpers
    showToast(message, type = 'success') {
        console.log(`[${type}] ${message}`);
    },

    showLoader() {
        if (!document.getElementById('global-loader')) {
            const loader = document.createElement('div');
            loader.id = 'global-loader';
            loader.innerHTML = `
                <div class="loader-overlay">
                    <div class="loader-spinner"></div>
                </div>
            `;
            document.body.appendChild(loader);

            if (!document.getElementById('loader-styles')) {
                const style = document.createElement('style');
                style.id = 'loader-styles';
                style.textContent = `
                    .loader-overlay {
                        position: fixed;
                        inset: 0;
                        background: rgba(255, 255, 255, 0.7);
                        backdrop-filter: blur(4px);
                        display: flex;
                        items-center: center;
                        justify-content: center;
                        z-index: 9999;
                        opacity: 0;
                        transition: opacity 0.3s ease;
                        pointer-events: all;
                    }
                    .loader-spinner {
                        width: 48px;
                        height: 48px;
                        border: 5px solid #3b82f6;
                        border-bottom-color: transparent;
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                    }
                    @keyframes spin {
                        to { transform: rotate(360deg); }
                    }
                `;
                document.head.appendChild(style);
            }
        }
        setTimeout(() => document.querySelector('.loader-overlay').style.opacity = '1', 10);
    },

    hideLoader() {
        const overlay = document.querySelector('.loader-overlay');
        if (overlay) {
            overlay.style.opacity = '0';
            setTimeout(() => overlay.remove(), 300);
            const container = document.getElementById('global-loader');
            if (container) setTimeout(() => container.remove(), 300);
        }
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
