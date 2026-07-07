'use client';

export function ErpEmptyState({ title, description }: { title: string; description: string }) {
    return (
        <div className="empty-state card p-6">
            <div className="eyebrow">No data yet</div>
            <h3 style={{ margin: '4px 0 8px' }}>{title}</h3>
            <p className="text-muted" style={{ margin: 0 }}>{description}</p>
        </div>
    );
}
