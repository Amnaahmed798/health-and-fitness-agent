# 🚀 Streamlit Deployment Guide

## 📋 Prerequisites

1. **Python 3.11+** installed
2. **Git** for version control
3. **Streamlit Cloud** account (free) or **Heroku/Railway** for deployment

## 🔧 Local Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file in your project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Run Locally
```bash
streamlit run streamlit_app.py
```

## 🌐 Deploy to Streamlit Cloud

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/health-coach-app.git
git push -u origin main
```

### 2. Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set the path to your app: `streamlit_app.py`
6. Add your secrets in the Streamlit Cloud dashboard:
   ```
   GEMINI_API_KEY = your_gemini_api_key_here
   ```

## 🔧 Alternative Deployments

### Heroku
1. Create `Procfile`:
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set GEMINI_API_KEY=your_key_here
   git push heroku main
   ```

### Railway
1. Connect your GitHub repo to Railway
2. Set environment variable: `GEMINI_API_KEY`
3. Deploy automatically

## 📁 Project Structure
```
health-coach-app/
├── streamlit_app.py          # Main Streamlit app
├── main.py                   # Original CLI version
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Project configuration
├── .env                     # Environment variables (local)
├── tools/                   # Tool modules
├── health_agents/           # Specialized agents
├── guardrails.py           # Input validation
└── README.md               # Project documentation
```

## 🔐 Environment Variables

### Required:
- `GEMINI_API_KEY`: Your Gemini API key from Google AI Studio

### Optional:
- `STREAMLIT_SERVER_PORT`: Custom port (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Custom address (default: localhost)

## 🚀 Features Available

✅ **Interactive Chat Interface**
✅ **User Profile Management**
✅ **Goal Analysis & Tracking**
✅ **Meal Planning**
✅ **Workout Recommendations**
✅ **Progress Tracking**
✅ **Specialized Agents** (Escalation, Injury Support, Nutrition)
✅ **Input Validation & Guardrails**
✅ **Responsive Design**

## 🛠️ Customization

### Adding New Tools
1. Create tool in `tools/` directory
2. Import in `streamlit_app.py`
3. Add to `initialize_tools()` function
4. Add processing logic in `process_user_input()`

### Styling
Modify the Streamlit theme in `streamlit_app.py`:
```python
st.set_page_config(
    page_title="Your App",
    page_icon="🏃‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

## 📊 Monitoring

### Streamlit Cloud
- View app logs in the Streamlit Cloud dashboard
- Monitor usage and performance
- Set up alerts for errors

### Local Development
```bash
streamlit run streamlit_app.py --logger.level debug
```

## 🔧 Troubleshooting

### Common Issues:

1. **API Key Not Found**
   - Ensure `.env` file exists locally
   - Set environment variable in deployment platform

2. **Import Errors**
   - Check all dependencies in `requirements.txt`
   - Ensure Python version is 3.11+

3. **Module Not Found**
   - Verify all files are in correct directories
   - Check import statements

4. **Streamlit Connection Issues**
   - Check firewall settings
   - Verify port availability

## 🎯 Next Steps

1. **Add Authentication**: Implement user login/signup
2. **Database Integration**: Store user data persistently
3. **Analytics**: Track usage and user engagement
4. **Mobile Optimization**: Improve mobile experience
5. **Multi-language Support**: Add internationalization

## 📞 Support

For deployment issues:
1. Check Streamlit documentation
2. Review error logs
3. Test locally first
4. Verify environment variables

---

**Happy Deploying! 🚀** 