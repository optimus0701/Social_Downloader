import React, { useState } from 'react'
import Header from './components/Header'
import DownloadForm from './components/DownloadForm'
import MediaPreview from './components/MediaPreview'
import DownloadQueue from './components/DownloadQueue'
import { ToastProvider } from './components/Toast'
import { useDownload } from './hooks/useDownload'

function AppContent() {
  const [currentInfo, setCurrentInfo] = useState(null);
  const [isFetchingInfo, setIsFetchingInfo] = useState(false);
  const { jobs, startDownload, getDownloadUrl } = useDownload();

  const handleInfoFetched = (info) => {
    setCurrentInfo(info);
    setIsFetchingInfo(false);
  };

  const handleFetchStart = () => {
    setIsFetchingInfo(true);
  };

  return (
    <>
      <div className="app-background">
        <div className="glow-circle glow-1"></div>
        <div className="glow-circle glow-2"></div>
      </div>
      <div className="app-container">
        <Header />
        
        <main>
          {/* We intercept the form submission slightly to manage the global loading state */}
          <div onClick={isFetchingInfo ? null : handleFetchStart}>
            <DownloadForm 
              onInfoFetched={handleInfoFetched} 
              isFetching={isFetchingInfo} 
            />
          </div>

          <MediaPreview 
            info={currentInfo} 
            onDownloadStart={startDownload} 
          />

          <DownloadQueue 
            jobs={jobs} 
            getDownloadUrl={getDownloadUrl} 
          />
        </main>
      </div>
    </>
  )
}

function App() {
  return (
    <ToastProvider>
      <AppContent />
    </ToastProvider>
  )
}

export default App
