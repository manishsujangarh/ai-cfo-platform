'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

import { buildApiUrl } from '../lib/api';

export default function JournalEntriesPage() {
    const router = useRouter();
    const [entries, setEntries] = useState<any[]>([]);

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            router.replace('/');
            return;
        }

        fetch(buildApiUrl('/journal-entries'), { headers: { Authorization: `Bearer ${token}` } })
            .then((res) => res.json())
            .then((data) => setEntries(Array.isArray(data) ? data : []))
            .catch(() => setEntries([]));
    }, []);

    return (
        <main>
            <h1>Journal entries</h1>
            <p className="text-muted mb-6">Create and review journal entries from the dashboard.</p>
            <div className="card p-6">
                {entries.length === 0 ? <p className="text-muted">No journal entries found yet.</p> : entries.map((entry) => <div key={entry.id} className="mb-4" style={{ borderBottom: '1px solid rgba(148,163,184,.15)', paddingBottom: 10 }}>{entry.description}</div>)}
            </div>
        </main>
    );
}
