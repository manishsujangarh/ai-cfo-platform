import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'AI CFO SaaS',
    description: 'Simple finance operations workspace for modern teams',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}
