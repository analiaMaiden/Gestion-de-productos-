/* eslint-disable @typescript-eslint/no-explicit-any */
import { defineStore } from 'pinia';
import { api } from '../services/api';
import type { Producto, ProductoCreate, Categoria } from '../types/product';

export const useProductsStore = defineStore('products', {
  state: () => ({
    products: [] as Producto[],
    categories: [] as Categoria[],
    loading: false as boolean,
  }),
  actions: {
    async fetchCategories() {
      this.loading = true;
      try {
        const { data } = await api.get<Categoria[]>('/categorias');
        this.categories = data;
      } finally { this.loading = false; }
    },
    async fetchProducts() {
      this.loading = true;
      try {
        const { data } = await api.get<Producto[]>('/productos');
        this.products = data;
      } finally { this.loading = false; }
    },
    async createProduct(payload: ProductoCreate, imageFile?: File) {
      const form = new FormData();
      form.append('nombre', payload.nombre);
      form.append('descripcion', payload.descripcion);
      form.append('precio', String(payload.precio));
      form.append('categoria_id', String(payload.categoria_id));
      if (imageFile) form.append('image', imageFile); // ⬅️ cambia a 'imagen' si tu endpoint lo exige
      const { data } = await api.post<Producto>('/productos', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      this.products.unshift(data);
      return data;
    },
    async updateProduct(id: number, payload: ProductoCreate, imageFile?: File) {
      const form = new FormData();
      form.append('nombre', payload.nombre);
      form.append('descripcion', payload.descripcion);
      form.append('precio', String(payload.precio));
      form.append('categoria_id', String(payload.categoria_id));
      if (imageFile) form.append('image', imageFile); // ⬅️ idem
      const { data } = await api.put<Producto>(`/productos/${id}`, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const i = this.products.findIndex(p => p.id === id);
      if (i >= 0) this.products[i] = data;
      return data;
    },
    async deleteProduct(id: number) {
      await api.delete(`/productos/${id}`);
      this.products = this.products.filter(p => p.id !== id);
    },
  },
});
