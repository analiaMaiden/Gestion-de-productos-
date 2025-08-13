<!-- src/pages/LoginPage.vue -->
<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const auth = useAuthStore();

const form = ref({ username: '', password: '' });
const errorMsg = ref<string | null>(null);
const showPass = ref(false);

async function submit() {
  if (!form.value.username || !form.value.password) {
    errorMsg.value = 'Completa usuario y contraseña.';
    return;
  }
  errorMsg.value = null;
  const ok = await auth.login({
    username: form.value.username,
    password: form.value.password,
  });
  if (ok) router.replace('/productos');
  else errorMsg.value = 'Credenciales inválidas o error del servidor';
}
</script>

<template>
  <div class="bg-light min-vh-100 d-flex align-items-center justify-content-center px-3">
    <div class="w-100" style="max-width: 440px;">
      <!-- Marca -->
      <div class="text-center mb-4">
        <div class="d-inline-flex align-items-center gap-2">
          <i class="bi bi-box-seam-fill fs-3 text-primary"></i>
          <h1 class="h4 m-0 fw-bold">Gestión de Productos</h1>
        </div>
        <p class="text-muted mt-2 mb-0">Inicia sesión para continuar</p>
      </div>

      <!-- Tarjeta -->
      <div class="card shadow-lg border-0 rounded-4">
        <div class="card-body p-4">
          <form @submit.prevent="submit" novalidate>
            <!-- Usuario -->
            <div class="mb-3">
              <label class="form-label">Usuario</label>
              <div class="input-group">
                <span class="input-group-text"><i class="bi bi-person"></i></span>
                <input
                  v-model="form.username"
                  class="form-control"
                  placeholder="admin"
                  autocomplete="username"
                />
              </div>
            </div>

            <!-- Contraseña -->
            <div class="mb-2">
              <label class="form-label">Contraseña</label>
              <div class="input-group">
                <span class="input-group-text"><i class="bi bi-lock"></i></span>
                <input
                  :type="showPass ? 'text' : 'password'"
                  v-model="form.password"
                  class="form-control"
                  placeholder="••••••••"
                  autocomplete="current-password"
                />
                <button
                  type="button"
                  class="btn btn-outline-secondary"
                  @click="showPass = !showPass"
                  :aria-pressed="showPass"
                >
                  <i :class="showPass ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
            </div>

            <!-- Error -->
            <div v-if="errorMsg" class="alert alert-danger py-2 small mb-3">
              {{ errorMsg }}
            </div>

            <!-- Botón -->
            <div class="d-grid">
              <button class="btn btn-primary py-2" :disabled="auth.loading">
                <span v-if="auth.loading" class="spinner-border spinner-border-sm me-2" role="status" />
                {{ auth.loading ? 'Entrando…' : 'Entrar' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Pie -->
      <p class="text-center text-muted small mt-3 mb-0">
        © {{ new Date().getFullYear() }} prueba
      </p>
    </div>
  </div>
</template>

<style scoped>
/* detalles sutiles */
.card { backdrop-filter: blur(2px); }
</style>
