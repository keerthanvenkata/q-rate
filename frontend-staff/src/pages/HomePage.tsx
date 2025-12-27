import React from 'react';
import { Link } from 'react-router-dom';
import { PlusCircle, QrCode } from 'lucide-react';

export const HomePage: React.FC = () => {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '2rem' }}>
            <div className="text-center mb-4">
                <h2>Hello, Staff!</h2>
                <p className="text-muted">Ready for the lunch rush?</p>
            </div>

            <Link to="/visit" className="btn btn-primary" style={{ padding: '2rem', fontSize: '1.25rem' }}>
                <PlusCircle size={32} />
                New Visit
            </Link>

            <Link to="/redeem" className="btn btn-outline" style={{ padding: '1.5rem' }}>
                <QrCode size={24} />
                Redeem Coupon
            </Link>
            
            <div className="card mt-4">
                <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>Recent Activity</h3>
                <p className="text-muted" style={{ fontSize: '0.875rem' }}>No recent visits configured in prototype.</p>
            </div>
        </div>
    );
};
