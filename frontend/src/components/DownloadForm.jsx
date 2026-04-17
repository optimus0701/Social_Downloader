import React, { useState } from 'react';
import { Link2, Search, Video, Music, Image as ImageIcon } from 'lucide-react';
import { api } from '../services/api';
import { useToast } from './Toast';

export default function DownloadForm({ onInfoFetched, isFetching }) {
  const [url, setUrl] = useState('');
  const { showToast } = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url) return;

    try {
      // isFetching is handled by parent App.jsx to show global loading state if needed
      onInfoFetched(null); // Clear previous
      const info = await api.getInfo(url);
      onInfoFetched({ ...info, originalUrl: url });
    } catch (error) {
      showToast(error.message, 'error');
    }
  };

  const getPlatformIcon = (url) => {
    if (!url) return <Link2 className="icon-input" size={20} />;
    
    const lowerUrl = url.toLowerCase();
    if (lowerUrl.includes('youtube.com') || lowerUrl.includes('youtu.be')) return <span className="icon-input" style={{color: 'var(--youtube)', fontWeight: 'bold'}}>YT</span>;
    if (lowerUrl.includes('tiktok.com')) return <span className="icon-input" style={{color: 'var(--tiktok-pink)', fontWeight: 'bold'}}>TK</span>;
    if (lowerUrl.includes('instagram.com')) return <span className="icon-input" style={{color: 'var(--instagram-3)', fontWeight: 'bold'}}>IG</span>;
    if (lowerUrl.includes('facebook.com') || lowerUrl.includes('fb.watch')) return <span className="icon-input" style={{color: 'var(--facebook)', fontWeight: 'bold'}}>FB</span>;
    if (lowerUrl.includes('bilibili.com')) return <span className="icon-input" style={{color: 'var(--bilibili)', fontWeight: 'bold'}}>BL</span>;
    
    return <Link2 className="icon-input" size={20} />;
  };

  return (
    <form onSubmit={handleSubmit} className="glass-panel animate-slide-up">
      <div className="input-group" style={{ marginBottom: '1rem' }}>
        <label className="input-label" htmlFor="url-input">Media URL</label>
        <div className="input-wrapper">
          {getPlatformIcon(url)}
          <input
            id="url-input"
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="text-input"
            placeholder="Paste Youtube, TikTok, Instagram, Facebook link here..."
            required
            disabled={isFetching}
          />
        </div>
      </div>
      
      <button 
        type="submit" 
        className="btn btn-primary" 
        style={{ width: '100%' }}
        disabled={!url || isFetching}
      >
        {isFetching ? (
          <>
            <div className="loading-shimmer" style={{position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, opacity: 0.5, borderRadius: 'inherit'}}></div>
            <Search size={20} className="animate-pulse" /> Analyzing...
          </>
        ) : (
          <>
            <Search size={20} /> Preview & Download
          </>
        )}
      </button>
    </form>
  );
}
