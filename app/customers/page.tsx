'use client';

import { ErpEmptyState } from '../components/erp-empty-state';
import { ErpModuleCard, ErpModuleGrid } from '../components/erp-module-grid';
import { ErpPageShell } from '../components/erp-page-shell';

export default function CustomersPage() {
    return (
        <main>
            <ErpPageShell
                title="Customers"
                subtitle="Manage customer records with a simple, reusable layout for future API integration."
                actions={<button className="btn btn-primary">Add customer</button>}
            >
                <ErpModuleGrid>
                    <ErpModuleCard title="Add customer" description="Capture customer name, contact details, and address." icon="👤" badge="Core" />
                    <ErpModuleCard title="View customers" description="List all customers in a simple card-based view." icon="📋" badge="List" />
                    <ErpModuleCard title="Manage activity" description="Track invoices, payments, and follow-ups later." icon="📈" badge="Future" />
                </ErpModuleGrid>
                <ErpEmptyState title="Customer records" description="This section is ready for FastAPI data once the backend endpoints are connected." />
            </ErpPageShell>
        </main>
    );
}
