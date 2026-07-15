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
  thumbnail_image?: string; // Menampung gambar dari backend jika nanti ada
}

const historyList = ref<SessionHistory[]>([])
const isLoading = ref(true)

// Computed untuk Summary Cards
import { computed } from 'vue'

const totalSessions = computed(() => historyList.value.length)

const sessionsThisMonth = computed(() => {
  const now = new Date()
  const currentMonth = now.getMonth()
  const currentYear = now.getFullYear()
  
  return historyList.value.filter(session => {
    const sessionDate = new Date(session.created_at)
    return sessionDate.getMonth() === currentMonth && sessionDate.getFullYear() === currentYear
  }).length
})

// Format Tanggal: 04 Juli 2026
const formatDate = (dateString: string) => {
  const options: Intl.DateTimeFormatOptions = { day: '2-digit', month: 'long', year: 'numeric' }
  return new Date(dateString).toLocaleDateString('id-ID', options)
}

// Fetch Data dari API
const fetchHistory = async () => {
  isLoading.value = true
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/sessions')
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
const showDeleteDialog = ref(false)
const sessionToDelete = ref<number | null>(null)

const confirmDeleteSession = (id: number, event: Event) => {
  event.stopPropagation()
  sessionToDelete.value = id
  showDeleteDialog.value = true
}

const handleDeleteConfirm = async (confirmAction: boolean) => {
  showDeleteDialog.value = false
  if (confirmAction && sessionToDelete.value !== null) {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/sessions/${sessionToDelete.value}`)
      historyList.value = historyList.value.filter(session => session.id !== sessionToDelete.value)
    } catch (error) {
      console.error('Error deleting session:', error)
      alert('Gagal menghapus riwayat pengamatan.')
    }
  }
  sessionToDelete.value = null
}
</script>

<template>
  <div class="flex flex-col min-h-[calc(100vh-4rem)] bg-slate-50 pb-20">
    <div class="px-4 py-5">
      <!-- Title & Subtitle -->
      <h2 class="text-2xl font-black text-slate-800 mb-1">Riwayat Deteksi</h2>
      <p class="text-sm text-slate-500 leading-relaxed mb-6">Lacak perkembangan kematangan hasil panen cabai Anda dari waktu ke waktu.</p>
      
      <!-- Summary Grid -->
      <div class="grid grid-cols-2 gap-3 mb-6">
        <!-- Card Total Deteksi -->
        <div class="bg-white rounded-2xl p-4 border border-slate-100 shadow-sm flex flex-col justify-between">
          <div class="text-emerald-700 mb-3 bg-emerald-50 w-8 h-8 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
            </svg>
          </div>
          <div>
            <p class="text-xs font-semibold text-slate-500 mb-0.5">Total Deteksi</p>
            <p class="text-xl font-black text-slate-800">{{ totalSessions }} Sesi</p>
          </div>
        </div>
        
        <!-- Card Bulan Ini -->
        <div class="bg-emerald-700 rounded-2xl p-4 shadow-md flex flex-col justify-between text-white relative overflow-hidden">
          <!-- Dekorasi Background -->
          <div class="absolute -right-4 -top-4 w-16 h-16 bg-emerald-600 rounded-full opacity-50 blur-xl"></div>
          
          <div class="text-emerald-100 mb-3 bg-emerald-600 w-8 h-8 rounded-lg flex items-center justify-center relative z-10">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5m-9-6h.008v.008H12v-.008zM12 15h.008v.008H12V15zm0 2.25h.008v.008H12v-.008zM9.75 15h.008v.008H9.75V15zm0 2.25h.008v.008H9.75v-.008zM7.5 15h.008v.008H7.5V15zm0 2.25h.008v.008H7.5v-.008zm6.75-4.5h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V15zm0 2.25h.008v.008h-.008v-.008zm2.25-4.5h.008v.008H16.5v-.008zm0 2.25h.008v.008H16.5V15z" />
            </svg>
          </div>
          <div class="relative z-10">
            <p class="text-xs font-medium text-emerald-100 mb-0.5">Bulan Ini</p>
            <p class="text-xl font-black">{{ sessionsThisMonth }} Sesi</p>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center items-center py-10">
        <div class="animate-spin rounded-full h-8 w-8 border-2 border-emerald-200 border-t-emerald-600"></div>
      </div>

      <!-- Elegant Empty State -->
      <div v-else-if="historyList.length === 0" class="flex flex-col justify-center items-center text-center p-8 bg-white rounded-3xl border border-slate-100 shadow-sm mt-4">
        <div class="w-16 h-16 bg-slate-50 rounded-full flex justify-center items-center mb-3 text-slate-300">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
          </svg>
        </div>
        <p class="text-sm font-medium text-slate-400">Belum ada riwayat pengamatan lahan.</p>
      </div>

      <!-- List Sesi (Card Item Premium dengan Thumbnail) -->
      <div v-else class="flex flex-col gap-3">
        <div 
          v-for="session in historyList" 
          :key="session.id"
          @click="goToDetail(session.id)"
          class="bg-white rounded-2xl p-3 shadow-sm border border-slate-100 cursor-pointer hover:border-emerald-200 hover:shadow-md transition-all duration-200 active:scale-[0.98] group flex items-center relative overflow-hidden"
        >
          <!-- Thumbnail Image (Placeholder/Actual) -->
          <div class="w-[72px] h-[72px] rounded-xl bg-slate-50 border border-slate-100 overflow-hidden shrink-0 flex justify-center items-center">
            <img v-if="session.thumbnail_image" :src="session.thumbnail_image" class="w-full h-full object-cover" />
            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-slate-300">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
            </svg>
          </div>
          
          <!-- Informasi (Tengah) -->
          <div class="ml-3 grow flex flex-col justify-center py-1">
            <span class="text-[13px] font-bold text-slate-800 mb-1.5">{{ formatDate(session.created_at) }}</span>
            
            <div 
              class="flex items-center gap-1.5"
              :class="{
                'text-emerald-700': (session.hrs ?? 0) >= 80,
                'text-amber-600': (session.hrs ?? 0) >= 60 && (session.hrs ?? 0) < 80,
                'text-slate-500': (session.hrs ?? 0) < 60
              }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-3.5 h-3.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
              </svg>
              <span class="text-[11px] font-bold tracking-wide">Skor HRS: {{ session.hrs !== null ? Number(session.hrs).toFixed(0) + '%' : '-' }}</span>
            </div>
          </div>
          
          <!-- Aksi Kanan (Badge & Hapus Sejajar) -->
          <div class="flex items-center gap-2 mr-1">
            <!-- Solid Badge -->
            <span 
              class="px-2 py-1 text-[9px] font-bold rounded-full uppercase tracking-wider text-white"
              :class="{
                'bg-emerald-600': (session.hrs ?? 0) >= 80,
                'bg-amber-500': (session.hrs ?? 0) >= 60 && (session.hrs ?? 0) < 80,
                'bg-slate-500': (session.hrs ?? 0) < 60
              }"
            >
              <template v-if="(session.hrs ?? 0) >= 80">Siap Panen</template>
              <template v-else-if="(session.hrs ?? 0) >= 60">Hampir Siap</template>
              <template v-else>Belum Matang</template>
            </span>
            
            <!-- Tombol Hapus -->
            <button 
              @click="(e) => confirmDeleteSession(session.id, e)"
              class="p-1.5 text-slate-300 hover:text-red-500 hover:bg-red-50 active:bg-red-100 rounded-lg transition-all"
              title="Hapus Sesi"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.145 0c-.167.04-.334.08-.5.12m-14.145 0c.167.04.334.08.5.12m14.145 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Custom Modal Konfirmasi Hapus -->
    <div v-if="showDeleteDialog" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
      <div class="bg-white rounded-2xl p-6 w-full max-w-xs shadow-2xl scale-100 transition-transform flex flex-col items-center text-center animate-in fade-in zoom-in duration-200">
        <!-- Icon Alert -->
        <div class="w-16 h-16 bg-red-50 text-red-500 rounded-full flex items-center justify-center mb-4 border-4 border-red-100">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-7 h-7">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.145 0c-.167.04-.334.08-.5.12m-14.145 0c.167.04.334.08.5.12m14.145 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
          </svg>
        </div>
        <h3 class="text-lg font-bold text-slate-800 mb-2">Hapus Riwayat Sesi?</h3>
        <p class="text-sm text-slate-500 mb-6 font-medium leading-relaxed">Sesi ini akan dihapus secara <b>permanen</b> dan tidak dapat dikembalikan lagi.</p>
        <div class="w-full flex flex-col gap-2.5">
          <button @click="handleDeleteConfirm(false)" class="w-full py-3.5 px-4 rounded-xl font-bold text-sm bg-slate-100 text-slate-700 hover:bg-slate-200 active:bg-slate-300 transition-colors">
            Batal
          </button>
          <button @click="handleDeleteConfirm(true)" class="w-full py-3.5 px-4 rounded-xl font-bold text-sm bg-red-500 text-white hover:bg-red-600 active:bg-red-700 transition-colors shadow-lg shadow-red-500/30">
            Ya, Hapus
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
