/* eslint-disable @typescript-eslint/no-explicit-any */
import axios, { AxiosError, type AxiosRequestConfig } from 'axios';
import { API_URL, AUTH_PATHS } from './config';
// If HAS_REFRESH is needed, make sure to export it from './config'
const HAS_REFRESH = true; // Or import from './config' if available

const api = axios.create({
  baseURL: API_URL,
  timeout: 15000,
});

function getAccessToken() {
  return localStorage.getItem('access_token');
}
function getRefreshToken() {
  return localStorage.getItem('refresh_token');
}

api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers = {
      ...(config.headers || {}),
      Authorization: `Bearer ${token}`,
    } as any;
  }
  return config;
});

let refreshing = false;
let queue: Array<[(v?: unknown) => void, (e?: unknown) => void]> = [];

function resolveQueue(error: unknown, token: string | null) {
  queue.forEach(([res, rej]) => (error ? rej(error) : res(token)));
  queue = [];
}

api.interceptors.response.use(
  (r) => r,
  async (error: AxiosError) => {
    if (!HAS_REFRESH) return Promise.reject(error);

    const status = error.response?.status;
    const original = error.config as AxiosRequestConfig & { _retry?: boolean };

    if (status === 401 && !original._retry) {
      if (refreshing) {
        return new Promise((resolve, reject) => {
          queue.push([resolve, reject]);
        }).then(() => {
          const token = getAccessToken();
          if (token) {
            original.headers = {
              ...(original.headers || {}),
              Authorization: `Bearer ${token}`,
            } as any;
          }
          return api(original);
        });
      }

      original._retry = true;
      refreshing = true;

      try {
        const rt = getRefreshToken();
        if (!rt) throw error;

        const resp = await axios.post(
          API_URL + AUTH_PATHS.refresh,
          { refresh_token: rt, refresh: rt },
          { timeout: 15000 }
        );

        const newAccess = (resp.data as any).access_token ?? (resp.data as any).access;
        if (!newAccess) throw error;

        localStorage.setItem('access_token', newAccess);
        resolveQueue(null, newAccess);

        original.headers = {
          ...(original.headers || {}),
          Authorization: `Bearer ${newAccess}`,
        } as any;

        return api(original);
      } catch (e) {
        resolveQueue(e, null);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        if (typeof window !== 'undefined') window.location.href = '/login';
        return Promise.reject(e);
      } finally {
        refreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export { api };
