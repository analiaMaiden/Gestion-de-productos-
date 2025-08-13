/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-explicit-any */
import { defineStore } from 'pinia';
import { api } from '@/services/api';
import { AUTH_PATHS } from '@/services/config';
import type { LoginPayload, TokenResponse, User } from '@/types/auth';
import { jwtDecode } from 'jwt-decode';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    loading: false,
    isAuthenticated: !!localStorage.getItem('access_token'),
  }),
  actions: {
      async login(payload: LoginPayload) {
        this.loading = true;
        try {
          const username = payload.username ?? payload.email ?? '';
          const body = { username, password: payload.password };

          const { data } = await api.post<TokenResponse>(AUTH_PATHS.login, body, {
            headers: { 'Content-Type': 'application/json' },
          });

          const access = (data as any).access_token as string | undefined;
          if (!access) throw new Error('No llegó access_token');

          localStorage.setItem('access_token', access);
          this.isAuthenticated = true;

          try {
            const me = await api.get<User>(AUTH_PATHS.me);
            this.user = me.data;
          } catch {
            try {
              const decoded: any = jwtDecode(access);
              this.user = {
                id: decoded.sub ?? decoded.id,
                email: decoded.email,
                username: decoded.username ?? username,
                role: decoded.role,
              };
            } catch {
              this.user = { username };
            }
          }
          return true;                 // ⬅️ INDICA ÉXITO
        } catch (e) {
          this.isAuthenticated = false;
          this.user = null;
          return false;                // ⬅️ INDICA FALLA
        } finally {
          this.loading = false;
        }
      }
,

    logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token'); // por si acaso
      this.user = null;
      this.isAuthenticated = false;
    },

    async hydrate() {
      const token = localStorage.getItem('access_token');
      this.isAuthenticated = !!token;
      if (!token) return;
      try {
        const me = await api.get<User>(AUTH_PATHS.me);
        this.user = me.data;
      } catch {
        try {
          const decoded: any = jwtDecode(token);
          this.user = {
            id: decoded.sub ?? decoded.id,
            email: decoded.email,
            username: decoded.username,
            role: decoded.role,
          };
        } catch {
          this.user = { username: 'Usuario' };
        }
      }
    },
  },
});
