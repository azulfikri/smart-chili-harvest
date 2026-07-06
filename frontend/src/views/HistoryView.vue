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
  <div class="p-4 flex flex-col min-h-[calc(100vh-4rem)]">
    <!-- Header -->
    <header class="mb-6 mt-2 px-2">
      <h1 class="text-2xl font-bold text-gray-900">Riwayat Pengamatan</h1>
      <p class="text-sm text-gray-500 mt-1">Daftar rekaman riwayat deteksi panen.</p>
    </header>

    <!-- Loading State -->
    <div v-if="isLoading" class="grow flex justify-center items-center">
      <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-green-600"></div>
    </div>

    <!-- Empty State (Jika Data Kosong) -->
    <div v-else-if="historyList.length === 0" class="grow flex flex-col justify-center items-center text-center p-6">
      <div class="w-24 h-24 bg-gray-100 rounded-full flex justify-center items-center mb-4 text-gray-300">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h3 class="text-lg font-bold text-gray-800">Riwayat Kosong</h3>
      <p class="text-gray-500 mt-2 text-sm leading-relaxed">Belum ada riwayat pengamatan yang tersimpan. Lakukan deteksi di Dashboard untuk mulai.</p>
    </div>

    <!-- List Sesi (Card Item) -->
    <div v-else class="grow flex flex-col gap-3 pb-6">
      <div 
        v-for="session in historyList" 
        :key="session.id"
        @click="goToDetail(session.id)"
        class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4 flex items-center justify-between cursor-pointer hover:border-green-300 hover:shadow-md active:scale-[0.98] transition-all group"
      >
        <!-- Informasi Sesi (Kiri) -->
        <div class="flex flex-col gap-1 w-full mr-4">
          <h3 class="font-bold text-gray-800 text-[15px] truncate">{{ session.session_name }}</h3>
          
          <div class="flex items-center gap-2 mt-1">
            <span class="text-xs font-medium text-gray-500">
              Skor HRS: <span class="text-gray-800 font-bold">{{ session.hrs !== null ? Number(session.hrs).toFixed(1) + '%' : 'Tidak Ada' }}</span>
            </span>
          </div>
          
          <div class="mt-2">
            <!-- Badge Status Panen Dinamis -->
            <span 
              class="px-2.5 py-1 text-[10px] font-bold rounded-md uppercase tracking-wide inline-block"
              :class="{
                'bg-green-100 text-green-700': session.harvest_status === 'Siap Panen' || ((session.hrs ?? 0) >= 80),
                'bg-orange-100 text-orange-700': session.harvest_status === 'Hampir Siap Panen' || ((session.hrs ?? 0) >= 60 && (session.hrs ?? 0) < 80),
                'bg-red-100 text-red-700': session.harvest_status === 'Belum Siap Panen' || ((session.hrs ?? 0) < 60)
              }"
            >
              {{ session.harvest_status || 'Belum Siap Panen' }}
            </span>
          </div>
        </div>

        <!-- Tombol Hapus (Kanan) -->
        <button 
          @click="(e) => deleteSession(session.id, e)"
          class="p-2.5 text-red-400 hover:text-red-600 hover:bg-red-50 active:bg-red-100 rounded-xl transition-all"
          title="Hapus Sesi Secara Permanen"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 opacity-80 group-hover:opacity-100">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.145 0c-.167.04-.334.08-.5.12m-14.145 0c.167.04.334.08.5.12m14.145 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
