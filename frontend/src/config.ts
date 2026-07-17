/**
 * Konfigurasi API Terpusat
 * 
 * Prioritas pembacaan URL:
 * 1. Environment variable VITE_API_BASE_URL (dari Vercel / .env file)
 * 2. Fallback default ke VPS production
 * 
 * Cara set di Vercel:
 *   Settings → Environment Variables → VITE_API_BASE_URL = http://210.79.190.219:8000
 * 
 * Cara set lokal:
 *   Buat file .env.local di folder frontend/ dengan isi:
 *   VITE_API_BASE_URL=http://127.0.0.1:8000
 */

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://210.79.190.219:8000'
