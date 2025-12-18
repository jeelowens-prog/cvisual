/**
 * CVisual Public API Client
 * Handles data fetching for the public pages.
 */

const PUBLIC_API_BASE = 'http://localhost:5000/api';

const CVisual = {
    async fetchPortfolio() {
        try {
            const res = await fetch(`${PUBLIC_API_BASE}/portfolio`);
            return await res.json();
        } catch (e) {
            console.error('Failed to fetch portfolio:', e);
            return [];
        }
    },

    async submitContact(data) {
        try {
            const res = await fetch(`${PUBLIC_API_BASE}/contact`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            return await res.json();
        } catch (e) {
            console.error('Failed to submit contact:', e);
            return { error: 'Network error' };
        }
    },

    async subscribeNewsletter(email) {
        try {
            const res = await fetch(`${PUBLIC_API_BASE}/newsletter`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });
            return await res.json();
        } catch (e) {
            console.error('Newsletter sub failed:', e);
            return { error: 'Network error' };
        }
    },

    async fetchServices() {
        try {
            const res = await fetch(`${PUBLIC_API_BASE}/services`);
            return await res.json();
        } catch (e) {
            console.error('Failed to fetch services:', e);
            return [];
        }
    }
};
