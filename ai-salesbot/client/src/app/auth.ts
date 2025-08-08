import api from './api'

const ACCESS_KEY = 'access_token'
const REFRESH_KEY = 'refresh_token'

export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_KEY)
}

export function setTokens(access: string, refresh: string) {
  localStorage.setItem(ACCESS_KEY, access)
  localStorage.setItem(REFRESH_KEY, refresh)
}

export async function loginWithVkUserId(vk_user_id: string) {
  const { data } = await api.post('/v1/auth/login', { vk_user_id })
  setTokens(data.access, data.refresh)
}