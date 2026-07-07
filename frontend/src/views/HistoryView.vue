<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// Interface Type-Safe untuk Data Riwayat
interface SessionHistory {
  id: number;
  session_name: string;
  status: string;
  hrs: number | null;
  harvest_status: string | null;
  created_at: string;
}

const historyList = ref<SessionHistory[]>([])
const isLoading = ref(true)

// Fetch Data dari API
const fetchHistory = async () => {
  isLoading.value = true
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/sessions')
    // Mengamankan jika response bukan array (error handling)
    if (Array.isArray(response.data)) {
      historyList.value = response.data
    }
  } catch (error) {
    console.error('Error fetching history:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchHistory()
})

// Logika Navigasi Detail
const goToDetail = (id: number) => {
  router.push(`/sessions/${id}`)
}

// Logika Hapus (Delete)
const deleteSession = async (id: number, event: Event) => {
  // Cegah bubbling click event (agar klik tombol delete tidak memicu goToDetail pada card wrapper)
  event.stopPropagation()
  
  const isConfirmed = confirm("Apakah Anda yakin ingin menghapus riwayat sesi ini secara permanen?")
  if (!isConfirmed) return
  
  try {
    await axios.delete(`http://127.0.0.1:8000/api/sessions/${id}`)
    
    // Hapus data secara lokal dari state untuk update UI instan tanpa reload browser
    historyList.value = historyList.value.filter(session => session.id !== id)
  } catch (error) {
    console.error('Error deleting session:', error)
    alert('Gagal menghapus riwayat pengamatan.')
  }
}
</script>

<template>
  <div class="flex flex-col min-h-[calc(100vh-4rem)] bg-slate-50 pb-20">
    <!-- Top Header Bar (Konsisten) -->
    <header class="flex items-center justify-center px-4 py-3 bg-white border-b border-emerald-100/50 sticky top-0 z-40">
      <h1 class="text-base font-bold text-slate-800">Riwayat Pengamatan</h1>
    </header>

    <!-- Loading State -->
    <div v-if="isLoading" class="grow flex justify-center items-center">
      <div class="animate-spin rounded-full h-10 w-10 border-2 border-emerald-200 border-t-emerald-600"></div>
    </div>

    <!-- Elegant Empty State -->
    <div v-else-if="historyList.length === 0" class="grow flex flex-col justify-center items-center text-center p-6">
      <div class="w-20 h-20 bg-slate-100 rounded-full flex justify-center items-center mb-4 text-slate-300 shadow-inner">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
          <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
        </svg>
      </div>
      <p class="text-sm font-medium text-slate-400 mt-2">Belum ada riwayat pengamatan lahan.</p>
    </div>

    <!-- List Sesi (Card Item Premium) -->
    <div v-else class="grow flex flex-col px-4 pt-4 pb-6">
      <div 
        v-for="session in historyList" 
        :key="session.id"
        @click="goToDetail(session.id)"
        class="bg-white rounded-2xl p-4 shadow-sm border border-slate-100 mb-4 cursor-pointer hover:border-emerald-200 hover:shadow-md transition-all duration-200 active:scale-[0.99] group flex justify-between items-center relative"
      >
        <!-- Informasi Sesi (Kiri) -->
        <div class="flex flex-col w-full pr-10">
          <h3 class="text-sm font-semibold text-slate-900 mb-1 truncate pr-2">{{ session.session_name }}</h3>
          
          <div class="flex items-center gap-2 mb-3">
            <span class="text-xs font-medium text-slate-400">Skor HRS:</span>
            <span class="text-base font-bold text-emerald-700">{{ session.hrs !== null ? Number(session.hrs).toFixed(1) + '%' : '-' }}</span>
          </div>
          
          <div>
            <!-- Soft Badge Dinamis -->
            <span 
              class="px-2.5 py-1 text-[9px] font-bold rounded-lg uppercase tracking-wider inline-block border"
              :class="{
                'bg-emerald-50 text-emerald-700 border-emerald-150': (session.hrs ?? 0) >= 80,
                'bg-amber-50 text-amber-700 border-amber-150': (session.hrs ?? 0) >= 60 && (session.hrs ?? 0) < 80,
                'bg-rose-50 text-rose-700 border-rose-150': (session.hrs ?? 0) < 60
              }"
            >
              <template v-if="(session.hrs ?? 0) >= 80">Siap Panen (Optimal)</template>
              <template v-else-if="(session.hrs ?? 0) >= 60">Hampir Siap Panen (Perlu Pemantauan)</template>
              <template v-else>Belum Siap Panen (Belum Optimal)</template>
            </span>
          </div>
        </div>

        <!-- Tombol Hapus (Kanan) -->
        <button 
          @click="(e) => deleteSession(session.id, e)"
          class="absolute right-4 p-2 text-slate-300 hover:text-red-500 hover:bg-red-50 active:bg-red-100 rounded-xl transition-all"
          title="Hapus Sesi Secara Permanen"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.145 0c-.167.04-.334.08-.5.12m-14.145 0c.167.04.334.08.5.12m14.145 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
