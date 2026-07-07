'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

import { buildApiUrl } from '../lib/api';

export default function AccountsPage() {
    const router = useRouter();
    const [accounts, setAccounts] = useState<any[]>([]);

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            router.replace('/');
            return;
        }

        fetch(buildApiUrl('/accounts'), { headers: { Authorization: `Bearer ${token}` } })
            .then((res) => res.json())
            .then((data) => setAccounts(Array.isArray(data) ? data : []))
            .catch(() => setAccounts([]));
    }, []);

    return (
        <main>
            <h1>Accounts</h1>
            <p className="text-muted mb-6">Manage your chart of accounts from the finance workspace.</p>
            <div className="card p-6">
                {accounts.length === 0 ? <p className="text-muted">No accounts found yet.</p> : accounts.map((account) => <div key={account.id} className="mb-4" style={{ borderBottom: '1px solid rgba(148,163,184,.15)', paddingBottom: 10 }}>{account.name} ({account.code})</div>)}
            </div>
        </main>
    );
}
