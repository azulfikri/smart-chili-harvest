<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <!-- Background Global & Wrapper -->
  <div class="max-w-md mx-auto min-h-screen bg-slate-50 shadow-2xl shadow-slate-200 relative pb-20 pt-14">
    
    <!-- Global Top Header -->
    <header class="absolute top-0 left-0 right-0 h-14 bg-white border-b border-slate-100 flex items-center px-4 z-40">
      <div class="flex items-center gap-2">
        <svg viewBox="0 0 24 24" fill="currentColor" class="w-7 h-7 text-emerald-600">
          <path d="M17.5 2.5C13.5 2.5 10 5.5 8 9.5C6 13.5 5 18 5 18C5 18 9.5 17 13.5 15C17.5 13 20.5 9.5 20.5 5.5C20.5 4 19 2.5 17.5 2.5Z" />
          <path d="M8 9.5C10 5.5 13.5 2.5 17.5 2.5C14.5 3.5 12.5 6 11 8.5C9.5 11 8.5 14.5 5 18C5 18 5.5 13 8 9.5Z" fill="white" opacity="0.3" />
        </svg>
        <span class="text-lg font-black text-slate-800 tracking-tight">Smart<span class="text-emerald-600">Harvest</span></span>
      </div>
    </header>

    <RouterView />

    <!-- Glassmorphism Bottom Navigation Bar -->
    <nav class="fixed bottom-0 left-0 right-0 max-w-md mx-auto bg-white/80 backdrop-blur-md border-t border-slate-100 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] z-50 flex justify-around items-center h-20 pb-4 pt-3">
      
      <!-- Dashboard Button -->
      <RouterLink 
        to="/dashboard" 
        class="flex flex-col items-center justify-center w-full h-full space-y-1 transition-all duration-200 ease-in-out active:scale-95"
        :class="route.path === '/dashboard' ? 'text-emerald-600' : 'text-slate-400 hover:text-slate-500'"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
        </svg>
        <span class="text-xs font-medium tracking-wide">Dashboard</span>
      </RouterLink>

      <!-- Deteksi Button -->
      <RouterLink 
        to="/detection" 
        class="flex flex-col items-center justify-center w-full h-full space-y-1 transition-all duration-200 ease-in-out active:scale-95"
        :class="route.path === '/detection' ? 'text-emerald-600' : 'text-slate-400 hover:text-slate-500'"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
        </svg>
        <span class="text-xs font-medium tracking-wide">Deteksi</span>
      </RouterLink>

      <!-- Riwayat Button -->
      <RouterLink 
        to="/history" 
        class="flex flex-col items-center justify-center w-full h-full space-y-1 transition-all duration-200 ease-in-out active:scale-95"
        :class="route.path.includes('/history') || route.path.includes('/sessions') ? 'text-emerald-600' : 'text-slate-400 hover:text-slate-500'"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="text-xs font-medium tracking-wide">Riwayat</span>
      </RouterLink>
    </nav>
  </div>
</template>

<style>
/* Basic reset/removal of vue scoped body styling if any escapes */
body {
  margin: 0;
  padding: 0;
  background-color: #f8fafc; /* slate-50 for desktop background outside mobile view */
}
</style>
