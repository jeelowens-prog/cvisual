/**
 * CVisual Public API Client
 * Handles data fetching for the public pages.
 */

const PUBLIC_API_BASE = 'http://localhost:5000/api';

const CVisual = {
    async fetchPortfolio() {
        try {
            this.showLoader();
            const res = await fetch(`${PUBLIC_API_BASE}/portfolio`);
            this.hideLoader();
            return await res.json();
        } catch (e) {
            this.hideLoader();
            console.error('Failed to fetch portfolio:', e);
            return [];
        }
    },

    async submitContact(data) {
        try {
            this.showLoader();
            const res = await fetch(`${PUBLIC_API_BASE}/contact`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            this.hideLoader();
            return await res.json();
        } catch (e) {
            this.hideLoader();
            console.error('Failed to submit contact:', e);
            return { error: 'Network error' };
        }
    },

    async subscribeNewsletter(email) {
        try {
            this.showLoader();
            const res = await fetch(`${PUBLIC_API_BASE}/newsletter`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });
            this.hideLoader();
            return await res.json();
        } catch (e) {
            this.hideLoader();
            console.error('Newsletter sub failed:', e);
            return { error: 'Network error' };
        }
    },

    async fetchServices() {
        try {
            this.showLoader();
            const res = await fetch(`${PUBLIC_API_BASE}/services`);
            this.hideLoader();
            return await res.json();
        } catch (e) {
            this.hideLoader();
            console.error('Failed to fetch services:', e);
            return [];
        }
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
                        background: rgba(0, 0, 0, 0.5);
                        backdrop-filter: blur(4px);
                        display: flex;
                        align-items: center;
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
        setTimeout(() => {
            const overlay = document.querySelector('.loader-overlay');
            if (overlay) overlay.style.opacity = '1';
        }, 10);
    },

    hideLoader() {
        const overlay = document.querySelector('.loader-overlay');
        if (overlay) {
            overlay.style.opacity = '0';
            setTimeout(() => {
                overlay.remove();
                const container = document.getElementById('global-loader');
                if (container) container.remove();
            }, 300);
        }
    }
};
