import React, { useState } from 'react';
import { Video, Music, Image as ImageIcon, Download } from 'lucide-react';
import { useToast } from './Toast';

export default function MediaPreview({ info, onDownloadStart }) {
  const { showToast } = useToast();
  
  // Default format type selection based on available media
  const [formatType, setFormatType] = useState('best'); // 'best' (Video), 'audio', 'images'

  if (!info) return null;

  const handleDownload = () => {
    console.log("[MediaPreview] Starting download for:", info.originalUrl, "Format:", formatType);
    onDownloadStart(info.originalUrl, formatType, 'highest')
      .then(() => {
        console.log("[MediaPreview] Download initialized successfully");
        showToast(`Download started!`, 'success');
      })
      .catch(err => {
        console.error("[MediaPreview] Error starting download:", err);
        showToast(err.message, 'error');
      });
  };

  const hasImages = info.is_slideshow;
  const isAudioAvailable = true; // yt-dlp usually can extract audio from video

  return (
    <div className="glass-panel animate-slide-up" style={{ marginTop: '1.5rem', animationDelay: '0.1s' }}>
      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        
        {/* Thumbnail */}
        {info.thumbnail && (
          <div style={{ flex: '1 1 200px', maxWidth: '300px' }}>
            <img 
              src={info.thumbnail} 
              alt={info.title} 
              style={{ width: '100%', borderRadius: 'inherit', objectFit: 'cover', aspectRatio: '16/9', backgroundColor: 'var(--bg-input)' }} 
            />
          </div>
        )}

        {/* Info & Options */}
        <div style={{ flex: '2 1 300px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.25rem', wordBreak: 'break-word' }}>
              {info.title}
            </h3>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              <span className="badge" style={{ background: 'var(--bg-input)' }}>{info.platform}</span>
              {info.duration && <span className="badge" style={{ background: 'var(--bg-input)' }}>{Math.floor(info.duration / 60)}:{(info.duration % 60).toString().padStart(2, '0')}</span>}
              {hasImages && <span className="badge badge-images">Slideshow</span>}
            </div>
          </div>

          {/* Format Selection Blocks (Bento Style) */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))', gap: '0.5rem' }}>
            
            {!hasImages && (
              <div 
                onClick={() => setFormatType('best')}
                style={{
                  padding: '1rem',
                  borderRadius: 'var(--radius-md)',
                  border: `2px solid ${formatType === 'best' ? 'var(--primary)' : 'var(--border)'}`,
                  background: formatType === 'best' ? 'var(--bg-input)' : 'transparent',
                  cursor: 'pointer',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  gap: '0.5rem',
                  transition: 'all 0.2s'
                }}
              >
                <Video size={24} color="var(--primary)" />
                <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>Video</span>
              </div>
            )}

            {isAudioAvailable && (
              <div 
                onClick={() => setFormatType('audio')}
                style={{
                  padding: '1rem',
                  borderRadius: 'var(--radius-md)',
                  border: `2px solid ${formatType === 'audio' ? 'var(--success)' : 'var(--border)'}`,
                  background: formatType === 'audio' ? 'var(--bg-input)' : 'transparent',
                  cursor: 'pointer',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  gap: '0.5rem',
                  transition: 'all 0.2s'
                }}
              >
                <Music size={24} color="var(--success)" />
                <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>Audio</span>
              </div>
            )}

            {hasImages && (
              <div 
                onClick={() => setFormatType('images')}
                style={{
                  padding: '1rem',
                  borderRadius: 'var(--radius-md)',
                  border: `2px solid ${formatType === 'images' ? 'var(--warning)' : 'var(--border)'}`,
                  background: formatType === 'images' ? 'var(--bg-input)' : 'transparent',
                  cursor: 'pointer',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  gap: '0.5rem',
                  transition: 'all 0.2s'
                }}
              >
                <ImageIcon size={24} color="var(--warning)" />
                <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>Images</span>
              </div>
            )}
          </div>

          <button className="btn btn-primary" onClick={handleDownload} style={{ marginTop: 'auto' }}>
            <Download size={18} /> Add to Queue
          </button>
        </div>
      </div>
    </div>
  );
}
