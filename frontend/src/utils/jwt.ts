export interface TokenPayload {
  sub: string
  role: string
  exp: number
}

export function decodeToken(token: string): TokenPayload | null {
  try {
    const payload = token.split('.')[1]
    return JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')))
  } catch {
    return null
  }
}