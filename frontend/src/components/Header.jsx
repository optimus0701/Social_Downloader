import React from 'react';
import { Moon, Sun, Download } from 'lucide-react';
import { useTheme } from '../hooks/useTheme';

export default function Header() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header style={{ 
      display: 'flex', 
      justifyContent: 'space-between', 
      alignItems: 'center',
      marginBottom: '1rem'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div style={{ 
          background: 'linear-gradient(135deg, var(--primary) 0%, var(--tiktok-cyan) 100%)',
          width: '40px',
          height: '40px',
          borderRadius: 'var(--radius-lg)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          boxShadow: 'var(--shadow-glow)'
        }}>
          <Download size={24} />
        </div>
        <div>
          <h1 className="heading-1" style={{ fontSize: '1.5rem', margin: 0 }}>Social Downloader</h1>
          <span className="subtitle" style={{ fontSize: '0.875rem' }}>High-speed media extraction</span>
        </div>
      </div>
      
      <button 
        className="btn-icon-only glass-panel" 
        onClick={toggleTheme}
        style={{ padding: '0.5rem', borderRadius: '50%' }}
        aria-label="Toggle theme"
      >
        {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
      </button>
    </header>
  );
}
