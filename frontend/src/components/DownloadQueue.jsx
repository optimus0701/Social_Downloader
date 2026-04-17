import React from 'react';
import { Download as DownloadIcon, CheckCircle, Loader, AlertCircle } from 'lucide-react';

export default function DownloadQueue({ jobs, getDownloadUrl }) {
  if (!jobs || jobs.length === 0) return null;

  return (
    <div className="glass-panel animate-slide-up" style={{ marginTop: '1.5rem', animationDelay: '0.2s' }}>
      <h3 style={{ fontSize: '1.125rem', fontWeight: 600, marginBottom: '1rem' }}>Active Downloads</h3>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {jobs.map(job => (
          <div key={job.job_id} style={{ 
            padding: '1rem', 
            background: 'var(--bg-input)', 
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border)',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.5rem'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.875rem', fontWeight: 500, fontFamily: 'monospace' }}>
                ID: {job.job_id.substring(0, 8)}...
              </span>
              
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                {job.status === 'downloading' && <Loader size={16} className="animate-spin" style={{ animation: 'spin 2s linear infinite' }} />}
                {job.status === 'completed' && <CheckCircle size={16} color="var(--success)" />}
                {job.status === 'error' && <AlertCircle size={16} color="var(--danger)" />}
                
                <span style={{ fontSize: '0.75rem', textTransform: 'uppercase', fontWeight: 600, 
                  color: job.status === 'error' ? 'var(--danger)' : 
                         job.status === 'completed' ? 'var(--success)' : 'var(--text-secondary)'
                }}>
                  {job.status}
                </span>
              </div>
            </div>

            {/* Progress Bar */}
            {(job.status === 'downloading' || job.status === 'pending') && (
              <div className="progress-container">
                <div className="progress-bar" style={{ width: `${Math.max(job.progress, 2)}%` }}></div>
              </div>
            )}

            {/* Error Message */}
            {job.status === 'error' && (
              <div style={{ fontSize: '0.875rem', color: 'var(--danger)', marginTop: '0.5rem' }}>
                {job.error}
              </div>
            )}

            {/* Download Link */}
            {job.status === 'completed' && (
              <a 
                href={getDownloadUrl(job.job_id)} 
                className="btn btn-primary" 
                style={{ alignSelf: 'flex-start', padding: '0.5rem 1rem', fontSize: '0.875rem', marginTop: '0.5rem' }}
                download
              >
                <DownloadIcon size={16} /> Save File
              </a>
            )}
          </div>
        ))}
      </div>
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
