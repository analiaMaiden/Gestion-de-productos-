<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue';
</script>

<template>
  <div class="min-vh-100 bg-light d-flex flex-column">
    <AppHeader />
    <main class="container my-4 flex-grow-1">
      <router-view />
    </main>
  </div>
</template>
