export interface User {
  id?: number | string;
  password?: string;
  username?: string;
  role?: string;
  [k: string]: unknown;
}

export interface LoginPayload {
  username?: string;
  email?: string;
  password: string;
}

export interface TokenResponse {
  access_token?: string;
  access?: string;
  refresh_token?: string;
  refresh?: string;
  [k: string]: unknown;
}
