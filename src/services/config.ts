export const API_URL = import.meta.env.VITE_API_URL as string;

export const AUTH_PATHS = {
  login: '/auth/login',
  refresh: '/auth/refresh',
  me: '/auth/me',
};

export const API_ORIGIN = new URL(API_URL).origin;

export function toImageURL(path?: string | null) {
  if (!path) return null;
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  if (path.startsWith('/')) return API_ORIGIN + path;
  return `${API_ORIGIN}/uploads/${path}`;
}
