import React from 'react';
import { Outlet, Link } from 'react-router-dom';
import { Home } from 'lucide-react';

export const Layout: React.FC = () => {
  return (
    <div className="container">
      <header style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        marginBottom: '2rem' 
      }}>
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit', fontWeight: 'bold', fontSize: '1.25rem' }}>
          Q-Rate <span style={{ color: 'var(--color-accent)' }}>Staff</span>
        </Link>
        <Link to="/" className="btn-outline" style={{ width: 'auto', padding: '0.5rem' }}>
          <Home size={20} />
        </Link>
      </header>
      
      <main>
        <Outlet />
      </main>
    </div>
  );
};
