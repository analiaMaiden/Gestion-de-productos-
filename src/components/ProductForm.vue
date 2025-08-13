<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import type { Producto, ProductoCreate, Categoria } from '../types/product';
import { useProductsStore } from '../stores/products';

const props = defineProps<{ categories: Categoria[]; initial?: Producto }>();
const emit = defineEmits<{ done: []; cancel: [] }>();
const store = useProductsStore();

const form = ref<ProductoCreate>({ nombre: '', descripcion: '', precio: 0, categoria_id: 0 });
const file = ref<File | null>(null);
const previewUrl = ref<string | null>(null);
const imageError = ref<string | null>(null);

const isEdit = computed(() => !!props.initial && typeof props.initial.id !== 'undefined');

watch(() => props.initial, (val) => {
  if (val) {
    form.value = {
      nombre: val.nombre, descripcion: val.descripcion,
      precio: val.precio, categoria_id: val.categoria_id
    };
    previewUrl.value = val.imagen ?? null;
    file.value = null; imageError.value = null;
  } else reset();
}, { immediate: true });

function reset() {
  form.value = { nombre: '', descripcion: '', precio: 0, categoria_id: 0 };
  file.value = null; previewUrl.value = null; imageError.value = null;
}

function onFileChange(e: Event) {
  const t = e.target as HTMLInputElement;
  const f = t.files?.[0] ?? null;
  file.value = null; previewUrl.value = null; imageError.value = null;
  if (!f) return;
  const ok = ['image/jpeg','image/png','image/webp'];
  if (!ok.includes(f.type)) { imageError.value = 'Usa JPG, PNG o WEBP.'; t.value=''; return; }
  if (f.size > 2*1024*1024) { imageError.value = 'Máximo 2MB.'; t.value=''; return; }
  file.value = f;
  const r = new FileReader(); r.onload = () => previewUrl.value = String(r.result); r.readAsDataURL(f);
}

async function submit() {
  if (!form.value.nombre || !form.value.categoria_id) { alert('Nombre y Categoría son obligatorios'); return; }
  try {
    if (isEdit.value && props.initial)
      await store.updateProduct(props.initial.id, form.value, file.value ?? undefined);
    else
      await store.createProduct(form.value, file.value ?? undefined);
    reset(); emit('done');
  } catch { alert('Error guardando el producto'); }
}
</script>

<template>
  <form @submit.prevent="submit" class="row g-3">
    <div class="col-12">
      <label class="form-label">Nombre</label>
      <input v-model="form.nombre" class="form-control" placeholder="Nombre del producto" />
    </div>

    <div class="col-12">
      <label class="form-label">Descripción</label>
      <textarea v-model="form.descripcion" rows="3" class="form-control" placeholder="Descripción"></textarea>
    </div>

    <div class="col-6">
      <label class="form-label">Precio</label>
      <input v-model.number="form.precio" type="number" step="0.01" class="form-control" placeholder="0.00" />
    </div>

    <div class="col-6">
      <label class="form-label">Categoría</label>
      <select v-model.number="form.categoria_id" class="form-select">
        <option :value="0" disabled>Selecciona una categoría</option>
        <option v-for="c in props.categories" :key="c.id" :value="c.id">{{ c.nombre }}</option>
      </select>
    </div>

    <div class="col-12">
      <label class="form-label">Imagen</label>
      <input type="file" class="form-control" accept="image/*" @change="onFileChange" />
      <div class="form-text" v-if="imageError">
        <span class="text-danger">{{ imageError }}</span>
      </div>

      <div class="mt-2 d-flex align-items-center gap-3" v-if="previewUrl">
        <img :src="previewUrl" alt="preview" class="img-thumbnail" style="width: 96px; height: 96px; object-fit: cover;" />
        <small class="text-muted">Vista previa</small>
      </div>
    </div>

    <div class="col-12 d-flex gap-2 justify-content-end">
      <button type="button" class="btn btn-outline-secondary" @click="reset">Limpiar</button>
      <button type="submit" class="btn btn-dark">{{ isEdit ? 'Actualizar' : 'Crear' }}</button>
      <button v-if="isEdit" type="button" class="btn btn-outline-secondary" @click="$emit('cancel')">Cancelar</button>
    </div>
  </form>
</template>
