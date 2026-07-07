<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// Sync dengan schema Backend JSON yang baru
interface HarvestSession {
  id: number;
  session_name: string;
  hrs: number | null;
  harvest_status: string | null;
}

// State
const isLoading = ref(true)
const isCreatingSession = ref(false)
const latestSession = ref<HarvestSession | null>(null)
const currentDate = ref('')

// Format Date
const formatDate = () => {
  const options: Intl.DateTimeFormatOptions = { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  }
  currentDate.value = new Date().toLocaleDateString('id-ID', options)
}

// Fetch Last Session
const fetchLatestSession = async () => {
  try {
    isLoading.value = true
    const response = await axios.get('http://127.0.0.1:8000/api/sessions')
    
    // Perbaikan Logika Reaktif Vue 3 (.value checking)
    if (response.data && response.data.length > 0) {
      // Trik Debugging (Console Log)
      console.log("Data Sesi Terakhir di Dashboard:", response.data[0])
      
      // Ambil indeks ke-0 sebagai sesi terbaru
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
    const response = await axios.post('http://127.0.0.1:8000/api/sessions')
    const newSession = response.data
    
    if (newSession && newSession.id) {
      // Save session ID to localStorage for use in detection page
      localStorage.setItem('activeSessionId', newSession.id.toString())
      // Navigate to detection page
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
  <div class="p-4 flex flex-col min-h-[calc(100vh-4rem)]">
    <!-- Header -->
    <header class="mb-4 mt-2 px-1">
      <h1 class="text-3xl font-bold text-gray-900">Halo, Pak Tani 👋</h1>
      <p class="text-sm text-gray-500 mt-1">{{ currentDate }}</p>
    </header>

    <!-- Card Pengamatan Terakhir -->
    <section class="grow flex flex-col">
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 mt-1">
        <h2 class="text-sm font-semibold text-gray-500 mb-4 uppercase tracking-wider">Pengamatan Terakhir</h2>
        
        <div v-if="isLoading" class="flex justify-center items-center py-6">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
        </div>
        
        <div v-else-if="!latestSession" class="text-center py-6">
          <p class="text-gray-500 italic text-sm">Belum ada riwayat pengamatan lahan.</p>
        </div>
        
        <div v-else class="flex flex-col gap-3">
          <div class="font-bold text-gray-800 text-[15px] truncate border-b border-gray-50 pb-2 mb-1">
            {{ latestSession.session_name }}
          </div>
          
          <div class="flex justify-between items-center">
            <span class="text-gray-700 font-medium text-sm">Skor HRS:</span>
            <span class="text-xl font-bold text-gray-900">
              {{ latestSession.hrs !== null && latestSession.hrs !== undefined ? Number(latestSession.hrs).toFixed(1) + '%' : '-' }}
            </span>
          </div>
          
          <div class="flex justify-between items-center mt-1">
            <span class="text-gray-700 font-medium text-sm">Status:</span>
            <span 
              class="px-2.5 py-1 text-[10px] font-bold rounded-md uppercase tracking-wide inline-block"
              :class="{
                'bg-green-100 text-green-700': latestSession.harvest_status === 'Siap Panen' || ((latestSession.hrs ?? 0) >= 80),
                'bg-orange-100 text-orange-700': latestSession.harvest_status === 'Hampir Siap Panen' || ((latestSession.hrs ?? 0) >= 60 && (latestSession.hrs ?? 0) < 80),
                'bg-red-100 text-red-700': latestSession.harvest_status === 'Belum Siap Panen' || ((latestSession.hrs ?? 0) < 60)
              }"
            >
              {{ latestSession.harvest_status || 'Belum Siap Panen' }}
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action (Bottom Area) -->
    <div class="mt-6 mb-4">
      <button 
        @click="startNewSession"
        :disabled="isCreatingSession"
        class="w-full bg-green-600 hover:bg-green-700 active:bg-green-800 text-white font-bold py-4 px-6 rounded-xl shadow-lg transition-all flex justify-center items-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
      >
        <span v-if="isCreatingSession" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span>
        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        {{ isCreatingSession ? 'Memulai...' : 'Mulai Pengamatan Baru' }}
      </button>
    </div>
  </div>
</template>
