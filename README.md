# Health & Wellness Coach - Full Stack Application

A comprehensive health and wellness coaching application with a Next.js frontend and Python FastAPI backend, featuring AI-powered health coaching with specialized agents and tools.

## 🏗️ Architecture

- **Frontend**: Next.js with TypeScript, Tailwind CSS, and Lucide React icons
- **Backend**: Python FastAPI with specialized health coaching agents
- **AI**: Gemini 2.0 Flash model for natural language processing
- **Tools**: Goal analysis, meal planning, progress tracking, workout recommendations

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Gemini API key

### 1. Setup Environment

Create a `.env` file in the `hello_agent` directory:

```bash
cd hello_agent
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

### 2. Install Backend Dependencies

```bash
cd hello_agent
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 4. Run the Application

#### Option A: Run Both Services (Recommended)

Open two terminal windows:

**Terminal 1 - Backend:**
```bash
cd hello_agent
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

#### Option B: Use the Development Script

Create a development script to run both services:

```bash
# Create a dev script (Windows)
echo "start /B python hello_agent/main.py & start /B npm run dev --prefix frontend" > dev.bat

# Or for Unix/Linux/Mac
echo "python hello_agent/main.py & npm run dev --prefix frontend" > dev.sh
chmod +x dev.sh
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🏃‍♀️ Features

### Frontend Features
- **User Onboarding**: Collect user information (age, fitness level, goals, equipment)
- **Real-time Chat**: Interactive chat interface with the health coach
- **Profile Management**: View and update user profile information
- **Quick Actions**: Direct access to common features
- **Responsive Design**: Works on desktop and mobile devices

### Backend Features
- **AI Health Coach**: Powered by Gemini 2.0 Flash
- **Specialized Agents**:
  - Escalation Agent: Human support requests
  - Injury Support Agent: Injury assessment and guidance
  - Nutrition Expert Agent: Detailed nutrition consultations
- **Smart Tools**:
  - Goal Analyzer: SMART goal setting and tracking
  - Meal Planner: Personalized meal plans (requires calorie target and dietary restrictions)
  - Progress Tracker: Measurement and workout logging
  - Workout Recommender: Customized exercise routines
  - Workout Logger: Track completed workout sessions
- **Guardrails**: Input validation and safety checks

## 🔧 API Endpoints

### Core Endpoints
- `POST /ask` - Send a message to the health coach
- `GET /profile` - Get user profile
- `POST /profile` - Update user profile
- `POST /meal-plan` - Generate meal plan
- `POST /workout` - Generate workout routine
- `POST /progress` - Track progress measurements
- `POST /goal` - Set new goal
- `POST /log-workout` - Log completed workout sessions

### Example API Usage

```javascript
// Send a message to the health coach
const response = await fetch('http://localhost:8000/ask', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: "I want to lose 10 pounds in 3 months",
    userInfo: {
      age: 30,
      fitnessLevel: "beginner",
      healthGoals: "weight loss",
      equipment: ["gym"]
    }
  })
});

const result = await response.json();
console.log(result.response);

// Log a workout session
const workoutResponse = await fetch('http://localhost:8000/log-workout', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    date: "2024-07-09",
    workout_type: "Balanced Beginner Routine",
    notes: "Completed all sets, feeling stronger!"
  })
});
```

## 🛠️ Development

### Frontend Development

```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
```

### Backend Development

```bash
cd hello_agent
python main.py  # Start FastAPI server
```

### File Structure

```
├── frontend/                 # Next.js frontend
│   ├── src/
│   │   ├── app/             # App router pages
│   │   └── services/        # API services
│   └── package.json
├── hello_agent/             # Python backend
│   ├── main.py              # FastAPI server
│   ├── tools/               # Health coaching tools
│   ├── health_agents/       # Specialized agents
│   └── requirements.txt
└── README.md
```

## 🔒 Environment Variables

Required environment variables in `hello_agent/.env`:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

## 🧪 Testing

### Test the Backend API

```bash
# Test the health coach
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "How can I improve my fitness?"}'

# Test meal plan generation (requires calorie target and restrictions)
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a 2500 calorie vegetarian meal plan"}'

# Test workout logging
curl -X POST "http://localhost:8000/log-workout" \
  -H "Content-Type: application/json" \
  -d '{"date":"2024-07-09","workout_type":"Strength Training","notes":"Great session!"}'
```

### Test the Frontend

1. Open http://localhost:3000
2. Complete the onboarding process
3. Try sending messages to the health coach
4. Test the quick action buttons

## 🚀 Deployment

### Frontend Deployment

```bash
cd frontend
npm run build
npm run start
```

### Backend Deployment

```bash
cd hello_agent
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check that both frontend and backend are running
2. Verify your Gemini API key is set correctly
3. Check the browser console and backend logs for errors
4. Ensure all dependencies are installed correctly

## 🔄 Updates

To update dependencies:

```bash
# Frontend
cd frontend
npm update

# Backend
cd hello_agent
pip install --upgrade -r requirements.txt
``` 