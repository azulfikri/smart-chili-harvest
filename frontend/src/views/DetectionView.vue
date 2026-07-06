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
    router.push('/history')
  } catch (error) {
    console.error('Error finalizing session:', error)
    alert('Gagal mengkalkulasi HRS. Pastikan backend aktif.')
  } finally {
    isFinalizing.value = false
  }
}
</script>

<template>
  <div class="p-4 flex flex-col h-[calc(100vh-4rem)]">
    
    <!-- Hidden File Input untuk integrasi Kamera Smartphone & File Browser Desktop -->
    <input 
      type="file" 
      accept="image/*" 
      ref="fileInputRef" 
      class="hidden" 
      @change="handleFileUpload"
    >

    <!-- LAYAR B (Feedback Instan Kotak Pembatas Per Foto) -->
    <div v-if="isViewingFeedback" class="grow flex flex-col items-center animate-in fade-in zoom-in duration-300">
      <div class="w-full bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden mt-2">
        <!-- Placeholder Image -->
        <div class="w-full h-80 bg-gray-900 relative flex items-center justify-center">
          <img v-if="previewImageUrl" :src="previewImageUrl" class="w-full h-full object-contain" alt="Captured Chili" />
          
          <!-- Mockup Bounding Box Overlay jika respon deteksi berhasil -->
          <div v-if="currentPhotoData && currentPhotoData.status === 'success'" class="absolute inset-0 border-4 border-green-500 rounded border-dashed opacity-50 m-4 pointer-events-none"></div>
        </div>

        <!-- Teks Statistik -->
        <div class="p-5 text-center bg-white">
          <h2 class="text-sm font-semibold text-gray-500 mb-2 uppercase tracking-wider">Hasil Deteksi AI</h2>
          <div v-if="currentPhotoData" class="flex justify-center space-x-4 text-xs font-medium text-gray-800">
            <div class="flex flex-col items-center">
              <span class="w-3 h-3 rounded-full bg-yellow-400 mb-1"></span>
              <span>Semi-ripe: {{ currentPhotoData.semi_ripe }}</span>
            </div>
            <div class="flex flex-col items-center">
              <span class="w-3 h-3 rounded-full bg-orange-500 mb-1"></span>
              <span>Nearly-ripe: {{ currentPhotoData.nearly_ripe }}</span>
            </div>
            <div class="flex flex-col items-center">
              <span class="w-3 h-3 rounded-full bg-red-600 mb-1"></span>
              <span>Ripe: {{ currentPhotoData.ripe }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tombol Feedback Horizontal -->
      <div class="w-full flex justify-between space-x-3 mt-6">
        <button 
          @click="handleRetake"
          class="flex-1 py-4 px-4 rounded-xl font-bold border-2 border-red-500 text-red-500 active:bg-red-50 transition-colors flex justify-center items-center gap-2"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          Foto Ulang
        </button>
        <button 
          @click="handleSaveAndContinue"
          class="flex-1 py-4 px-4 rounded-xl font-bold bg-green-600 text-white active:bg-green-700 transition-colors flex justify-center items-center gap-2 shadow-lg shadow-green-200"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
          </svg>
          Simpan & Lanjut
        </button>
      </div>
    </div>

    <!-- LAYAR A (Kamera Aktif & Placeholder Capture) -->
    <div v-else class="grow flex flex-col">
      <!-- Indikator Counter Kanan Atas -->
      <div class="flex justify-end mb-2">
        <div class="bg-black/60 text-white px-4 py-1.5 rounded-full text-xs font-bold shadow-md z-10 flex items-center gap-2">
          <span :class="{'text-green-400': photoCounter >= 7}">Foto: {{ photoCounter }} / 7</span>
        </div>
      </div>

      <!-- Kotak Hitam Placeholder Kamera -->
      <div class="w-full grow bg-gray-900 rounded-2xl relative shadow-inner overflow-hidden flex flex-col items-center justify-center">
        <!-- Loading Overlay Saat Upload -->
        <div v-if="isUploading" class="absolute inset-0 bg-black/70 z-20 flex flex-col items-center justify-center text-white">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-white mb-3"></div>
          <p class="font-medium">Menganalisis Gambar AI...</p>
        </div>

        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1" stroke="currentColor" class="w-20 h-20 text-gray-700 mb-2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
        </svg>
        <p class="text-gray-500 font-medium">Lensa Kamera Siap</p>
      </div>

      <!-- Alternatif Input Horizontal (Bawah Kamera) -->
      <div class="flex space-x-3 mt-4 mb-2">
        <!-- Tombol Utama (Ambil Foto) -->
        <button 
          @click="triggerFileInput(true)"
          :disabled="isUploading"
          class="grow flex flex-col items-center justify-center bg-gray-800 hover:bg-gray-700 active:bg-gray-900 text-white py-4 rounded-2xl shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <!-- Lingkaran Shutter -->
          <div class="w-12 h-12 rounded-full border-4 border-gray-400 bg-white mb-2 flex items-center justify-center">
            <div class="w-10 h-10 rounded-full bg-white border-2 border-gray-800"></div>
          </div>
          <span class="text-xs font-bold tracking-wide uppercase">Ambil Foto</span>
        </button>

        <!-- Tombol Sekunder (Galeri) -->
        <button 
          @click="triggerFileInput(false)"
          :disabled="isUploading"
          class="w-1/3 flex flex-col items-center justify-center bg-white border border-gray-200 text-gray-700 py-4 rounded-2xl shadow-sm hover:bg-gray-50 active:bg-gray-100 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-7 h-7 mb-2 text-gray-500">
            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
          </svg>
          <span class="text-[10px] font-bold tracking-wide uppercase">Galeri</span>
        </button>
      </div>
    </div>

    <!-- Tombol Evaluasi Akhir (Hitung HRS) -->
    <div class="mt-4 mb-2">
      <button 
        @click="handleFinalize"
        :disabled="photoCounter < 7 || isFinalizing"
        class="w-full py-4 px-6 rounded-xl font-bold text-white shadow transition-all flex justify-center items-center gap-2"
        :class="{
          'bg-gray-300 text-gray-500 cursor-not-allowed': photoCounter < 7,
          'bg-green-500 hover:bg-green-600 active:bg-green-700 shadow-green-200 shadow-lg': photoCounter >= 7
        }"
      >
        <span v-if="isFinalizing" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span>
        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ isFinalizing ? 'Menghitung Data...' : (photoCounter < 7 ? `Kurang ${7 - photoCounter} Foto Lagi` : 'Hitung Kesiapan Panen (HRS)') }}
      </button>
    </div>
  </div>
</template>
