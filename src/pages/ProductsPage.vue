<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useProductsStore } from '../stores/products';
import ProductForm from '../components/ProductForm.vue';
import ProductTable from '../components/ProductTable.vue';
import type { Producto } from '../types/product';

const store = useProductsStore();
const editing = ref<Producto | null>(null);

onMounted(async () => {
  await Promise.all([store.fetchCategories(), store.fetchProducts()]);
});

function onEdit(p: Producto) { editing.value = p; }
function onCancelEdit() { editing.value = null; }
function onDone() { editing.value = null; }
</script>

<template>
  <div class="container my-4">
    <h1 class="display-6 fw-bold mb-4">Productos</h1>

    <div class="row g-4">
      <!-- Formulario -->
      <div class="col-12 col-lg-6">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white">
            <h2 class="h6 m-0">{{ editing ? 'Editar' : 'Crear' }} producto</h2>
          </div>
          <div class="card-body">
            <ProductForm
              :categories="store.categories"
              :initial="editing ?? undefined"
              @done="onDone"
              @cancel="onCancelEdit"
            />
          </div>
        </div>
      </div>

      <!-- Listado -->
      <div class="col-12 col-lg-6">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-white d-flex align-items-center justify-content-between">
            <h2 class="h6 m-0">Listado ({{ store.products.length }})</h2>
            <button class="btn btn-sm btn-outline-secondary"
                    @click="store.fetchProducts" :disabled="store.loading">
              {{ store.loading ? 'Cargando…' : 'Refrescar' }}
            </button>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <ProductTable
                :products="store.products"
                @edit="onEdit"
                @remove="store.deleteProduct"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
