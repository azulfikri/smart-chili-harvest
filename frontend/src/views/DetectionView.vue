<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// STATE MANAGEMENT UTAMA
const currentSessionId = ref<string | null>(null)
interface DetectionResult {
  status: string;
  session_id: number;
  semi_ripe: number;
  nearly_ripe: number;
  ripe: number;
  persen_semi_ripe: number;
  persen_nearly_ripe: number;
  persen_ripe: number;
  confidence: number;
  boxes: Array<{ box: number[]; label: string }>;
}

const photoCounter = ref(0)
const detectionsList = ref<DetectionResult[]>([])
const currentPhotoData = ref<DetectionResult | null>(null)
const isViewingFeedback = ref(false)

// Tambahan state untuk UI & UX
const isUploading = ref(false)
const isFinalizing = ref(false)
const previewImageUrl = ref<string | null>(null)
const fileInputRef = ref<HTMLInputElement | null>(null)

// Lifecycle Hook
onMounted(() => {
  const sessionId = localStorage.getItem('activeSessionId')
  if (!sessionId) {
    alert('Sesi tidak valid! Kembali ke Dashboard.')
    router.push('/dashboard')
    return
  }
  currentSessionId.value = sessionId
})

// Fungsi memicu hidden input file
const triggerFileInput = (captureMode: boolean) => {
  if (!fileInputRef.value) return
  
  if (captureMode) {
    fileInputRef.value.setAttribute('capture', 'environment')
  } else {
    fileInputRef.value.removeAttribute('capture')
  }
  
  fileInputRef.value.click()
}

// Handler ketika file dipilih (Bisa dari mock browser desktop atau smartphone)
const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!target.files || target.files.length === 0) return

  const file = target.files[0]
  if (!file) return
  
  // Create object URL untuk preview gambar pada Layar Feedback
  previewImageUrl.value = URL.createObjectURL(file)
  
  const formData = new FormData()
  formData.append('file', file)

  isUploading.value = true
  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/sessions/${currentSessionId.value}/detect`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    // Simpan respon backend ke state feedback layer
    currentPhotoData.value = response.data
    // Tampilkan Layar Feedback
    isViewingFeedback.value = true
  } catch (error) {
    console.error('Error uploading photo:', error)
    alert('Gagal memproses gambar. Pastikan API Backend berjalan dan tidak ada masalah CORS.')
  } finally {
    isUploading.value = false
    // Reset nilai file input agar input file yang sama bisa memicu trigger event lagi
    if (fileInputRef.value) fileInputRef.value.value = ''
  }
}

// Handler Layar B: Foto Ulang
const handleRetake = () => {
  currentPhotoData.value = null
  if (previewImageUrl.value) {
    URL.revokeObjectURL(previewImageUrl.value)
    previewImageUrl.value = null
  }
  // Kembali ke Layar Kamera Utama tanpa menambah counter
  isViewingFeedback.value = false
}

// Handler Layar B: Simpan & Lanjut
const handleSaveAndContinue = () => {
  if (currentPhotoData.value) {
    detectionsList.value.push(currentPhotoData.value)
    photoCounter.value++
  }
  currentPhotoData.value = null
  if (previewImageUrl.value) {
    URL.revokeObjectURL(previewImageUrl.value)
    previewImageUrl.value = null
  }
  // Kembali ke Layar Kamera Utama dan siap untuk pohon selanjutnya
  isViewingFeedback.value = false
}

// Handler Evaluasi Akhir (Hitung HRS)
const handleFinalize = async () => {
  // Guard condition sesuai spesifikasi
  if (photoCounter.value < 7) return
  
  isFinalizing.value = true
  try {
    await axios.post(`http://127.0.0.1:8000/api/sessions/${currentSessionId.value}/finalize`)
    // Arahkan ke history view setelah sukses finalize
    router.push(`/sessions/${currentSessionId.value}`)
  } catch (error) {
    console.error('Error finalizing session:', error)
    alert('Gagal mengkalkulasi HRS. Pastikan backend aktif.')
  } finally {
    isFinalizing.value = false
  }
}
</script>

<template>
  <div class="flex flex-col min-h-[calc(100vh-5rem)]">
    
    <!-- Hidden File Input -->
    <input 
      type="file" 
      accept="image/*" 
      ref="fileInputRef" 
      class="hidden" 
      @change="handleFileUpload"
    >

    <!-- Top Header Bar -->
    <div class="flex items-center justify-between px-4 py-3">
      <button 
        @click="router.push('/dashboard')" 
        class="p-2 -ml-2 rounded-full hover:bg-slate-100 active:bg-slate-200 transition-colors text-slate-700"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
        </svg>
      </button>
      <h1 class="text-base font-bold text-slate-800">Pemindaian AI</h1>
      <!-- Floating Pill Counter -->
      <div 
        class="px-3 py-1 rounded-full text-xs font-semibold border"
        :class="photoCounter >= 7 
          ? 'bg-emerald-50 text-emerald-700 border-emerald-200' 
          : 'bg-slate-100 text-slate-600 border-slate-200'"
      >
        <span :class="{'text-emerald-600 font-bold': photoCounter >= 7}">{{ photoCounter }}</span> / 7
      </div>
    </div>

    <!-- ============================================ -->
    <!-- LAYAR B: Feedback Instan Setelah Foto Diambil -->
    <!-- ============================================ -->
    <div v-if="isViewingFeedback" class="grow flex flex-col px-4 pb-4">
      
      <!-- Preview Foto -->
      <div class="w-full rounded-2xl shadow-md border border-slate-100 overflow-hidden bg-slate-900">
        <div class="w-full aspect-[3/4] relative flex items-center justify-center">
          <img v-if="previewImageUrl" :src="previewImageUrl" class="w-full h-full object-contain" alt="Captured Chili" />
          
          <!-- Overlay Success Indicator -->
          <div v-if="currentPhotoData && currentPhotoData.status === 'success'" class="absolute top-3 right-3 bg-emerald-500 text-white px-2.5 py-1 rounded-full text-[10px] font-bold tracking-wide flex items-center gap-1 shadow-lg">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3 h-3">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
            </svg>
            Terdeteksi
          </div>
        </div>
      </div>

      <!-- Mini Grid Statistik 3 Kolom -->
      <div v-if="currentPhotoData" class="bg-white rounded-2xl shadow-sm border border-slate-100 mt-4 overflow-hidden">
        <p class="text-[10px] font-semibold text-slate-400 uppercase tracking-widest text-center pt-3 pb-2">Hasil Deteksi AI</p>
        <div class="grid grid-cols-3 divide-x divide-slate-100">
          <!-- Semi-ripe -->
          <div class="flex flex-col items-center py-3">
            <span class="text-lg font-bold text-slate-800">{{ currentPhotoData.semi_ripe }}</span>
            <span class="text-[10px] font-medium text-amber-500 uppercase tracking-wider mt-0.5">Semi-ripe</span>
          </div>
          <!-- Nearly-ripe -->
          <div class="flex flex-col items-center py-3">
            <span class="text-lg font-bold text-slate-800">{{ currentPhotoData.nearly_ripe }}</span>
            <span class="text-[10px] font-medium text-orange-500 uppercase tracking-wider mt-0.5">Nearly-ripe</span>
          </div>
          <!-- Ripe -->
          <div class="flex flex-col items-center py-3">
            <span class="text-lg font-bold text-slate-800">{{ currentPhotoData.ripe }}</span>
            <span class="text-[10px] font-medium text-rose-600 uppercase tracking-wider mt-0.5">Ripe</span>
          </div>
        </div>
      </div>

      <!-- Spacer -->
      <div class="grow"></div>

      <!-- Tombol Aksi Feedback -->
      <div class="flex gap-3 mt-4">
        <button 
          @click="handleRetake"
          class="flex-1 py-3.5 px-4 rounded-xl font-semibold text-sm bg-slate-100 text-slate-600 hover:bg-slate-200 active:bg-slate-200 transition-all active:scale-[0.98] flex justify-center items-center gap-2 cursor-pointer"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          Foto Ulang
        </button>
        <button 
          @click="handleSaveAndContinue"
          class="flex-1 py-3.5 px-4 rounded-xl font-semibold text-sm bg-emerald-600 text-white hover:bg-emerald-700 active:bg-emerald-800 transition-all active:scale-[0.98] shadow-lg shadow-emerald-600/20 flex justify-center items-center gap-2 cursor-pointer"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
          </svg>
          Simpan & Lanjut
        </button>
      </div>
    </div>

    <!-- ======================================== -->
    <!-- LAYAR A: Kamera Aktif & Placeholder -->
    <!-- ======================================== -->
    <div v-else class="grow flex flex-col px-4 pb-4">
      
      <!-- Bingkai Kamera Futuristik -->
      <div class="w-full grow bg-slate-900 rounded-2xl relative shadow-[inset_0_2px_20px_rgba(0,0,0,0.3)] overflow-hidden flex flex-col items-center justify-center">
        
        <!-- Loading Overlay Saat Upload -->
        <div v-if="isUploading" class="absolute inset-0 bg-black/80 z-20 flex flex-col items-center justify-center text-white backdrop-blur-sm">
          <div class="animate-spin rounded-full h-12 w-12 border-2 border-white/20 border-t-white mb-4"></div>
          <p class="text-sm font-semibold tracking-wide">Menganalisis Gambar...</p>
          <p class="text-xs text-white/50 mt-1">Model YOLOv8 sedang memproses</p>
        </div>

        <!-- Scanning Target Overlay (Sudut Bidik) -->
        <div class="absolute inset-6 pointer-events-none">
          <!-- Top-Left Corner -->
          <div class="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-white/30 rounded-tl-lg"></div>
          <!-- Top-Right Corner -->
          <div class="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-white/30 rounded-tr-lg"></div>
          <!-- Bottom-Left Corner -->
          <div class="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-white/30 rounded-bl-lg"></div>
          <!-- Bottom-Right Corner -->
          <div class="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-white/30 rounded-br-lg"></div>
        </div>

        <!-- Ikon Kamera Center -->
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="0.8" stroke="currentColor" class="w-16 h-16 text-white/15 mb-2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
        </svg>
        <p class="text-white/25 text-xs font-medium tracking-wider uppercase">Arahkan ke tanaman cabai</p>
      </div>

      <!-- Tombol Capture & Galeri -->
      <div class="flex items-center gap-3 mt-4">
        <!-- Tombol Galeri (Kiri) -->
        <button 
          @click="triggerFileInput(false)"
          :disabled="isUploading"
          class="w-14 h-14 flex items-center justify-center bg-white border border-slate-200 rounded-xl shadow-sm hover:bg-slate-50 active:bg-slate-100 transition-all cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-slate-500">
            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
          </svg>
        </button>

        <!-- Tombol Capture Besar (Tengah) -->
        <button 
          @click="triggerFileInput(true)"
          :disabled="isUploading"
          class="grow h-14 flex items-center justify-center bg-white border-2 border-emerald-500 rounded-xl shadow-md hover:border-emerald-600 active:scale-[0.97] transition-all cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed gap-2"
        >
          <!-- Shutter Ring -->
          <div class="w-10 h-10 rounded-full border-[3px] border-emerald-500 flex items-center justify-center">
            <div class="w-7 h-7 rounded-full bg-emerald-500"></div>
          </div>
          <span class="text-xs font-bold text-emerald-700 uppercase tracking-wide">Ambil Foto</span>
        </button>
      </div>
    </div>

    <!-- Tombol Evaluasi Akhir (Hitung HRS) -->
    <div class="px-4 pb-4">
      <button 
        @click="handleFinalize"
        :disabled="photoCounter < 7 || isFinalizing"
        class="w-full py-4 px-6 rounded-xl font-semibold text-sm transition-all duration-200 flex justify-center items-center gap-2"
        :class="{
          'bg-slate-200 text-slate-400 cursor-not-allowed': photoCounter < 7,
          'bg-[#065f46] text-white shadow-lg shadow-emerald-700/20 hover:bg-[#064e3b] active:scale-[0.98] cursor-pointer': photoCounter >= 7
        }"
      >
        <span v-if="isFinalizing" class="animate-spin rounded-full h-5 w-5 border-2 border-white/20 border-t-white"></span>
        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ isFinalizing ? 'Menghitung Data...' : (photoCounter < 7 ? `Kurang ${7 - photoCounter} Foto Lagi` : 'Hitung Kesiapan Panen (HRS)') }}
      </button>
    </div>
  </div>
</template>

