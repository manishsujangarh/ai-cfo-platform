const API_BASE = process.env.NEXT_PUBLIC_API_URL || '/api';

export function getApiBase() {
    return API_BASE;
}

export function buildApiUrl(path: string) {
    const normalizedPath = path.startsWith('/') ? path : `/${path}`;
    return `${API_BASE}${normalizedPath}`;
}
