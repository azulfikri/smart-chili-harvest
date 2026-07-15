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
  <div class="bg-linear-to-br from-slate-950 via-emerald-950 to-slate-950 flex flex-col items-center justify-center min-h-screen relative overflow-hidden">
    
    <!-- Efek Cahaya Latar (Glow) -->
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-emerald-500/20 rounded-full blur-3xl"></div>

    <!-- Konten Utama -->
    <div class="relative z-10 flex flex-col items-center justify-center w-full px-6 text-center">
      
      <!-- Lingkaran Logo Animasi Berdenyut -->
      <div class="animate-pulse bg-emerald-500/10 border border-emerald-500/20 p-6 rounded-full mb-4 shadow-lg shadow-emerald-500/10">
        <!-- Ikon Minimalis AI / Daun Cabai -->
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 text-emerald-400">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
        </svg>
      </div>

      <!-- Tipografi Branding -->
      <h1 class="text-3xl font-extrabold tracking-wide text-white mb-2">Smart Harvest</h1>
      <h2 class="text-xs text-emerald-400/80 font-medium tracking-widest uppercase text-center max-w-[250px] leading-relaxed">
        AI-Powered Chili Maturity & Yield Estimation
      </h2>

      <!-- Loading Indicator Spinner -->
      <div class="animate-spin border-2 border-emerald-500 border-t-transparent rounded-full w-5 h-5 mt-8"></div>
    </div>

    <!-- Footer Copyright -->
    <p class="text-[10px] text-slate-500 font-semibold tracking-wider uppercase bottom-6 absolute">
      Universitas Madura &bull; 2026
    </p>

  </div>
</template>
