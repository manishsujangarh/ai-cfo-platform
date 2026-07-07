'use client';

import { ReactNode } from 'react';

type ErpPageShellProps = {
    title: string;
    subtitle?: string;
    actions?: ReactNode;
    children: ReactNode;
};

export function ErpPageShell({ title, subtitle, actions, children }: ErpPageShellProps) {
    return (
        <section className="page-shell" style={{ maxWidth: 1120, margin: '0 auto' }}>
            <div className="card p-6">
                <div className="page-shell-header">
                    <div>
                        <div className="eyebrow">ERP module</div>
                        <h1 style={{ margin: '4px 0 8px' }}>{title}</h1>
                        {subtitle ? <p className="text-muted" style={{ margin: 0 }}>{subtitle}</p> : null}
                    </div>
                    {actions ? <div className="page-shell-actions">{actions}</div> : null}
                </div>
            </div>
            <div>{children}</div>
        </section>
    );
}
