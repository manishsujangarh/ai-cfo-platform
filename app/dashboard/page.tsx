'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

import { buildApiUrl } from '../lib/api';

export default function DashboardPage() {
    const router = useRouter();
    const [orgName, setOrgName] = useState('');
    const [organizations, setOrganizations] = useState<any[]>([]);
    const [accounts, setAccounts] = useState<any[]>([]);
    const [journalEntries, setJournalEntries] = useState<any[]>([]);
    const [user, setUser] = useState<any>(null);
    const [activeOrgId, setActiveOrgId] = useState<number | null>(null);
    const [showEntryForm, setShowEntryForm] = useState(false);
    const [entryDescription, setEntryDescription] = useState('');
    const [entryReference, setEntryReference] = useState('');
    const [entryDate, setEntryDate] = useState(new Date().toISOString().slice(0, 10));
    const [entryAccountId, setEntryAccountId] = useState('');
    const [entryDebit, setEntryDebit] = useState('0');
    const [entryCredit, setEntryCredit] = useState('0');
    const [entrySubmitting, setEntrySubmitting] = useState(false);
    const [loading, setLoading] = useState(true);
    const [creating, setCreating] = useState(false);

    const getUserDisplay = (userData: any) => {

        if (!userData) return 'Authenticated user';
        if (userData.full_name) return userData.full_name;
        if (userData.email) return userData.email;
        return `User #${userData.id ?? ''}`.trim();
    };

    const authHeaders = () => ({
        Authorization: `Bearer ${localStorage.getItem('token') || ''}`,
    });

    const loadData = async () => {

        try {
            const [userRes, orgsRes, entriesRes] = await Promise.all([
                fetch(buildApiUrl('/users/me'), { headers: authHeaders() }),
                fetch(buildApiUrl('/organizations'), { headers: authHeaders() }),
                fetch(buildApiUrl('/journal-entries'), { headers: authHeaders() }),
            ]);

            const [userData, orgs, entriesData] = await Promise.all([
                userRes.json().catch(() => null),
                orgsRes.json().catch(() => []),
                entriesRes.json().catch(() => []),
            ]);

            setUser(userData);
            setOrganizations(Array.isArray(orgs) ? orgs : []);
            setJournalEntries(Array.isArray(entriesData) ? entriesData : []);
        } catch {
            // keep dashboard resilient
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            router.replace('/');
            return;
        }
        loadData();
    }, []);

    const createOrganization = async (event: React.FormEvent) => {
        event.preventDefault();
        setCreating(true);
        const response = await fetch(buildApiUrl('/organizations'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', ...authHeaders() },
            body: JSON.stringify({ name: orgName }),
        });
        const data = await response.json().catch(() => ({}));
        if (response.ok) {
            setOrgName('');
            loadData();
        }
        setCreating(false);
    };

    const openOrganization = async (organizationId: number) => {
        setActiveOrgId(organizationId);
        setShowEntryForm(false);
        const response = await fetch(buildApiUrl(`/accounts?organization_id=${organizationId}`), {
            headers: authHeaders(),
        });
        const data = await response.json().catch(() => []);
        setAccounts(Array.isArray(data) ? data : []);
    };

    const submitEntry = async (event: React.FormEvent) => {
        event.preventDefault();
        if (!activeOrgId) return;

        setEntrySubmitting(true);
        const response = await fetch(buildApiUrl('/journal-entries'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', ...authHeaders() },
            body: JSON.stringify({
                organization_id: activeOrgId,
                entry_date: entryDate,
                reference: entryReference || null,
                description: entryDescription,
                lines: [
                    {
                        account_id: Number(entryAccountId),
                        description: entryDescription,
                        debit: entryDebit || '0',
                        credit: entryCredit || '0',
                    },
                ],
            }),
        });

        const data = await response.json().catch(() => ({}));
        if (response.ok) {
            setEntryDescription('');
            setEntryReference('');
            setEntryDate(new Date().toISOString().slice(0, 10));
            setEntryAccountId('');
            setEntryDebit('0');
            setEntryCredit('0');
            setShowEntryForm(false);
            loadData();
        }
        setEntrySubmitting(false);
    };

    return (
        <main>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
                <div>
                    <h1 style={{ margin: 0 }}>Company dashboard</h1>
                    <p className="text-muted">{user ? `Signed in as ${getUserDisplay(user)}` : 'Create your organization, review accounts, and track journal entries.'}</p>
                </div>
                <button className="btn btn-secondary" onClick={() => { localStorage.removeItem('token'); router.replace('/'); }}>Logout</button>
            </div>

            <div className="grid grid-2 mb-6">
                <div className="card p-6">
                    <h3>Signed-in user</h3>
                    <p className="text-muted">{user ? getUserDisplay(user) : 'Loading user…'}</p>
                    <p className="text-muted">Email: {user?.email || '—'}</p>
                    <p className="text-muted">User ID: {user?.id ?? '—'}</p>
                </div>
                <div className="card p-6">
                    <h3>Create organization</h3>
                    <form onSubmit={createOrganization} className="space-y">
                        <input value={orgName} onChange={(e) => setOrgName(e.target.value)} placeholder="Acme Holdings" style={{ width: '100%', padding: 12, borderRadius: 12, border: '1px solid rgba(148,163,184,.2)', background: '#020617', color: 'white' }} />
                        <button className="btn btn-primary" disabled={creating}>{creating ? 'Creating…' : 'Create company'}</button>
                    </form>
                </div>
                <div className="card p-6">
                    <h3>Overview</h3>
                    <p className="text-muted">Organizations: {organizations.length}</p>
                    <p className="text-muted">Accounts: {accounts.length}</p>
                    <p className="text-muted">Journal entries: {journalEntries.length}</p>
                </div>
            </div>

            {!loading ? (
                <div className="grid grid-2">
                    <div className="card p-6">
                        <h3>Organizations</h3>
                        <div style={{ maxHeight: 320, overflowY: 'auto', paddingRight: 6 }}>
                            {organizations.length === 0 ? <p className="text-muted">No organizations yet.</p> : organizations.map((org) => (
                                <div key={org.id} className="mb-4" style={{ borderBottom: '1px solid rgba(148,163,184,.15)', paddingBottom: 10 }}>
                                    <button className="btn btn-secondary" style={{ width: '100%', justifyContent: 'flex-start', marginBottom: 8 }} onClick={() => openOrganization(org.id)}>
                                        <strong>{org.name}</strong>
                                    </button>
                                    <div className="text-muted">ID: {org.id}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="card p-6">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                            <h3 style={{ margin: 0 }}>Accounts for organization</h3>
                            {activeOrgId !== null ? <button className="btn btn-primary" onClick={() => setShowEntryForm((value) => !value)}>{showEntryForm ? 'Hide form' : 'Add entry'}</button> : null}
                        </div>
                        {showEntryForm && activeOrgId !== null ? (
                            <form onSubmit={submitEntry} className="space-y" style={{ marginBottom: 12 }}>
                                <div>
                                    <label className="text-sm text-muted">Description</label>
                                    <input value={entryDescription} onChange={(e) => setEntryDescription(e.target.value)} placeholder="Rent expense entry" style={{ width: '100%', padding: 10, borderRadius: 10, border: '1px solid rgba(148,163,184,.2)', background: '#020617', color: 'white' }} required />
                                </div>
                                <div className="grid grid-2">
                                    <div>
                                        <label className="text-sm text-muted">Date</label>
                                        <input type="date" value={entryDate} onChange={(e) => setEntryDate(e.target.value)} style={{ width: '100%', padding: 10, borderRadius: 10, border: '1px solid rgba(148,163,184,.2)', background: '#020617', color: 'white' }} required />
                                    </div>
                                    <div>
                                        <label className="text-sm text-muted">Reference</label>
                                        <input value={entryReference} onChange={(e) => setEntryReference(e.target.value)} placeholder="INV-001" style={{ width: '100%', padding: 10, borderRadius: 10, border: '1px solid rgba(148,163,184,.2)', background: '#020617', color: 'white' }} />
                                    </div>
                                </div>
                                <div className="grid grid-2">
                                    <div>
                                        <label className="text-sm text-muted">Account</label>
                                        <select value={entryAccountId} onChange={(e) => setEntryAccountId(e.target.value)} style={{ width: '100%', padding: 10, borderRadius: 10, border: '1px solid rgba(148,163,184,.2)', background: '#020617', color: 'white' }} required>
                                            <option value="">Select account</option>
                                            {accounts.map((account) => (
                                                <option key={account.id} value={account.id}>{account.code} - {account.name} ({account.type})</option>
                                            ))}
                                        </select>
                                    </div>
                                    <div>
                                        <label className="text-sm text-muted">Debit</label>
                                        <input value={entryDebit} onChange={(e) => setEntryDebit(e.target.value)} placeholder="0" style={{ width: '100%', padding: 10, borderRadius: 10, border: '1px solid rgba(148,163,184,.2)', background: '#020617', color: 'white' }} />
                                    </div>
                                </div>
                                <div>
                                    <label className="text-sm text-muted">Credit</label>
                                    <input value={entryCredit} onChange={(e) => setEntryCredit(e.target.value)} placeholder="0" style={{ width: '100%', padding: 10, borderRadius: 10, border: '1px solid rgba(148,163,184,.2)', background: '#020617', color: 'white' }} />
                                </div>
                                <button className="btn btn-primary" disabled={entrySubmitting}>{entrySubmitting ? 'Saving…' : 'Save entry'}</button>
                            </form>
                        ) : null}
                        <div style={{ maxHeight: 320, overflowY: 'auto', paddingRight: 6 }}>
                            {activeOrgId === null ? <p className="text-muted">Select an organization to view accounts.</p> : accounts.length === 0 ? <p className="text-muted">No accounts found for this organization.</p> : accounts.map((account) => (
                                <div key={account.id} className="mb-3" style={{ border: '1px solid rgba(148,163,184,.15)', borderRadius: 12, padding: 10 }}>
                                    <div>
                                        <strong>{account.name}</strong>
                                        <div className="text-muted">Organization ID: {account.organization_id} • Code: {account.code} • Type: {account.type}</div>
                                    </div>
                                    <div style={{ marginTop: 8 }}>
                                        <div className="text-muted">Entries</div>
                                        <div style={{ maxHeight: 120, overflowY: 'auto', marginTop: 6 }}>
                                            {journalEntries.filter((entry) => entry.organization_id === activeOrgId).slice(0, 6).map((entry) => (
                                                <div key={entry.id} className="mb-2" style={{ borderBottom: '1px solid rgba(148,163,184,.1)', paddingBottom: 6 }}>
                                                    {entry.description || 'Journal entry'}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            ) : <p className="text-muted">Loading dashboard…</p>}
        </main>
    );
}
