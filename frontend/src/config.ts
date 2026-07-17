/**
 * Konfigurasi API Terpusat
 * 
 * Mode operasi:
 * - Vercel (production): VITE_API_BASE_URL kosong → request jadi relative (/api/...)
 *   → Vercel rewrites proxy ke VPS backend
 * - Development lokal: VITE_API_BASE_URL = http://210.79.190.219:8000
 *   → request langsung ke VPS
 */

const envUrl = import.meta.env.VITE_API_BASE_URL

// Jika aplikasi di-build untuk production (Vercel), paksa gunakan relative path ('') 
// agar request dilewatkan melalui Vercel rewrites proxy (menghindari error HTTPS ke HTTP).
// Jika di development lokal, gunakan nilai dari .env.development.
export const API_BASE_URL = import.meta.env.PROD ? '' : (envUrl || 'http://210.79.190.219:8000')
