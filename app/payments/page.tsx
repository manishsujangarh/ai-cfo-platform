'use client';

import { ErpEmptyState } from '../components/erp-empty-state';
import { ErpModuleCard, ErpModuleGrid } from '../components/erp-module-grid';
import { ErpPageShell } from '../components/erp-page-shell';

export default function PaymentsPage() {
    return (
        <main>
            <ErpPageShell
                title="Payments"
                subtitle="A reusable payments module for receipts, payouts, and future reconciliation workflows."
                actions={<button className="btn btn-primary">Record payment</button>}
            >
                <ErpModuleGrid>
                    <ErpModuleCard title="Receive payment" description="Capture incoming payments with date and reference." icon="💳" badge="Core" />
                    <ErpModuleCard title="Make payment" description="Record outgoing payments to vendors and bills." icon="💸" badge="Core" />
                    <ErpModuleCard title="Reconcile" description="Match payments to invoices and bills later." icon="🔄" badge="Future" />
                </ErpModuleGrid>
                <ErpEmptyState title="Payment records" description="This section is ready for FastAPI transaction data once the backend endpoints are connected." />
            </ErpPageShell>
        </main>
    );
}
