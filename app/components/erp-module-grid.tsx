'use client';

import { ReactNode } from 'react';

type ErpModuleCardProps = {
    title: string;
    description: string;
    icon: string;
    badge?: string;
    children?: ReactNode;
};

export function ErpModuleCard({ title, description, icon, badge, children }: ErpModuleCardProps) {
    return (
        <div className="module-card card p-6">
            <div className="card-icon">{icon}</div>
            <div className="module-title-row">
                <h3 style={{ margin: 0 }}>{title}</h3>
                {badge ? <span className="module-pill">{badge}</span> : null}
            </div>
            <p className="text-muted" style={{ margin: 0 }}>{description}</p>
            {children ? <div style={{ marginTop: 8 }}>{children}</div> : null}
        </div>
    );
}

export function ErpModuleGrid({ children }: { children: ReactNode }) {
    return <div className="module-grid">{children}</div>;
}
