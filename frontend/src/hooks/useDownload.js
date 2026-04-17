import { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';

export function useDownload() {
  const [jobs, setJobs] = useState([]);
  const [activeJobId, setActiveJobId] = useState(null);
  const pollingIntervalRef = useRef(null);

  // Poll for active job status
  useEffect(() => {
    const activeJobs = jobs.filter(j => j.status === 'pending' || j.status === 'downloading');
    
    if (activeJobs.length > 0) {
      // Start polling
      pollingIntervalRef.current = setInterval(async () => {
        for (const job of activeJobs) {
          try {
            const updatedJob = await api.checkStatus(job.job_id);
            setJobs(prevJobs => prevJobs.map(j => 
              j.job_id === updatedJob.job_id ? updatedJob : j
            ));
          } catch (e) {
            console.error(e);
          }
        }
      }, 1000); // Polling every second
    } else {
      // Stop polling when no active jobs
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
    }

    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
    };
  }, [jobs]);

  const startDownload = async (url, format, quality) => {
    try {
      const newJob = await api.startDownload(url, format, quality);
      setJobs(prev => [newJob, ...prev]);
      return newJob;
    } catch (error) {
      throw error;
    }
  };

  const removeJob = (jobId) => {
    setJobs(prev => prev.filter(j => j.job_id !== jobId));
  };
  
  const getDownloadUrl = (jobId) => {
    return api.getDownloadUrl(jobId);
  }

  return { jobs, startDownload, removeJob, getDownloadUrl };
}
