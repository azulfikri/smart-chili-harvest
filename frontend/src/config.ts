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

// Jika env kosong/undefined → gunakan '' (relative path, untuk Vercel proxy)
// Jika env diisi → gunakan value tersebut (untuk dev lokal)
export const API_BASE_URL = envUrl !== undefined && envUrl !== '' ? envUrl : ''
