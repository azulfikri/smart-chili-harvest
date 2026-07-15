<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  setTimeout(() => {
    router.push('/dashboard')
  }, 2500)
})
</script>

<template>
  <div class="bg-[#F3F9F1] flex flex-col items-center justify-center min-h-screen relative overflow-hidden font-sans">
    
    <!-- Konten Utama -->
    <div class="relative z-10 flex flex-col items-center justify-center w-full px-6 text-center">
      
      <!-- Lingkaran Putih Besar -->
      <div class="w-48 h-48 bg-white rounded-full flex items-center justify-center shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-black/5 mb-8">
        
        <!-- Inner Faint Square -->
        <div class="bg-[#F7FCF8] w-28 h-28 flex items-center justify-center p-3 rounded-sm">
          
          <!-- Logo Area -->
          <div class="flex items-center gap-1.5">
            <!-- Ikon Abstrak Scan & Cabai -->
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-8 h-8 text-[#065f46]">
              <!-- Target corners -->
              <path d="M4 8V6a2 2 0 0 1 2-2h2" />
              <path d="M4 16v2a2 2 0 0 0 2 2h2" />
              <path d="M16 4h2a2 2 0 0 1 2 2v2" />
              <path d="M16 20h2a2 2 0 0 0 2-2v-2" />
              <!-- Chili Shape -->
              <path d="M10 9c-2.5 0-4 2.5-3 5.5 .5 1.5 2 3.5 5 3.5s4.5-2 5-3.5c1-3-.5-5.5-3-5.5" />
              <path d="M13 9v-2" />
            </svg>
            
            <!-- Teks Logo Stacked -->
            <div class="flex flex-col items-start leading-[1.1]">
              <span class="text-[#065f46] font-extrabold text-[13px] tracking-tight">Smart</span>
              <span class="text-[#065f46] font-extrabold text-[13px] tracking-tight">Harvest</span>
            </div>
          </div>

        </div>
      </div>

      <!-- Tipografi Branding (Mengikuti Mockup) -->
      <h1 class="text-[22px] sm:text-[26px] font-black tracking-wide text-[#0b6e32] mb-3 uppercase">Smart Chili Harvest</h1>
      <h2 class="text-[10px] text-slate-700 font-bold tracking-[0.15em] uppercase text-center max-w-[280px] leading-relaxed mb-16">
        YOLOv8-Based Harvest Estimation Tool
      </h2>

      <!-- Loading Indicator Spinner Besar -->
      <div class="animate-spin border-[3px] border-[#c2e5d3] border-t-[#065f46] rounded-full w-[50px] h-[50px]"></div>
    </div>

    <!-- Footer Copyright -->
    <p class="text-[11px] text-slate-500 font-semibold tracking-wider bottom-8 absolute">
      Smart Agriculture Project &copy; 2026
    </p>

  </div>
</template>
