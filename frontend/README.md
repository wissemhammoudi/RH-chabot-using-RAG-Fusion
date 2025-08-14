# Frontend - RH Chatbot using RAG Fusion

> **📖 Main Project Documentation**: See the [main README](../README.md) for complete project overview and Docker setup instructions.

AI-powered HR assistant frontend for resume analysis and job matching.

## Project Structure

```
frontend/
├── src/
│   ├── component/          # Reusable UI components
│   │   ├── Avatar.js      # User/bot avatar display
│   │   ├── Loading.js     # Loading spinner component
│   │   └── Error.js       # Error display component
│   ├── config/
│   │   └── config.js      # Centralized configuration
│   ├── hooks/
│   │   └── useChatbot.js  # Business logic and state management
│   ├── services/
│   │   └── apiService.js  # API communication service
│   ├── page/
│   │   └── Chatbot.js     # UI component (dumb component)
│   └── App.js             # Application entry point
```

## Key Improvements Made

### 1. **Separation of Concerns**
- **`useChatbot` hook**: Contains all business logic, state management, and API calls
- **`Chatbot` component**: Pure UI component that only renders and handles user interactions
- **`apiService`**: Handles all HTTP communication

### 2. **Centralized Configuration**
- All API endpoints moved to `config/config.js`
- Environment variables support (REACT_APP_*)
- Easy to change API URLs without touching components

### 3. **Custom Hook Pattern**
- Business logic extracted into `useChatbot` hook
- Component becomes a "dumb" component that only renders
- Easier to test business logic separately from UI
- Reusable logic across different components if needed

### 4. **Clean Architecture**
- **Hooks**: Business logic and state
- **Components**: UI rendering only
- **Services**: API communication
- **Config**: Settings and constants

## Configuration

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_BASE_URL=http://127.0.0.1:8000
REACT_APP_APP_NAME=RH Chatbot
REACT_APP_VERSION=1.0.0
```

## Usage

### **Option 1: Docker (Recommended)**
```bash
# From project root
docker-compose up frontend -d
```

### **Option 2: Local Development**
```bash
cd frontend
npm install
npm start
```

## Related Documentation

- **[Main Project README](../README.md)** - Complete project overview and Docker setup
- **[Backend Documentation](../backend/README.md)** - Backend services and API
- **[API Reference](../backend/API_DOCUMENTATION.md)** - Complete API documentation
