const API_BASE_URL = '/api';

export const api = {
  async getInfo(url) {
    const response = await fetch(`${API_BASE_URL}/info`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to fetch media info');
    }
    
    return response.json();
  },

  async startDownload(url, format, quality) {
    const response = await fetch(`${API_BASE_URL}/download`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url, format, quality }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to start download');
    }
    
    return response.json();
  },

  async checkStatus(jobId) {
    const response = await fetch(`${API_BASE_URL}/download/${jobId}/status`);
    if (!response.ok) {
       throw new Error('Failed to fetch status');
    }
    return response.json();
  },
  
  getDownloadUrl(jobId) {
    return `${API_BASE_URL}/download/${jobId}/file`;
  }
};
