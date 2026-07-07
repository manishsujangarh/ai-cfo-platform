'use client';

import { ErpEmptyState } from '../components/erp-empty-state';
import { ErpModuleCard, ErpModuleGrid } from '../components/erp-module-grid';
import { ErpPageShell } from '../components/erp-page-shell';

export default function InvoicesPage() {
    return (
        <main>
            <ErpPageShell
                title="Invoices"
                subtitle="A reusable sales billing module that can be adapted to any business flow."
                actions={<button className="btn btn-primary">Create invoice</button>}
            >
                <ErpModuleGrid>
                    <ErpModuleCard title="Create invoice" description="Add invoice number, date, customer, and line items." icon="🧾" badge="Core" />
                    <ErpModuleCard title="Track status" description="Show draft, sent, paid, and overdue states." icon="✅" badge="Workflow" />
                    <ErpModuleCard title="Follow-up" description="Connect to payments and reminders later." icon="🔔" badge="Future" />
                </ErpModuleGrid>
                <ErpEmptyState title="Invoice records" description="This section is ready for FastAPI billing data once the backend endpoints are connected." />
            </ErpPageShell>
        </main>
    );
}
