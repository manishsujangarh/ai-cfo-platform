'use client';

import { ErpEmptyState } from '../components/erp-empty-state';
import { ErpModuleCard, ErpModuleGrid } from '../components/erp-module-grid';
import { ErpPageShell } from '../components/erp-page-shell';

export default function VendorsPage() {
    return (
        <main>
            <ErpPageShell
                title="Vendors"
                subtitle="A consistent supplier module that can be reused for purchase operations."
                actions={<button className="btn btn-primary">Add vendor</button>}
            >
                <ErpModuleGrid>
                    <ErpModuleCard title="Add vendor" description="Store business name, address, and payment preferences." icon="🏭" badge="Core" />
                    <ErpModuleCard title="View vendors" description="Show supplier profile cards and important details." icon="📦" badge="List" />
                    <ErpModuleCard title="Manage bills" description="Connect vendors with expenses and bills later." icon="🧾" badge="Future" />
                </ErpModuleGrid>
                <ErpEmptyState title="Vendor records" description="This section is ready for FastAPI data once the vendor endpoints are connected." />
            </ErpPageShell>
        </main>
    );
}
