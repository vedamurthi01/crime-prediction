# 🔍 Crime Prediction & Criminal Identification System

A comprehensive full-stack machine learning application for crime prediction and suspect identification using advanced ML algorithms, Flask backend, React.js frontend, and MongoDB database.

## 🎯 Features

### Crime Type Prediction
- **6 ML Algorithms**: Logistic Regression, Decision Tree, Random Forest, XGBoost, SVM, Naive Bayes
- **Automatic Model Selection**: Trains all models and selects the best performer
- **Multi-factor Analysis**: Location, time, weapon, victim/suspect age, district
- **Real-time Predictions**: REST API with confidence scores

### Criminal Identification
- **KNN Algorithm**: K-Nearest Neighbors for suspect matching
- **Pattern Recognition**: Modus operandi, location, time-based matching
- **Top 5 Suspects**: Ranked by similarity score
- **Suspect Database**: Automatically generated from crime patterns

### Crime Analytics
- **Interactive Visualizations**: Heatmaps, bar charts, pie charts, trend analysis
- **Statistical Insights**: Crime by hour, month, location, type
- **Real-time Analytics**: Dynamic data processing
- **Export-ready**: Base64 image generation

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0
- **Database**: MongoDB
- **ML Libraries**: scikit-learn, XGBoost, pandas, numpy
- **Visualization**: Matplotlib, Seaborn
- **API**: RESTful endpoints with CORS support

### Frontend
- **Framework**: React.js 18
- **Build Tool**: Vite 5
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Styling**: Custom CSS with responsive design

### Machine Learning
- **Crime Type Models**: LR, DT, RF, XGBoost, SVM, NB
- **Criminal Identification**: KNN with distance weighting
- **Preprocessing**: Label encoding, standard scaling
- **Evaluation**: Accuracy, precision, recall, F1-score

## 📁 Project Structure

```
pradeep_project/
├── backend/
│   ├── app.py                      # Flask application
│   ├── config.py                   # Configuration
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # Environment variables
│   ├── database/
│   │   ├── __init__.py
│   │   └── mongodb.py              # MongoDB connection
│   ├── models/
│   │   ├── train_crime_type.py     # Crime type trainer
│   │   └── train_criminal_knn.py   # KNN trainer
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── train_routes.py         # Training endpoints
│   │   ├── predict_routes.py       # Prediction endpoints
│   │   └── visualization_routes.py # Visualization endpoints
│   ├── utils/
│   │   ├── __init__.py
│   │   └── dataset_merger.py       # Data preprocessing
│   └── visualizations/
│       ├── __init__.py
│       └── crime_visualizer.py     # Visualization generator
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── App.css
│       ├── services/
│       │   └── api.js              # API client
│       └── pages/
│           ├── HomePage.jsx
│           ├── TrainingPage.jsx
│           ├── CrimeTypePrediction.jsx
│           ├── CriminalPrediction.jsx
│           └── AnalyticsDashboard.jsx
└── datasets/
    ├── crime_dataset_india.csv
    ├── Crime_Data_from_2020_to_Present.csv
    └── communities.names
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB (local or cloud)
- Git

### Backend Setup

1. **Navigate to backend directory**
```powershell
cd backend
```

2. **Create virtual environment**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Configure environment variables**
Edit `backend/.env` file:
```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=crime_prediction_db
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

5. **Start MongoDB**
```powershell
# If using local MongoDB
mongod
```

6. **Run Flask server**
```powershell
python app.py
```
Server will run at: `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
```powershell
cd frontend
```

2. **Install dependencies**
```powershell
npm install
```

3. **Start development server**
```powershell
npm run dev
```
Frontend will run at: `http://localhost:5173`

## 📊 Usage Guide

### 1. Train Models (First Time Setup)

**Via Frontend:**
1. Navigate to `http://localhost:5173/train`
2. Click "Train Crime Type Models" (takes 2-5 minutes)
3. Click "Train KNN Model" (takes 1-2 minutes)
4. Wait for training completion

**Via Backend (Alternative):**
```powershell
cd backend
python models/train_crime_type.py
python models/train_criminal_knn.py
```

### 2. Predict Crime Type

**Via Frontend:**
1. Go to "Crime Prediction" page
2. Fill in the form:
   - Location (e.g., "Downtown")
   - Time (0-23 hours)
   - Weapon Used
   - Victim Age
   - Suspect Age
   - Month (1-12)
   - Weekday (0-6)
   - District
3. Click "Predict Crime Type"
4. View results with confidence scores

**Via API:**
```powershell
curl -X POST http://localhost:5000/api/predict/crime-type `
  -H "Content-Type: application/json" `
  -d '{
    "location": "Downtown",
    "time": 14,
    "weapon_used": "Firearm",
    "victim_age": 35,
    "suspect_age": 28,
    "month": 6,
    "weekday": 2,
    "district": "Central"
  }'
```

### 3. Identify Suspects

**Via Frontend:**
1. Go to "Criminal Prediction" page
2. Enter crime details:
   - Crime Type (e.g., "BURGLARY")
   - Location
   - Time
   - Modus Operandi
   - District
3. Click "Identify Suspects"
4. View top 5 matched suspects

**Via API:**
```powershell
curl -X POST http://localhost:5000/api/predict/criminal `
  -H "Content-Type: application/json" `
  -d '{
    "crime_type": "BURGLARY",
    "location": "Downtown",
    "time": 22,
    "modus_operandi": "Firearm",
    "district": "Central"
  }'
```

### 4. View Analytics Dashboard

1. Navigate to "Analytics" page
2. View:
   - Crime heatmap (Location vs Hour)
   - Hourly crime distribution
   - Crime type distribution
   - Monthly trends
   - Top locations and crime types
3. Click "Refresh Analytics" to update data

## 🔌 API Endpoints

### Training Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/train/crime-type` | Train crime type models |
| POST | `/api/train/criminal-knn` | Train KNN model |
| GET | `/api/train/status` | Check training status |

### Prediction Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predict/crime-type` | Predict crime type |
| POST | `/api/predict/criminal` | Identify suspects |
| GET | `/api/predict/models/status` | Check model status |

### Visualization Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/visualization/heatmap` | Get crime heatmap |
| GET | `/api/visualization/statistics` | Get crime statistics |
| GET | `/api/visualization/charts/hour` | Hourly chart |
| GET | `/api/visualization/charts/type` | Crime type chart |
| GET | `/api/visualization/charts/monthly` | Monthly trend |
| GET | `/api/visualization/all` | All visualizations |

## 🧪 Testing

### Test Backend Endpoints
```powershell
# Health check
curl http://localhost:5000/health

# Root endpoint (API docs)
curl http://localhost:5000/

# Training status
curl http://localhost:5000/api/train/status

# Statistics
curl http://localhost:5000/api/visualization/statistics
```

### Test Frontend
1. Open browser: `http://localhost:5173`
2. Navigate through all pages
3. Test form submissions
4. Verify visualizations load

## 📈 Model Performance

### Crime Type Prediction Models
- **Logistic Regression**: Linear classification
- **Decision Tree**: Rule-based decisions
- **Random Forest**: Ensemble of trees
- **XGBoost**: Gradient boosting
- **SVM**: Support vector classification
- **Naive Bayes**: Probabilistic classification

Best model is automatically selected based on accuracy.

### KNN Criminal Identification
- **Algorithm**: K-Nearest Neighbors
- **Distance Metric**: Euclidean (scaled)
- **K Value**: 5 neighbors
- **Weighting**: Distance-based

## 🗄️ Database Schema

### Crime Records Collection
```javascript
{
  crime_id: String,
  crime_type: String,
  location: String,
  latitude: Number,
  longitude: Number,
  date: String,
  time: String,
  victim_age: Number,
  suspect_age: Number,
  weapon_used: String,
  district: String,
  hour: Number,
  month: Number,
  weekday: Number,
  crime_category: String
}
```

## 🎨 Frontend Features

- **Responsive Design**: Works on desktop, tablet, mobile
- **Modern UI**: Gradient backgrounds, cards, animations
- **Real-time Updates**: Loading states, error handling
- **Data Visualization**: Charts rendered as images
- **Form Validation**: Client-side validation
- **Navigation**: React Router with active states

## 🔒 Security Notes

- Change `SECRET_KEY` in production
- Use environment variables for sensitive data
- Enable MongoDB authentication
- Use HTTPS in production
- Implement rate limiting for API

## 🐛 Troubleshooting

### Backend Issues

**MongoDB Connection Failed**
- Ensure MongoDB is running: `mongod`
- Check connection string in `.env`
- Verify MongoDB port (default: 27017)

**Module Not Found**
```powershell
pip install -r requirements.txt
```

**Model Not Found**
- Train models first via `/api/train/crime-type`
- Check `backend/models/` directory for .pkl files

### Frontend Issues

**npm install fails**
```powershell
rm -rf node_modules package-lock.json
npm install
```

**Blank page**
- Check browser console for errors
- Verify backend is running
- Check CORS configuration

**API calls fail**
- Ensure backend is running on port 5000
- Check proxy settings in `vite.config.js`
- Verify API base URL in `services/api.js`

## 📝 Development

### Adding New Features

1. **Backend**: Add route in `routes/` directory
2. **Frontend**: Create component in `src/components/`
3. **API**: Update `services/api.js`
4. **Testing**: Test endpoint and UI integration

### Code Style
- Backend: PEP 8 Python style guide
- Frontend: ESLint with React rules
- Comments: Explain complex logic

## 📦 Deployment

### Backend Deployment
1. Use production WSGI server (gunicorn)
2. Set `FLASK_ENV=production`
3. Configure MongoDB connection
4. Set up reverse proxy (nginx)

### Frontend Deployment
```powershell
npm run build
```
Serve `dist/` folder with static file server

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 📄 License

This project is for educational purposes.

## 👥 Authors

Crime Prediction & Criminal Identification System

## 🙏 Acknowledgments

- Datasets: UCI ML Repository, Public Crime Data
- Libraries: scikit-learn, Flask, React
- Community: Stack Overflow, GitHub

## 📞 Support

For issues and questions:
- Check troubleshooting section
- Review API documentation
- Check backend logs
- Inspect browser console

---

**Built with ❤️ using Flask, React, and Machine Learning**
#   c r i m e - p r e d i c t i o n  
 