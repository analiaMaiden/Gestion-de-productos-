<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
const router = useRouter();
const auth = useAuthStore();
function logout() { auth.logout(); router.replace('/login'); }
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm px-3">
    <div class="container-fluid">
      <a class="navbar-brand fw-semibold" href="#">Gestión de Productos</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navContent">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div id="navContent" class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto">
          <li class="nav-item"><RouterLink class="nav-link" to="/productos">Productos</RouterLink></li>
        </ul>
        <span class="me-3 small text-white-50 d-none d-md-inline">
          Hola, {{ auth.user?.username || auth.user?.email || 'Usuario' }}
        </span>
        <button class="btn btn-outline-light" @click="logout">
          <i class="bi bi-box-arrow-right me-1"></i> Salir
        </button>
      </div>
    </div>
  </nav>
</template>
