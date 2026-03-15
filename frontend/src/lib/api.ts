// frontend/src/lib/api.ts

import axios, { AxiosInstance } from 'axios';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api: AxiosInstance = axios.create({
  baseURL: `${BASE_URL}/api/v1`,
  headers: { 'Content-Type': 'application/json' },
});

// Attach JWT token from localStorage on every request
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Redirect to /login on 401
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401 && typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

// ── Auth ──────────────────────────────────────────────────────────────────
export const authApi = {
  register: (data: { email: string; password: string; full_name: string }) =>
    api.post('/users/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/users/login', data),
  me: () => api.get('/users/me'),
};

// ── Clients ──────────────────────────────────────────────────────────────
export const clientsApi = {
  list: (limit = 50, offset = 0) =>
    api.get('/clients', { params: { limit, offset } }),
  create: (data: any) => api.post('/clients', data),
  update: (id: string, data: any) => api.patch(`/clients/${id}`, data),
  delete: (id: string) => api.delete(`/clients/${id}`),
};

// ── Invoices ─────────────────────────────────────────────────────────────
export const invoicesApi = {
  list: (limit = 20, offset = 0) =>
    api.get('/invoices', { params: { limit, offset } }),
  get: (id: string) => api.get(`/invoices/${id}`),
  create: (data: any) => api.post('/invoices', data),
  update: (id: string, data: any) => api.patch(`/invoices/${id}`, data),
};

// ── Payments ─────────────────────────────────────────────────────────────
export const paymentsApi = {
  list: (limit = 20, offset = 0) =>
    api.get('/payments', { params: { limit, offset } }),
  record: (data: any) => api.post('/payments', data),
  forInvoice: (invoiceId: string) =>
    api.get(`/payments/invoice/${invoiceId}`),
};

// ── Dashboard ────────────────────────────────────────────────────────────
export const dashboardApi = {
  get: () => api.get('/dashboard'),
};
