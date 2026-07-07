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
    const [customers, setCustomers] = useState<any[]>([]);
    const [vendors, setVendors] = useState<any[]>([]);
    const [customerName, setCustomerName] = useState('');
    const [customerEmail, setCustomerEmail] = useState('');
    const [customerPhone, setCustomerPhone] = useState('');
    const [customerAddress, setCustomerAddress] = useState('');
    const [vendorName, setVendorName] = useState('');
    const [vendorEmail, setVendorEmail] = useState('');
    const [vendorPhone, setVendorPhone] = useState('');
    const [vendorAddress, setVendorAddress] = useState('');
    const [vendorGstNumber, setVendorGstNumber] = useState('');
    const [creatingCustomer, setCreatingCustomer] = useState(false);
    const [creatingVendor, setCreatingVendor] = useState(false);
    const [statusMessage, setStatusMessage] = useState<string | null>(null);
    const [chatOpen, setChatOpen] = useState(false);
    const [chatInput, setChatInput] = useState('');
    const [chatMessages, setChatMessages] = useState<Array<{ role: 'assistant' | 'user'; content: string }>>([
        { role: 'assistant', content: 'Hi! I can help summarize your organization, draft journal entries, and suggest next actions.' },
    ]);
    const [chatBusy, setChatBusy] = useState(false);
    const [activeView, setActiveView] = useState<'dashboard' | 'organizations' | 'customers' | 'vendors' | 'journal' | 'accounts'>('dashboard');
    const [detailTab, setDetailTab] = useState<'customers' | 'vendors' | 'journal' | 'accounts'>('customers');
    const [orgPage, setOrgPage] = useState(1);
    const [showCustomerForm, setShowCustomerForm] = useState(false);
    const [showVendorForm, setShowVendorForm] = useState(false);
    const [showProfileSettings, setShowProfileSettings] = useState(false);
    const [theme, setTheme] = useState<'dark' | 'light'>('dark');
    const [userRole, setUserRole] = useState<'admin' | 'manager' | 'viewer'>('admin');

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

        const savedTheme = localStorage.getItem('erp-theme') as 'dark' | 'light' | null;
        const savedRole = localStorage.getItem('erp-role') as 'admin' | 'manager' | 'viewer' | null;
        if (savedTheme) {
            setTheme(savedTheme);
        }
        if (savedRole) {
            setUserRole(savedRole);
        }

        loadData();
    }, []);

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('erp-theme', theme);
    }, [theme]);

    useEffect(() => {
        localStorage.setItem('erp-role', userRole);
    }, [userRole]);

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

    const loadOrganizationDetails = async (organizationId: number) => {
        const [accountsRes, customersRes, vendorsRes] = await Promise.all([
            fetch(buildApiUrl(`/accounts?organization_id=${organizationId}`), { headers: authHeaders() }),
            fetch(buildApiUrl('/customers'), { headers: authHeaders() }),
            fetch(buildApiUrl('/vendors'), { headers: authHeaders() }),
        ]);

        const [accountsData, customersData, vendorsData] = await Promise.all([
            accountsRes.json().catch(() => []),
            customersRes.json().catch(() => []),
            vendorsRes.json().catch(() => []),
        ]);

        setAccounts(Array.isArray(accountsData) ? accountsData : []);
        setCustomers(Array.isArray(customersData) ? customersData.filter((customer: any) => customer.organization_id === organizationId) : []);
        setVendors(Array.isArray(vendorsData) ? vendorsData.filter((vendor: any) => vendor.organization_id === organizationId) : []);
    };

    const openOrganization = async (organizationId: number) => {
        setActiveOrgId(organizationId);
        setShowEntryForm(false);
        setStatusMessage(null);
        await loadOrganizationDetails(organizationId);
    };

    const createCustomer = async (event: React.FormEvent) => {
        event.preventDefault();
        if (!activeOrgId) return;

        setCreatingCustomer(true);
        const response = await fetch(buildApiUrl('/customers'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', ...authHeaders() },
            body: JSON.stringify({
                organization_id: activeOrgId,
                name: customerName,
                email: customerEmail || null,
                phone: customerPhone || null,
                address: customerAddress || null,
            }),
        });

        if (response.ok) {
            setCustomerName('');
            setCustomerEmail('');
            setCustomerPhone('');
            setCustomerAddress('');
            setStatusMessage('Customer created successfully.');
            await loadOrganizationDetails(activeOrgId);
        } else {
            setStatusMessage('Unable to create customer.');
        }
        setCreatingCustomer(false);
    };

    const createVendor = async (event: React.FormEvent) => {
        event.preventDefault();
        if (!activeOrgId) return;

        setCreatingVendor(true);
        const response = await fetch(buildApiUrl('/vendors'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', ...authHeaders() },
            body: JSON.stringify({
                organization_id: activeOrgId,
                name: vendorName,
                email: vendorEmail || null,
                phone: vendorPhone || null,
                address: vendorAddress || null,
                gst_number: vendorGstNumber || null,
            }),
        });

        if (response.ok) {
            setVendorName('');
            setVendorEmail('');
            setVendorPhone('');
            setVendorAddress('');
            setVendorGstNumber('');
            setStatusMessage('Vendor created successfully.');
            await loadOrganizationDetails(activeOrgId);
        } else {
            setStatusMessage('Unable to create vendor.');
        }
        setCreatingVendor(false);
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

    const sendChatMessage = async (event?: React.FormEvent) => {
        event?.preventDefault();
        if (!chatInput.trim()) return;

        const userMessage = chatInput.trim();
        setChatMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
        setChatInput('');
        setChatBusy(true);

        try {
            const prompt = activeOrgId
                ? `Help with organization ${activeOrgId}. User asked: ${userMessage}`
                : `Help with workspace. User asked: ${userMessage}`;

            const response = await fetch(buildApiUrl('/agents'), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', ...authHeaders() },
                body: JSON.stringify({
                    organization_id: activeOrgId,
                    message: prompt,
                    user_id: user?.id,
                }),
            });

            const data = await response.json().catch(() => ({}));
            const assistantReply = response.ok && data?.response
                ? data.response
                : 'I can help with journal entries, customer records, vendors, and account summaries.';

            setChatMessages((prev) => [...prev, { role: 'assistant', content: assistantReply }]);
        } catch {
            setChatMessages((prev) => [...prev, { role: 'assistant', content: 'I am unavailable right now. Please try again shortly.' }]);
        } finally {
            setChatBusy(false);
        }
    };

    const orgPageSize = 5;
    const totalOrgPages = Math.max(1, Math.ceil(organizations.length / orgPageSize));
    const visibleOrganizations = organizations.slice((orgPage - 1) * orgPageSize, orgPage * orgPageSize);
    const selectedOrganization = organizations.find((org) => org.id === activeOrgId) ?? null;
    const canManage = userRole !== 'viewer';
    const canCreateOrganization = userRole === 'admin' || userRole === 'manager';
    const roleLabel = userRole === 'admin' ? 'Administrator' : userRole === 'manager' ? 'Manager' : 'Viewer';

    const moduleCards = [
        {
            title: 'Organizations',
            icon: '🏢',
            description: 'Create and switch between companies in one place.',
            count: organizations.length,
            status: organizations.length ? 'Live' : 'Ready',
        },
        {
            title: 'Customers',
            icon: '👥',
            description: 'Add and view customers for the active organization.',
            count: customers.length,
            status: activeOrgId ? 'Live' : 'Ready',
        },
        {
            title: 'Vendors',
            icon: '🏭',
            description: 'Keep supplier records simple and searchable.',
            count: vendors.length,
            status: activeOrgId ? 'Live' : 'Ready',
        },
        {
            title: 'Chart of Accounts',
            icon: '📚',
            description: 'Manage accounts and financial categories.',
            count: accounts.length,
            status: activeOrgId ? 'Live' : 'Ready',
        },
        {
            title: 'Journal Entries',
            icon: '🧾',
            description: 'Record vouchers with debit and credit lines.',
            count: journalEntries.length,
            status: journalEntries.length ? 'Live' : 'Ready',
        },
        {
            title: 'Invoices',
            icon: '🧾',
            description: 'Invoice workflows for sales and billing.',
            count: '—',
            status: 'Ready',
        },
        {
            title: 'Payments',
            icon: '💳',
            description: 'Track payments received and made.',
            count: '—',
            status: 'Ready',
        },
        {
            title: 'Expenses',
            icon: '🛒',
            description: 'Capture daily spending and approvals.',
            count: '—',
            status: 'Ready',
        },
        {
            title: 'Bills',
            icon: '📄',
            description: 'Manage purchase bills and vendor dues.',
            count: '—',
            status: 'Ready',
        },
    ];

    return (
        <main>
            <div className="workspace-layout">
                <aside className="workspace-sidebar card p-6">
                    <div className="dashboard-topbar" style={{ marginBottom: 10 }}>
                        <div>
                            <div className="eyebrow">ERP workspace</div>
                            <h2 style={{ margin: 0 }}>Modules</h2>
                        </div>
                        <button className="btn btn-secondary" onClick={() => { localStorage.removeItem('token'); router.replace('/'); }}>Logout</button>
                    </div>

                    <div className="profile-settings-card card p-4">
                        <div className="section-header">
                            <div>
                                <div className="eyebrow">Profile</div>
                                <h3 style={{ margin: 0 }}>{user ? getUserDisplay(user) : 'Your profile'}</h3>
                            </div>
                            <button className="icon-btn" onClick={() => setShowProfileSettings((value) => !value)} title="Open profile settings">⚙️</button>
                        </div>
                        <p className="text-muted" style={{ margin: '0 0 10px' }}>{user?.email || 'Configure your access and workspace appearance.'}</p>
                        {showProfileSettings ? (
                            <div className="space-y">
                                <label className="text-sm text-muted">
                                    Role
                                    <select value={userRole} onChange={(e) => setUserRole(e.target.value as 'admin' | 'manager' | 'viewer')}>
                                        <option value="admin">Administrator</option>
                                        <option value="manager">Manager</option>
                                        <option value="viewer">Viewer</option>
                                    </select>
                                </label>
                                <div className="theme-switch-row">
                                    <span className="text-sm text-muted">Theme</span>
                                    <button className="btn btn-secondary" onClick={() => setTheme((value) => value === 'dark' ? 'light' : 'dark')}>
                                        {theme === 'dark' ? '☀️ Light' : '🌙 Dark'}
                                    </button>
                                </div>
                            </div>
                        ) : (
                            <div className="theme-switch-row">
                                <span className="text-sm text-muted">{roleLabel}</span>
                                <span className="module-pill">{theme === 'dark' ? 'Dark mode' : 'Light mode'}</span>
                            </div>
                        )}
                    </div>

                    <div className="stack-list">
                        {[
                            { key: 'dashboard', label: 'Dashboard', icon: '📊' },
                            { key: 'organizations', label: 'Organizations', icon: '🏢' },
                            { key: 'customers', label: 'Customers', icon: '👥' },
                            { key: 'vendors', label: 'Vendors', icon: '🏭' },
                            { key: 'journal', label: 'Journal Entries', icon: '🧾' },
                            { key: 'accounts', label: 'Accounts', icon: '📚' },
                        ].map((item) => (
                            <button
                                key={item.key}
                                className={`workspace-nav-item ${activeView === item.key ? 'active' : ''}`}
                                onClick={() => {
                                    setActiveView(item.key as 'dashboard' | 'organizations' | 'customers' | 'vendors' | 'journal' | 'accounts');
                                    if (item.key === 'customers' || item.key === 'vendors' || item.key === 'journal' || item.key === 'accounts') {
                                        setDetailTab(item.key as 'customers' | 'vendors' | 'journal' | 'accounts');
                                    }
                                }}
                            >
                                <span>{item.icon}</span>
                                <span>{item.label}</span>
                            </button>
                        ))}
                    </div>

                    <div className="workspace-sidebar-section">
                        <div className="section-header">
                            <div>
                                <div className="eyebrow">Organizations</div>
                                <h3 style={{ margin: 0 }}>Company list</h3>
                            </div>
                        </div>
                        {organizations.length === 0 ? (
                            <p className="text-muted">No organizations yet.</p>
                        ) : (
                            <>
                                {visibleOrganizations.map((org) => (
                                    <button
                                        key={org.id}
                                        className={`workspace-org-item ${activeOrgId === org.id ? 'active' : ''}`}
                                        onClick={() => openOrganization(org.id)}
                                    >
                                        <div>
                                            <strong>{org.name}</strong>
                                            <div className="text-muted text-sm">Org #{org.id}</div>
                                        </div>
                                        <span className="module-pill">Open</span>
                                    </button>
                                ))}
                                <div className="workspace-pagination">
                                    <button className="icon-btn" disabled={orgPage === 1} onClick={() => setOrgPage((page) => Math.max(1, page - 1))}>←</button>
                                    <span className="text-sm text-muted">Page {orgPage} / {totalOrgPages}</span>
                                    <button className="icon-btn" disabled={orgPage >= totalOrgPages} onClick={() => setOrgPage((page) => Math.min(totalOrgPages, page + 1))}>→</button>
                                </div>
                            </>
                        )}
                    </div>
                </aside>

                <section className="workspace-main">
                    {activeView === 'dashboard' ? (
                        <div className="dashboard-shell">
                            <div className="hero-card card p-6">
                                <div className="hero-copy">
                                    <div className="eyebrow">Simple ERP</div>
                                    <h2 style={{ margin: 0 }}>Easy finance workspace for every user</h2>
                                    <p className="text-muted">Create organizations, manage customers and vendors, record accounts and journal entries, and keep your books clear.</p>
                                </div>
                                <div className="hero-actions">
                                    <button className="btn btn-primary" onClick={() => setActiveView('organizations')} disabled={!canCreateOrganization}>{canCreateOrganization ? 'Manage organizations' : 'View only access'}</button>
                                    <button className="btn btn-secondary" onClick={() => { setActiveView('journal'); setShowEntryForm(true); }} disabled={!canManage}>Add journal entry</button>
                                </div>
                            </div>

                            <div className="module-grid">
                                {moduleCards.map((module) => (
                                    <div key={module.title} className="module-card card p-6">
                                        <div className="card-icon">{module.icon}</div>
                                        <div className="module-title-row">
                                            <h3 style={{ margin: 0 }}>{module.title}</h3>
                                            <span className="module-pill">{module.status}</span>
                                        </div>
                                        <p className="text-muted" style={{ margin: 0 }}>{module.description}</p>
                                        <div className="module-meta">
                                            <strong>{module.count}</strong>
                                            <span className="text-muted">items</span>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            <div className="grid grid-2">
                                <div className="card p-6 dashboard-card">
                                    <div className="card-icon">👤</div>
                                    <h3>Profile</h3>
                                    <p className="text-muted">{user ? getUserDisplay(user) : 'Loading user…'}</p>
                                    <p className="text-muted">Email: {user?.email || '—'}</p>
                                    <p className="text-muted">User ID: {user?.id ?? '—'}</p>
                                </div>
                                <div className="card p-6 dashboard-card">
                                    <div className="card-icon">🏢</div>
                                    <h3>Create organization</h3>
                                    {canCreateOrganization ? (
                                        <form onSubmit={createOrganization} className="space-y">
                                            <input value={orgName} onChange={(e) => setOrgName(e.target.value)} placeholder="Acme Holdings" />
                                            <button className="btn btn-primary" disabled={creating}>{creating ? 'Creating…' : 'Create company'}</button>
                                        </form>
                                    ) : (
                                        <p className="text-muted">Only administrators and managers can create organizations from this workspace.</p>
                                    )}
                                </div>
                            </div>
                        </div>
                    ) : null}

                    {activeView === 'organizations' ? (
                        <div className="card p-6 dashboard-card">
                            <div className="workspace-header">
                                <div>
                                    <div className="eyebrow">Organizations</div>
                                    <h2 style={{ margin: 0 }}>Company directory</h2>
                                </div>
                                <button className="btn btn-primary" onClick={() => setActiveView('dashboard')} disabled={!canCreateOrganization}>{canCreateOrganization ? 'Create organization' : 'View only'}</button>
                            </div>
                            <p className="text-muted">Select a company from the list to view customer, vendor, journal entry, and account records.</p>

                            <div className="workspace-tabs">
                                {[
                                    { key: 'customers', label: 'Customers' },
                                    { key: 'vendors', label: 'Vendors' },
                                    { key: 'journal', label: 'Journal Entries' },
                                    { key: 'accounts', label: 'Accounts' },
                                ].map((tab) => (
                                    <button
                                        key={tab.key}
                                        className={`tab-pill ${detailTab === tab.key ? 'active' : ''}`}
                                        onClick={() => {
                                            setDetailTab(tab.key as 'customers' | 'vendors' | 'journal' | 'accounts');
                                            setActiveView(tab.key as 'dashboard' | 'organizations' | 'customers' | 'vendors' | 'journal' | 'accounts');
                                        }}
                                    >
                                        {tab.label}
                                    </button>
                                ))}
                            </div>

                            {selectedOrganization ? (
                                <div className="sub-card" style={{ marginTop: 12 }}>
                                    <div className="sub-card-header">
                                        <div>
                                            <h3 style={{ margin: 0 }}>{selectedOrganization.name}</h3>
                                            <div className="text-muted text-sm">Open for {detailTab === 'customers' ? 'customer management' : detailTab === 'vendors' ? 'vendor management' : detailTab === 'journal' ? 'journal entry review' : 'account review'}</div>
                                        </div>
                                    </div>
                                    {detailTab === 'customers' ? (
                                        <div className="stack-list">
                                            <div className="workspace-header">
                                                <h4 style={{ margin: 0 }}>Customers</h4>
                                                <button className="btn btn-primary" onClick={() => setShowCustomerForm((value) => !value)} disabled={!canManage}>Add customer</button>
                                            </div>
                                            {showCustomerForm ? (
                                                <form onSubmit={createCustomer} className="space-y">
                                                    <input value={customerName} onChange={(e) => setCustomerName(e.target.value)} placeholder="Customer name" required />
                                                    <input value={customerEmail} onChange={(e) => setCustomerEmail(e.target.value)} placeholder="Email" />
                                                    <input value={customerPhone} onChange={(e) => setCustomerPhone(e.target.value)} placeholder="Phone" />
                                                    <input value={customerAddress} onChange={(e) => setCustomerAddress(e.target.value)} placeholder="Address" />
                                                    <button className="btn btn-primary" disabled={creatingCustomer}>{creatingCustomer ? 'Creating…' : 'Create customer'}</button>
                                                </form>
                                            ) : null}
                                            {customers.length === 0 ? <p className="text-muted">No customers yet.</p> : customers.map((customer) => (
                                                <div key={customer.id} className="account-card">
                                                    <div>
                                                        <strong>{customer.name}</strong>
                                                        <div className="text-muted text-sm">{customer.email || 'No email'}</div>
                                                    </div>
                                                    <span className="module-pill">Customer</span>
                                                </div>
                                            ))}
                                        </div>
                                    ) : null}

                                    {detailTab === 'vendors' ? (
                                        <div className="stack-list">
                                            <div className="workspace-header">
                                                <h4 style={{ margin: 0 }}>Vendors</h4>
                                                <button className="btn btn-primary" onClick={() => setShowVendorForm((value) => !value)} disabled={!canManage}>Add vendor</button>
                                            </div>
                                            {showVendorForm ? (
                                                <form onSubmit={createVendor} className="space-y">
                                                    <input value={vendorName} onChange={(e) => setVendorName(e.target.value)} placeholder="Vendor name" required />
                                                    <input value={vendorEmail} onChange={(e) => setVendorEmail(e.target.value)} placeholder="Email" />
                                                    <input value={vendorPhone} onChange={(e) => setVendorPhone(e.target.value)} placeholder="Phone" />
                                                    <input value={vendorAddress} onChange={(e) => setVendorAddress(e.target.value)} placeholder="Address" />
                                                    <input value={vendorGstNumber} onChange={(e) => setVendorGstNumber(e.target.value)} placeholder="GST number" />
                                                    <button className="btn btn-primary" disabled={creatingVendor}>{creatingVendor ? 'Creating…' : 'Create vendor'}</button>
                                                </form>
                                            ) : null}
                                            {vendors.length === 0 ? <p className="text-muted">No vendors yet.</p> : vendors.map((vendor) => (
                                                <div key={vendor.id} className="account-card">
                                                    <div>
                                                        <strong>{vendor.name}</strong>
                                                        <div className="text-muted text-sm">{vendor.email || 'No email'}</div>
                                                    </div>
                                                    <span className="module-pill">Vendor</span>
                                                </div>
                                            ))}
                                        </div>
                                    ) : null}

                                    {detailTab === 'journal' ? (
                                        <div className="stack-list">
                                            <div className="workspace-header">
                                                <h4 style={{ margin: 0 }}>Journal entries</h4>
                                                <button className="btn btn-primary" onClick={() => { setShowEntryForm((value) => !value); }} disabled={!canManage}>Add entry</button>
                                            </div>
                                            {showEntryForm ? (
                                                <form onSubmit={submitEntry} className="space-y" style={{ marginBottom: 12 }}>
                                                    <input value={entryDescription} onChange={(e) => setEntryDescription(e.target.value)} placeholder="Rent expense entry" required />
                                                    <div className="grid grid-2">
                                                        <div>
                                                            <label className="text-sm text-muted">Date</label>
                                                            <input type="date" value={entryDate} onChange={(e) => setEntryDate(e.target.value)} required />
                                                        </div>
                                                        <div>
                                                            <label className="text-sm text-muted">Reference</label>
                                                            <input value={entryReference} onChange={(e) => setEntryReference(e.target.value)} placeholder="INV-001" />
                                                        </div>
                                                    </div>
                                                    <div className="grid grid-2">
                                                        <div>
                                                            <label className="text-sm text-muted">Account</label>
                                                            <select value={entryAccountId} onChange={(e) => setEntryAccountId(e.target.value)} required>
                                                                <option value="">Select account</option>
                                                                {accounts.map((account) => (
                                                                    <option key={account.id} value={account.id}>{account.code} - {account.name} ({account.type})</option>
                                                                ))}
                                                            </select>
                                                        </div>
                                                        <div>
                                                            <label className="text-sm text-muted">Debit</label>
                                                            <input value={entryDebit} onChange={(e) => setEntryDebit(e.target.value)} placeholder="0" />
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <label className="text-sm text-muted">Credit</label>
                                                        <input value={entryCredit} onChange={(e) => setEntryCredit(e.target.value)} placeholder="0" />
                                                    </div>
                                                    <button className="btn btn-primary" disabled={entrySubmitting}>{entrySubmitting ? 'Saving…' : 'Save entry'}</button>
                                                </form>
                                            ) : null}
                                            {journalEntries.length === 0 ? <p className="text-muted">No journal entries yet.</p> : journalEntries.map((entry) => (
                                                <div key={entry.id} className="account-card">
                                                    <div>
                                                        <strong>{entry.description || 'Journal entry'}</strong>
                                                        <div className="text-muted text-sm">{entry.entry_date || '—'} • Ref {entry.reference || '—'}</div>
                                                    </div>
                                                    <span className="module-pill">Entry</span>
                                                </div>
                                            ))}
                                        </div>
                                    ) : null}

                                    {detailTab === 'accounts' ? (
                                        <div className="stack-list">
                                            <div className="workspace-header">
                                                <h4 style={{ margin: 0 }}>Accounts</h4>
                                            </div>
                                            {accounts.length === 0 ? <p className="text-muted">No accounts found.</p> : accounts.map((account) => (
                                                <div key={account.id} className="account-card">
                                                    <div>
                                                        <strong>{account.name}</strong>
                                                        <div className="text-muted text-sm">{account.code} • {account.type}</div>
                                                    </div>
                                                    <span className="module-pill">Account</span>
                                                </div>
                                            ))}
                                        </div>
                                    ) : null}
                                </div>
                            ) : (
                                <p className="text-muted">Select an organization from the left to begin.</p>
                            )}
                        </div>
                    ) : null}

                    {activeView === 'customers' ? (
                        <div className="card p-6 dashboard-card">
                            <div className="workspace-header">
                                <div>
                                    <div className="eyebrow">Customers</div>
                                    <h2 style={{ margin: 0 }}>Customer records</h2>
                                </div>
                                <button className="btn btn-primary" onClick={() => setShowCustomerForm((value) => !value)} disabled={!canManage}>Add customer</button>
                            </div>
                            {showCustomerForm ? (
                                <form onSubmit={createCustomer} className="space-y" style={{ marginBottom: 12 }}>
                                    <input value={customerName} onChange={(e) => setCustomerName(e.target.value)} placeholder="Customer name" required />
                                    <input value={customerEmail} onChange={(e) => setCustomerEmail(e.target.value)} placeholder="Email" />
                                    <input value={customerPhone} onChange={(e) => setCustomerPhone(e.target.value)} placeholder="Phone" />
                                    <input value={customerAddress} onChange={(e) => setCustomerAddress(e.target.value)} placeholder="Address" />
                                    <button className="btn btn-primary" disabled={creatingCustomer}>{creatingCustomer ? 'Creating…' : 'Create customer'}</button>
                                </form>
                            ) : null}
                            {customers.length === 0 ? <p className="text-muted">No customers available.</p> : customers.map((customer) => (
                                <div key={customer.id} className="account-card">
                                    <div>
                                        <strong>{customer.name}</strong>
                                        <div className="text-muted text-sm">{customer.email || 'No email'}</div>
                                    </div>
                                    <span className="module-pill">Customer</span>
                                </div>
                            ))}
                        </div>
                    ) : null}

                    {activeView === 'vendors' ? (
                        <div className="card p-6 dashboard-card">
                            <div className="workspace-header">
                                <div>
                                    <div className="eyebrow">Vendors</div>
                                    <h2 style={{ margin: 0 }}>Vendor records</h2>
                                </div>
                                <button className="btn btn-primary" onClick={() => setShowVendorForm((value) => !value)} disabled={!canManage}>Add vendor</button>
                            </div>
                            {showVendorForm ? (
                                <form onSubmit={createVendor} className="space-y" style={{ marginBottom: 12 }}>
                                    <input value={vendorName} onChange={(e) => setVendorName(e.target.value)} placeholder="Vendor name" required />
                                    <input value={vendorEmail} onChange={(e) => setVendorEmail(e.target.value)} placeholder="Email" />
                                    <input value={vendorPhone} onChange={(e) => setVendorPhone(e.target.value)} placeholder="Phone" />
                                    <input value={vendorAddress} onChange={(e) => setVendorAddress(e.target.value)} placeholder="Address" />
                                    <input value={vendorGstNumber} onChange={(e) => setVendorGstNumber(e.target.value)} placeholder="GST number" />
                                    <button className="btn btn-primary" disabled={creatingVendor}>{creatingVendor ? 'Creating…' : 'Create vendor'}</button>
                                </form>
                            ) : null}
                            {vendors.length === 0 ? <p className="text-muted">No vendors available.</p> : vendors.map((vendor) => (
                                <div key={vendor.id} className="account-card">
                                    <div>
                                        <strong>{vendor.name}</strong>
                                        <div className="text-muted text-sm">{vendor.email || 'No email'}</div>
                                    </div>
                                    <span className="module-pill">Vendor</span>
                                </div>
                            ))}
                        </div>
                    ) : null}

                    {activeView === 'journal' ? (
                        <div className="card p-6 dashboard-card">
                            <div className="workspace-header">
                                <div>
                                    <div className="eyebrow">Journal entries</div>
                                    <h2 style={{ margin: 0 }}>Entry workspace</h2>
                                </div>
                                <button className="btn btn-primary" onClick={() => setShowEntryForm((value) => !value)} disabled={!canManage}>Add entry</button>
                            </div>
                            {showEntryForm ? (
                                <form onSubmit={submitEntry} className="space-y" style={{ marginBottom: 12 }}>
                                    <input value={entryDescription} onChange={(e) => setEntryDescription(e.target.value)} placeholder="Rent expense entry" required />
                                    <div className="grid grid-2">
                                        <div>
                                            <label className="text-sm text-muted">Date</label>
                                            <input type="date" value={entryDate} onChange={(e) => setEntryDate(e.target.value)} required />
                                        </div>
                                        <div>
                                            <label className="text-sm text-muted">Reference</label>
                                            <input value={entryReference} onChange={(e) => setEntryReference(e.target.value)} placeholder="INV-001" />
                                        </div>
                                    </div>
                                    <div className="grid grid-2">
                                        <div>
                                            <label className="text-sm text-muted">Account</label>
                                            <select value={entryAccountId} onChange={(e) => setEntryAccountId(e.target.value)} required>
                                                <option value="">Select account</option>
                                                {accounts.map((account) => (
                                                    <option key={account.id} value={account.id}>{account.code} - {account.name} ({account.type})</option>
                                                ))}
                                            </select>
                                        </div>
                                        <div>
                                            <label className="text-sm text-muted">Debit</label>
                                            <input value={entryDebit} onChange={(e) => setEntryDebit(e.target.value)} placeholder="0" />
                                        </div>
                                    </div>
                                    <div>
                                        <label className="text-sm text-muted">Credit</label>
                                        <input value={entryCredit} onChange={(e) => setEntryCredit(e.target.value)} placeholder="0" />
                                    </div>
                                    <button className="btn btn-primary" disabled={entrySubmitting}>{entrySubmitting ? 'Saving…' : 'Save entry'}</button>
                                </form>
                            ) : null}
                            {journalEntries.length === 0 ? <p className="text-muted">No journal entries available.</p> : journalEntries.map((entry) => (
                                <div key={entry.id} className="account-card">
                                    <div>
                                        <strong>{entry.description || 'Journal entry'}</strong>
                                        <div className="text-muted text-sm">{entry.entry_date || '—'} • Ref {entry.reference || '—'}</div>
                                    </div>
                                    <span className="module-pill">Entry</span>
                                </div>
                            ))}
                        </div>
                    ) : null}

                    {activeView === 'accounts' ? (
                        <div className="card p-6 dashboard-card">
                            <div className="workspace-header">
                                <div>
                                    <div className="eyebrow">Accounts</div>
                                    <h2 style={{ margin: 0 }}>Chart of accounts</h2>
                                </div>
                            </div>
                            {accounts.length === 0 ? <p className="text-muted">No accounts available.</p> : accounts.map((account) => (
                                <div key={account.id} className="account-card">
                                    <div>
                                        <strong>{account.name}</strong>
                                        <div className="text-muted text-sm">{account.code} • {account.type}</div>
                                    </div>
                                    <span className="module-pill">Account</span>
                                </div>
                            ))}
                        </div>
                    ) : null}
                </section>
            </div>

            <button className="ai-fab" onClick={() => setChatOpen((value) => !value)} title="Open AI assistant">✨</button>

            {chatOpen ? (
                <div className="ai-chat-panel card">
                    <div className="ai-chat-header">
                        <div>
                            <div className="eyebrow">AI Copilot</div>
                            <h3 style={{ margin: 0 }}>Finance assistant</h3>
                        </div>
                        <button className="icon-btn" onClick={() => setChatOpen(false)} title="Close chat">✕</button>
                    </div>
                    <div className="ai-chat-messages">
                        {chatMessages.map((message, index) => (
                            <div key={`${message.role}-${index}`} className={`ai-bubble ${message.role}`}>
                                {message.content}
                            </div>
                        ))}
                    </div>
                    <form onSubmit={sendChatMessage} className="ai-chat-form">
                        <input value={chatInput} onChange={(e) => setChatInput(e.target.value)} placeholder="Ask about records, reports, or next actions" />
                        <button className="btn btn-primary" disabled={chatBusy}>{chatBusy ? 'Thinking…' : 'Send'}</button>
                    </form>
                </div>
            ) : null}
        </main>
    );
}
