<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div class="max-w-md mx-auto min-h-screen bg-gray-50 shadow-xl relative pb-16">
    <RouterView />

    <!-- Fixed Bottom Navigation Bar -->
    <nav class="fixed bottom-0 left-0 right-0 max-w-md mx-auto bg-white border-t border-gray-200 z-50 flex justify-around items-center h-16">
      <RouterLink 
        to="/dashboard" 
        class="flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors"
        :class="route.path === '/dashboard' ? 'text-green-600' : 'text-gray-400 hover:text-gray-500'"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
        </svg>
        <span class="text-xs font-medium">Dashboard</span>
      </RouterLink>

      <RouterLink 
        to="/detection" 
        class="flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors"
        :class="route.path === '/detection' ? 'text-green-600' : 'text-gray-400 hover:text-gray-500'"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
        </svg>
        <span class="text-xs font-medium">Deteksi</span>
      </RouterLink>

      <RouterLink 
        to="/history" 
        class="flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors"
        :class="route.path === '/history' ? 'text-green-600' : 'text-gray-400 hover:text-gray-500'"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="text-xs font-medium">Riwayat</span>
      </RouterLink>
    </nav>
  </div>
</template>

<style>
/* Basic reset/removal of vue scoped body styling if any escapes */
body {
  margin: 0;
  padding: 0;
  background-color: #f3f4f6; /* gray-100 for desktop background outside mobile view */
}
</style>
