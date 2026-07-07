'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

import { buildApiUrl } from './lib/api';

export default function HomePage() {
    const router = useRouter();
    const [email, setEmail] = useState('owner@example.com');
    const [password, setPassword] = useState('password123');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
        if (token) router.replace('/dashboard');
    }, []);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setLoading(true);
        setError('');

        try {
            const form = new URLSearchParams();
            form.append('username', email);
            form.append('password', password);
            form.append('grant_type', 'password');

            const response = await fetch(buildApiUrl('/auth/login'), {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: form.toString(),
            });

            const text = await response.text();
            let data: any = {};
            if (text) {
                try {
                    data = JSON.parse(text);
                } catch {
                    data = { detail: text };
                }
            }

            if (!response.ok) throw new Error(data.detail || 'Login failed');

            localStorage.setItem('token', data.access_token);
            router.push('/dashboard');
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <main style={{ display: 'grid', minHeight: '100vh', placeItems: 'center', padding: 24 }}>
            <div className="card p-6" style={{ width: '100%', maxWidth: 460 }}>
                <h1 style={{ fontSize: 32, marginBottom: 8 }}>AI CFO SaaS</h1>
                <p className="text-muted mb-6">Owner login, company setup, and finance operations in one place.</p>
                <form onSubmit={handleSubmit} className="space-y">
                    <div>
                        <label className="text-sm text-muted">Email</label>
                        <input value={email} onChange={(e) => setEmail(e.target.value)} className="p-4" style={{ width: '100%', marginTop: 6, borderRadius: 12, border: '1px solid rgba(148,163,184,.2)', background: '#020617', color: 'white' }} />
                    </div>
                    <div>
                        <label className="text-sm text-muted">Password</label>
                        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="p-4" style={{ width: '100%', marginTop: 6, borderRadius: 12, border: '1px solid rgba(148,163,184,.2)', background: '#020617', color: 'white' }} />
                    </div>
                    {error ? <div className="text-sm" style={{ color: '#fda4af' }}>{error}</div> : null}
                    <button className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>{loading ? 'Signing in…' : 'Sign in'}</button>
                </form>
            </div>
        </main>
    );
}
