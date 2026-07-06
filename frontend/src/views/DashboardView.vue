<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

interface HarvestSession {
  id: number;
  avg_hrs_score: number | null;
  status: string | null;
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
    const sessions = response.data
    
    if (sessions && sessions.length > 0) {
      // Assuming the backend returns sorted data or we take the first one
      latestSession.value = sessions[0]
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
  <div class="p-6 flex flex-col min-h-[calc(100vh-4rem)]">
    <!-- Header -->
    <header class="mb-8 mt-4">
      <h1 class="text-3xl font-bold text-gray-900">Halo, Pak Tani 👋</h1>
      <p class="text-sm text-gray-500 mt-1">{{ currentDate }}</p>
    </header>

    <!-- Card Pengamatan Terakhir -->
    <section class="grow">
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5">
        <h2 class="text-sm font-semibold text-gray-500 mb-4 uppercase tracking-wider">Pengamatan Terakhir</h2>
        
        <div v-if="isLoading" class="flex justify-center items-center py-6">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
        </div>
        
        <div v-else-if="!latestSession" class="text-center py-6">
          <p class="text-gray-500 italic">Belum ada riwayat pengamatan lahan.</p>
        </div>
        
        <div v-else class="flex flex-col gap-3">
          <div class="flex justify-between items-center">
            <span class="text-gray-700 font-medium">Skor HRS:</span>
            <span class="text-xl font-bold text-gray-900">
              {{ latestSession.avg_hrs_score !== null && latestSession.avg_hrs_score !== undefined ? Number(latestSession.avg_hrs_score).toFixed(1) + '%' : '-' }}
            </span>
          </div>
          
          <div class="flex justify-between items-center mt-2">
            <span class="text-gray-700 font-medium">Status:</span>
            <span 
              class="px-3 py-1 text-xs font-bold rounded-md"
              :class="{
                'bg-green-100 text-green-700': latestSession.status === 'Siap Panen' || ((latestSession.avg_hrs_score ?? 0) >= 80),
                'bg-yellow-100 text-yellow-700': latestSession.status === 'Belum Panen' || (latestSession.avg_hrs_score !== null && latestSession.avg_hrs_score < 80)
              }"
            >
              {{ latestSession.status || ((latestSession.avg_hrs_score ?? 0) >= 80 ? 'Siap Panen' : 'Belum Panen') }}
            </span>
          </div>
          <div class="text-xs text-gray-400 mt-2 text-right">
            Sesi ID: {{ latestSession.id }}
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action (Bottom Area) -->
    <div class="mt-8 mb-6">
      <button 
        @click="startNewSession"
        :disabled="isCreatingSession"
        class="w-full bg-green-600 hover:bg-green-700 active:bg-green-800 text-white font-bold py-4 px-6 rounded-xl shadow-lg transition-all flex justify-center items-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
      >
        <span v-if="isCreatingSession" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span>
        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        {{ isCreatingSession ? 'Memulai...' : 'Mulai Pengamatan Baru' }}
      </button>
    </div>
  </div>
</template>
