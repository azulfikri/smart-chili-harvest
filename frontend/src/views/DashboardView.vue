<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '@/config'

const router = useRouter()

// Sync dengan schema Backend JSON
interface HarvestSession {
  id: number;
  session_name: string;
  hrs: number | null;
  harvest_status: string | null;
  created_at: string | null;
}

// State
const isLoading = ref(true)
const isCreatingSession = ref(false)
const latestSession = ref<HarvestSession | null>(null)
const currentDate = ref('')

// Mock Data (Cuaca & Kelembaban - belum ada di backend)
const mockWeather = ref({ label: 'Cerah', temp: '31°C' })
const mockHumidity = ref({ value: '65% RH' })

// Format Date (untuk header sapaan)
const formatDate = () => {
  const options: Intl.DateTimeFormatOptions = { 
    weekday: 'long', 
    day: 'numeric',
    month: 'long', 
    year: 'numeric' 
  }
  currentDate.value = new Date().toLocaleDateString('id-ID', options)
}

// Format tanggal sesi untuk card (misal: "2 Juli")
const formattedSessionDate = computed(() => {
  if (!latestSession.value?.created_at) return '-'
  let dateStr = latestSession.value.created_at
  if (!dateStr.includes('T')) {
    dateStr = dateStr.replace(' ', 'T') + 'Z'
  } else if (!dateStr.endsWith('Z')) {
    dateStr += 'Z'
  }
  const date = new Date(dateStr)
  
  // Gunakan timezone Jakarta agar hari tidak mundur/maju karena beda zona
  const day = date.toLocaleDateString('id-ID', { timeZone: 'Asia/Jakarta', day: 'numeric' })
  const month = date.toLocaleDateString('id-ID', { timeZone: 'Asia/Jakarta', month: 'long' })
  return `${day} ${month}`
})

// HRS Score display text (misal: "82% Optimal")
const hrsScoreText = computed(() => {
  if (!latestSession.value || latestSession.value.hrs === null || latestSession.value.hrs === undefined) {
    return { score: '-', label: '', colorClass: 'text-slate-400' }
  }
  const score = Number(latestSession.value.hrs).toFixed(0)
  const hrs = latestSession.value.hrs
  let label = 'Rendah'
  let colorClass = 'text-rose-600'
  if (hrs >= 80) { label = 'Optimal'; colorClass = 'text-emerald-700' }
  else if (hrs >= 60) { label = 'Menengah'; colorClass = 'text-amber-600' }
  return { score: `${score}%`, label, colorClass }
})

// Fetch Last Session
const fetchLatestSession = async () => {
  try {
    isLoading.value = true
    const response = await axios.get(`${API_BASE_URL}/api/sessions`)
    
    if (response.data && response.data.length > 0) {
      console.log("Data Sesi Terakhir di Dashboard:", response.data[0])
      latestSession.value = response.data[0]
    } else {
      latestSession.value = null
    }
  } catch (error) {
    console.error('Error fetching sessions:', error)
    latestSession.value = null
  } finally {
    isLoading.value = false
  }
}

// Start New Session
const startNewSession = async () => {
  try {
    isCreatingSession.value = true
    const response = await axios.post(`${API_BASE_URL}/api/sessions`)
    const newSession = response.data
    
    if (newSession && newSession.id) {
      localStorage.setItem('activeSessionId', newSession.id.toString())
      router.push('/detection')
    }
  } catch (error) {
    console.error('Error creating new session:', error)
    alert('Gagal memulai sesi baru. Pastikan backend berjalan.')
  } finally {
    isCreatingSession.value = false
  }
}

onMounted(() => {
  formatDate()
  fetchLatestSession()
})
</script>

<template>
  <div class="px-5 pb-6 flex flex-col min-h-[calc(100vh-8.5rem)]">
    
    <!-- Header Sapaan -->
    <header class="mb-6 mt-1">
      <h1 class="text-[26px] font-bold text-slate-900 tracking-tight leading-tight">Halo, Pak Tani</h1>
      <div class="flex items-center gap-2 mt-1.5">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 text-slate-400">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
        </svg>
        <span class="text-sm text-slate-500">{{ currentDate }}</span>
      </div>
    </header>

    <!-- Card Pemindaian Terakhir (Sesuai Mockup) -->
    <div class="bg-white rounded-2xl shadow-sm border border-slate-100/60 p-5 mb-4">
      
      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center items-center py-10">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600"></div>
      </div>
      
      <!-- Empty State -->
      <div v-else-if="!latestSession" class="flex flex-col items-center justify-center text-center py-8">
        <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-3">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8 text-slate-300">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m3.75 9v6m3-3H9m1.5-12H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
          </svg>
        </div>
        <p class="text-slate-400 text-sm font-medium">Belum ada riwayat pengamatan.</p>
      </div>
      
      <!-- Data Terisi -->
      <div v-else>
        <!-- Baris Atas: Label + Badge -->
        <div class="flex justify-between items-start mb-1">
          <div>
            <p class="text-[11px] font-semibold text-slate-400 uppercase tracking-widest">Pemindaian Terakhir</p>
            <p class="text-2xl font-bold text-slate-900 mt-1">{{ formattedSessionDate }}</p>
          </div>
          <!-- Soft Pill Badge -->
          <span 
            class="px-3 py-1.5 rounded-full text-[11px] font-semibold tracking-wide border mt-1"
            :class="{
              'bg-emerald-600 text-white border-emerald-600': latestSession.harvest_status === 'Siap Panen' || ((latestSession.hrs ?? 0) >= 80),
              'bg-amber-500 text-white border-amber-500': latestSession.harvest_status === 'Hampir Siap Panen' || ((latestSession.hrs ?? 0) >= 60 && (latestSession.hrs ?? 0) < 80),
              'bg-rose-500 text-white border-rose-500': latestSession.harvest_status === 'Belum Siap Panen' || ((latestSession.hrs ?? 0) < 60)
            }"
          >
            {{ latestSession.harvest_status || 'Belum Siap Panen' }}
          </span>
        </div>
        
        <!-- Garis Pemisah -->
        <div class="border-b border-slate-100 my-3"></div>
        
        <!-- Baris Bawah: Skor HRS + Icon Badge -->
        <div class="flex justify-between items-center">
          <div>
            <p class="text-[11px] font-semibold text-slate-400 uppercase tracking-widest mb-1">Skor HRS</p>
            <div class="flex items-baseline gap-2">
              <span class="text-3xl font-extrabold tracking-tight" :class="hrsScoreText.colorClass">{{ hrsScoreText.score }}</span>
              <span class="text-sm font-medium text-slate-500">{{ hrsScoreText.label }}</span>
            </div>
          </div>
          <!-- Ikon Daun Badge -->
          <div class="bg-emerald-50 text-emerald-600 rounded-full p-3">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
              <path fill-rule="evenodd" d="M12.963 2.286a.75.75 0 00-1.071-.136 9.742 9.742 0 00-3.539 6.177A7.547 7.547 0 016.648 6.61a.75.75 0 00-1.152.082A9 9 0 1015.68 4.534a7.46 7.46 0 01-2.717-2.248zM15.75 14.25a3.75 3.75 0 11-7.313-1.172c.628.465 1.35.81 2.133 1a5.99 5.99 0 011.925-3.545 3.75 3.75 0 013.255 3.717z" clip-rule="evenodd" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Grid Cards (Cuaca & Kelembaban) -->
    <div class="grid grid-cols-2 gap-3 mb-4">
      <!-- Card Cuaca -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100/60 p-4">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-7 h-7 text-amber-500 mb-2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
        </svg>
        <p class="text-sm font-semibold text-slate-700">Cuaca</p>
        <p class="text-base font-bold text-slate-900 mt-0.5">{{ mockWeather.label }}, {{ mockWeather.temp }}</p>
      </div>
      <!-- Card Kelembaban -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100/60 p-4">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-7 h-7 text-rose-400 mb-2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 3.75c-4.97 4.97-7.5 8.22-7.5 11.25a7.5 7.5 0 0015 0c0-3.03-2.53-6.28-7.5-11.25z" />
        </svg>
        <p class="text-sm font-semibold text-slate-700">Kelembaban</p>
        <p class="text-base font-bold text-slate-900 mt-0.5">{{ mockHumidity.value }}</p>
      </div>
    </div>

    <!-- Banner Gambar Kondisi Lahan -->
    <div class="rounded-2xl overflow-hidden shadow-sm relative mb-6">
      <img 
        src="/images/chili-farm-banner.png" 
        alt="Kondisi lahan pertanian cabai" 
        class="w-full h-44 object-cover"
      />
      <!-- Overlay Gradasi -->
      <div class="absolute inset-0 bg-linear-to-t from-black/60 via-black/10 to-transparent"></div>
      <!-- Teks Overlay -->
      <p class="absolute bottom-3 left-4 text-white font-semibold text-sm tracking-wide">Sawah Blok A - Kondisi Terkini</p>
    </div>

    <!-- Spacer untuk mendorong tombol ke bawah -->
    <div class="grow"></div>

    <!-- Action Button (CTA Forest Green) -->
    <div class="mb-2">
      <button 
        @click="startNewSession"
        :disabled="isCreatingSession"
        class="w-full bg-[#065f46] hover:bg-[#064e3b] active:bg-[#053c2e] text-white font-semibold py-4 px-6 rounded-2xl shadow-lg shadow-emerald-900/15 transition-all duration-200 active:scale-[0.98] flex justify-center items-center gap-3 cursor-pointer disabled:opacity-70 disabled:cursor-not-allowed"
      >
        <span v-if="isCreatingSession" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white/80"></span>
        <!-- Ikon Scan/Focus -->
        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 3.75H6A2.25 2.25 0 003.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0120.25 6v1.5m0 9V18A2.25 2.25 0 0118 20.25h-1.5m-9 0H6A2.25 2.25 0 013.75 18v-1.5M12 9v6m3-3H9" />
        </svg>
        <span class="text-sm tracking-wide">{{ isCreatingSession ? 'Mempersiapkan...' : 'Mulai Pengamatan Baru' }}</span>
      </button>
    </div>
  </div>
</template>
