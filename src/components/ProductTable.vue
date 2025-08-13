<script setup lang="ts">
import type { Producto } from '../types/product';
import { toImageURL } from '../services/config';

const props = defineProps<{ products: Producto[] }>();
const emit = defineEmits<{ edit: [Producto]; remove: [number] }>();

function onRemove(id: number) {
  if (confirm('¿Eliminar producto?')) emit('remove', id);
}
</script>

<template>
  <table class="table table-sm table-striped table-hover align-middle">
    <thead class="table-light">
      <tr>
        <th>ID</th>
        <th>Nombre</th>
        <th class="w-25">Descripción</th>
        <th>Categoría</th>
        <th>Precio</th>
        <th>Imagen</th>
        <th class="text-nowrap">Acciones</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="p in products" :key="p.id">
        <td>{{ p.id }}</td>
        <td class="fw-semibold">{{ p.nombre }}</td>
        <td class="text-muted">{{ p.descripcion }}</td>
        <td>{{ p.categoria?.nombre ?? p.categoria_id }}</td>
        <td>{{ p.precio }}</td>
        <td>
          <img v-if="p.imagen" :src="toImageURL(p.imagen)" alt="img" class="thumb img-thumbnail" />
          <span v-else class="text-secondary">—</span>
        </td>
        <td class="text-nowrap">
          <button class="btn btn-outline-primary btn-sm me-2" @click="$emit('edit', p)">Editar</button>
          <button class="btn btn-outline-danger btn-sm" @click="onRemove(p.id)">Eliminar</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.thumb{
  width: 72px;
  height: 72px;
  object-fit: cover;
  border-radius: .5rem;
}
</style>
