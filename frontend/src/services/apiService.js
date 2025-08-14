import config from '../config/config';

class ApiService {
  constructor() {
    this.baseURL = config.API_BASE_URL;
  }

  async makeRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    };

    try {
      const response = await fetch(url, defaultOptions);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API Error: ${response.status} - ${errorText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Request failed:', error);
      throw error;
    }
  }

  async generateResponse(data) {
    return this.makeRequest(config.ENDPOINTS.GENERATE, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async generateSubquestions(description) {
    return this.makeRequest(config.ENDPOINTS.SUBQUESTIONS, {
      method: 'POST',
      body: JSON.stringify({ description }),
    });
  }

  async retrieveResumes(subquestions) {
    return this.makeRequest(config.ENDPOINTS.RETRIEVE_RESUMES, {
      method: 'POST',
      body: JSON.stringify({ subquestions }),
    });
  }
}

export default new ApiService();
