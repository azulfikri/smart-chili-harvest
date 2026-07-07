<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const sessionId = route.params.id

// Strict Interface for type safety
interface SessionDetail {
  id: number;
  session_name: string;
  status: string;
  sample_quality: number | null;
  hrs: number;
  harvest_status: string;
  estimated_shelf_life: number;
  total_semi_ripe: number;
  total_nearly_ripe: number;
  total_ripe: number;
  recommendation: string;
  created_at: string;
  completed_at: string;
  detections: Array<{
    id: number;
    original_image: string;
    processed_image: string;
    semi_ripe_count: number;
    nearly_ripe_count: number;
    ripe_count: number;
    average_confidence: number;
  }>;  
}

const session = ref<SessionDetail | null>(null)
const isLoading = ref(true)

onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/sessions/${sessionId}`)
    session.value = response.data
  } catch (error) {
    console.error('Error fetching session details:', error)
    alert('Gagal memuat detail sesi.')
  } finally {
    isLoading.value = false
  }
})

// Dynamic classes computed based on HRS score
const gaugeStrokeClass = computed(() => {
  if (!session.value) return 'text-slate-300'
  if (session.value.hrs >= 80) return 'text-emerald-500'
  if (session.value.hrs >= 60) return 'text-amber-500'
  return 'text-rose-500'
})

const gaugeTextClass = computed(() => {
  if (!session.value) return 'text-slate-400'
  if (session.value.hrs >= 80) return 'text-emerald-700'
  if (session.value.hrs >= 60) return 'text-amber-700'
  return 'text-rose-700'
})

const gaugeSubText = computed(() => {
  if (!session.value) return ''
  if (session.value.hrs >= 80) return 'Optimal'
  if (session.value.hrs >= 60) return 'Perlu Pemantauan'
  return 'Belum Optimal'
})
</script>

<template>
  <div class="flex flex-col min-h-[calc(100vh-5rem)] bg-slate-50 pb-6">
    <!-- TOP NAVIGATION BAR -->
    <header class="bg-white border-b border-slate-100 px-4 py-3 flex items-center justify-center sticky top-0 z-40 shadow-sm relative">
      <button 
        @click="router.push('/history')" 
        class="absolute left-4 p-2 -ml-2 rounded-full hover:bg-slate-100 active:bg-slate-200 transition-colors text-slate-700"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
        </svg>
      </button>
      <h1 class="text-base font-bold text-slate-800">Detail Pengamatan</h1>
    </header>

    <!-- Loading State -->
    <div v-if="isLoading" class="grow flex justify-center items-center">
      <div class="animate-spin rounded-full h-10 w-10 border-2 border-emerald-200 border-t-emerald-600"></div>
    </div>
    
    <!-- Detail Content -->
    <div v-else-if="session" class="grow flex flex-col gap-6 px-4 pt-6">
      
      <!-- Header Info -->
      <div class="text-center">
        <h2 class="text-lg font-bold text-slate-800 tracking-tight">{{ session.session_name }}</h2>
        <p class="text-[10px] font-medium text-slate-400 mt-1 uppercase tracking-widest">{{ new Date(session.completed_at).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' }) }}</p>
      </div>
      
      <!-- Premium Score Gauge Ring (Visualisasi Utama) -->
      <div class="flex justify-center my-2">
        <div class="relative w-56 h-56 flex flex-col items-center justify-center bg-white rounded-full shadow-sm">
          <!-- Background SVG Ring -->
          <svg class="absolute inset-0 w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            <!-- Background circle (gray) -->
            <circle cx="50" cy="50" r="44" fill="none" stroke="currentColor" stroke-width="8" class="text-slate-100" />
            <!-- Foreground circle (colored) -->
            <circle cx="50" cy="50" r="44" fill="none" stroke="currentColor" stroke-width="8" 
                    stroke-linecap="round"
                    :class="gaugeStrokeClass"
                    :stroke-dasharray="2 * Math.PI * 44"
                    :stroke-dashoffset="(2 * Math.PI * 44) - ((2 * Math.PI * 44) * (session.hrs / 100))"
                    class="transition-all duration-1000 ease-out" />
          </svg>
          
          <!-- Inner Text Content -->
          <div class="relative z-10 flex flex-col items-center" :class="gaugeTextClass">
            <span class="text-[10px] font-bold uppercase tracking-widest mb-1 opacity-70">{{ session.harvest_status }}</span>
            <div class="flex items-start">
              <span class="text-6xl font-black tracking-tighter">{{ Number(session.hrs).toFixed(1) }}</span>
              <span class="text-2xl font-bold mt-2">%</span>
            </div>
            <span class="text-xs font-medium tracking-wide uppercase mt-1 opacity-80">{{ gaugeSubText }}</span>
          </div>
        </div>
      </div>
      
      <!-- Grid Akumulasi Total Buah -->
      <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-100">
        <h3 class="text-[10px] font-semibold text-slate-400 mb-4 uppercase tracking-wider text-center">Akumulasi Total Objek</h3>
        <div class="grid grid-cols-3 divide-x divide-slate-100">
          <div class="flex flex-col items-center py-2">
            <span class="text-slate-900 font-extrabold text-xl">{{ session.total_semi_ripe }}</span>
            <span class="text-[10px] font-medium text-slate-500 uppercase tracking-wider mt-1">Semi-ripe</span>
          </div>
          <div class="flex flex-col items-center py-2">
            <span class="text-slate-900 font-extrabold text-xl">{{ session.total_nearly_ripe }}</span>
            <span class="text-[10px] font-medium text-slate-500 uppercase tracking-wider mt-1">Nearly-ripe</span>
          </div>
          <div class="flex flex-col items-center py-2">
            <span class="text-slate-900 font-extrabold text-xl">{{ session.total_ripe }}</span>
            <span class="text-[10px] font-medium text-slate-500 uppercase tracking-wider mt-1">Ripe</span>
          </div>
        </div>
        <div class="mt-4 pt-4 border-t border-slate-100 flex justify-between items-center px-2">
          <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Total Terdeteksi</span>
          <span class="text-lg font-black text-slate-800">{{ session.total_semi_ripe + session.total_nearly_ripe + session.total_ripe }}</span>
        </div>
      </div>
      
      <!-- Kotak Rekomendasi Pascapanen & Daya Simpan -->
      <div class="bg-emerald-950 text-emerald-50 rounded-2xl p-5 shadow-lg relative overflow-hidden">
        <!-- Dekorasi Background -->
        <div class="absolute -right-8 -top-8 w-32 h-32 bg-emerald-900/50 rounded-full blur-2xl"></div>
        
        <div class="flex items-start gap-3 relative z-10">
          <div class="mt-1 bg-emerald-900/50 p-2 rounded-xl text-emerald-400">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <h3 class="text-sm font-bold text-emerald-100 mb-1.5 uppercase tracking-wide">Rekomendasi Pascapanen</h3>
            <p class="text-sm text-emerald-200/90 leading-relaxed font-medium">{{ session.recommendation }}</p>
          </div>
        </div>
        
        <div class="mt-5 pt-4 border-t border-emerald-800/50 relative z-10 flex items-center justify-between">
          <div class="flex items-center gap-2 text-emerald-300">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
            </svg>
            <span class="text-xs font-semibold uppercase tracking-widest">Estimasi Daya Simpan</span>
          </div>
          <span class="text-sm font-bold text-white">{{ session.estimated_shelf_life }} Hari</span>
        </div>
      </div>
      
    </div>
    
    <div v-else class="grow flex flex-col justify-center items-center text-center">
      <p class="text-slate-500 font-medium">Data pengamatan tidak ditemukan.</p>
    </div>
    
    <!-- Button Action Footer -->
    <div class="px-4 mt-8" v-if="session">
      <button 
        @click="router.push('/dashboard')"
        class="w-full bg-white hover:bg-slate-50 active:bg-slate-100 text-slate-700 font-bold py-3.5 px-6 rounded-xl border-2 border-slate-200 shadow-sm transition-all flex justify-center items-center gap-2"
      >
        Kembali ke Dashboard
      </button>
    </div>
  </div>
</template>
