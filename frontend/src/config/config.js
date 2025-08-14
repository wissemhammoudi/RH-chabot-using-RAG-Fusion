const config = {
  API_BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8000',
  ENDPOINTS: {
    GENERATE: '/generate/',
    SUBQUESTIONS: '/generate_subquestions/',
    RETRIEVE_RESUMES: '/retrieve_resumes/',
  },
  APP: {
    NAME: process.env.REACT_APP_APP_NAME || 'RH Chatbot',
    VERSION: process.env.REACT_APP_VERSION || '1.0.0',
  },
  CHAT: {
    MAX_MESSAGE_LENGTH: 1000,
    TYPING_INDICATOR_DELAY: 1000,
  }
};

export default config;
