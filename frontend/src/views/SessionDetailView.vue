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
const gaugeColorClass = computed(() => {
  if (!session.value) return 'text-gray-500 border-gray-300'
  if (session.value.hrs >= 80) return 'text-green-600 border-green-500'
  if (session.value.hrs >= 60) return 'text-orange-500 border-orange-400'
  return 'text-red-600 border-red-500'
})

const gaugeBgClass = computed(() => {
  if (!session.value) return 'bg-gray-50'
  if (session.value.hrs >= 80) return 'bg-green-50'
  if (session.value.hrs >= 60) return 'bg-orange-50'
  return 'bg-red-50'
})
</script>

<template>
  <div class="p-6 flex flex-col min-h-[calc(100vh-4rem)]">
    <!-- Loading State -->
    <div v-if="isLoading" class="grow flex justify-center items-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
    </div>
    
    <!-- Detail Content -->
    <div v-else-if="session" class="grow flex flex-col gap-6">
      
      <!-- Header Info -->
      <div class="text-center mt-2">
        <h1 class="text-2xl font-bold text-gray-800">Hasil Analisis</h1>
        <p class="text-sm text-gray-500 mt-1">{{ session.session_name }}</p>
      </div>
      
      <!-- Ring Score Gauge (Visualisasi Utama) -->
      <div class="flex flex-col items-center justify-center">
        <div 
          class="w-56 h-56 rounded-full flex flex-col items-center justify-center border-14 shadow-inner transition-all duration-500 bg-white"
          :class="gaugeColorClass"
        >
          <span class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Skor HRS</span>
          <span class="text-5xl font-black">{{ Number(session.hrs).toFixed(1) }}<span class="text-2xl">%</span></span>
          <span 
            class="text-sm font-bold mt-2 px-3 py-1 rounded-full" 
            :class="[gaugeColorClass.split(' ')[0], gaugeBgClass]"
          >
            {{ session.harvest_status }}
          </span>
        </div>
      </div>
      
      <!-- Detail Statistik Grid -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mt-2">
        <h2 class="text-sm font-semibold text-gray-500 mb-4 uppercase tracking-wider text-center">Statistik Deteksi AI</h2>
        
        <div class="grid grid-cols-3 gap-3">
          <div class="flex flex-col items-center p-3 bg-yellow-50 rounded-xl border border-yellow-100">
            <span class="text-[10px] text-yellow-600 font-bold uppercase mb-1 text-center">Semi Ripe</span>
            <span class="text-2xl font-black text-yellow-700">{{ session.total_semi_ripe }}</span>
          </div>
          <div class="flex flex-col items-center p-3 bg-orange-50 rounded-xl border border-orange-100">
            <span class="text-[10px] text-orange-600 font-bold uppercase mb-1 text-center">Nearly Ripe</span>
            <span class="text-2xl font-black text-orange-700">{{ session.total_nearly_ripe }}</span>
          </div>
          <div class="flex flex-col items-center p-3 bg-red-50 rounded-xl border border-red-100">
            <span class="text-[10px] text-red-600 font-bold uppercase mb-1 text-center">Ripe</span>
            <span class="text-2xl font-black text-red-700">{{ session.total_ripe }}</span>
          </div>
        </div>
        
        <div class="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center">
          <span class="font-medium text-gray-600">Total Buah Terdeteksi</span>
          <span class="text-xl font-bold text-gray-800">{{ session.total_semi_ripe + session.total_nearly_ripe + session.total_ripe }}</span>
        </div>
      </div>
      
      <!-- Kotak Rekomendasi Pascapanen & Daya Simpan -->
      <div class="bg-blue-50/50 rounded-2xl p-5 border border-blue-100 shadow-sm relative overflow-hidden">
        <!-- Dekorasi Background -->
        <div class="absolute -right-4 -top-4 w-24 h-24 bg-blue-100 rounded-full opacity-50 blur-xl"></div>
        
        <div class="flex items-start gap-3 relative z-10">
          <div class="mt-1 bg-blue-100 p-1.5 rounded-lg text-blue-700">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <h2 class="text-md font-bold text-blue-900 mb-1">Rekomendasi Pascapanen</h2>
            <p class="text-sm text-blue-800/80 leading-relaxed">{{ session.recommendation }}</p>
          </div>
        </div>
        
        <div class="mt-4 pt-4 border-t border-blue-100/50 relative z-10 flex items-center justify-between">
          <div class="flex items-center gap-2 text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
            </svg>
            <span class="text-xs font-semibold uppercase tracking-wide">Estimasi Daya Simpan</span>
          </div>
          <span class="text-sm font-black text-blue-900">{{ session.estimated_shelf_life }} Hari</span>
        </div>
      </div>
    </div>
    
    <div v-else class="grow flex flex-col justify-center items-center text-center">
      <p class="text-gray-500 mb-4">Data sesi tidak ditemukan.</p>
    </div>
    
    <!-- Tombol Kembali ke Dashboard (Call to Action) -->
    <div class="mt-6 mb-2">
      <button 
        @click="router.push('/dashboard')"
        class="w-full bg-gray-900 hover:bg-black active:bg-gray-800 text-white font-bold py-4 px-6 rounded-xl shadow-lg transition-all flex justify-center items-center gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
        </svg>
        Kembali ke Dashboard
      </button>
    </div>
  </div>
</template>
