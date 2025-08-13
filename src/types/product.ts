export interface Categoria {
  id: number;
  nombre: string;
}

export interface Producto {
  id: number;
  nombre: string;
  descripcion: string;
  precio: number;
  imagen?: string | null;
  categoria_id: number;
  categoria?: Categoria;
}

export interface ProductoCreate {
  nombre: string;
  descripcion: string;
  precio: number;
  categoria_id: number;
}
