# 🚀 Full-Stack Monorepo Deployment Guide for Render

This is a complete monorepo setup for deploying a **FastAPI backend** and **React (Vite) frontend** to Render using Docker containers.

## 📁 Project Structure

```
monorepo-example/
├── render.yaml                 # Render Blueprint (deploys both services)
├── backend/
│   ├── Dockerfile             # Backend Docker image
│   ├── .dockerignore
│   ├── main.py                # FastAPI application with CORS
│   └── requirements.txt       # Python dependencies
└── frontend/
    ├── Dockerfile             # Frontend Docker image (multi-stage)
    ├── .dockerignore
    ├── docker-entrypoint.sh   # Runtime config injection script
    ├── nginx.conf.template    # Nginx configuration
    ├── package.json           # Node.js dependencies
    ├── vite.config.js         # Vite configuration
    ├── index.html             # HTML entry point
    ├── public/
    │   └── config.js.template # Runtime API URL template
    └── src/
        ├── main.jsx           # React entry point
        ├── App.jsx            # Main React component
        ├── App.css            # Component styles
        └── index.css          # Global styles
```

---

## 🎯 Key Features

### ✅ Backend (FastAPI)
- **CORS middleware** configured to allow frontend domain
- Dynamic `FRONTEND_URL` from environment variable
- Health check endpoint at `/health`
- Example prediction API at `/api/predict`
- Docker containerized with Python 3.11

### ✅ Frontend (React + Vite)
- **Runtime API URL injection** (no rebuild needed for different environments)
- Nginx serves static files with proper caching
- Multi-stage Docker build (build + production)
- Responsive UI with gradient design
- Connects to backend API dynamically

### ✅ Render Deployment
- **Single `render.yaml`** for both services
- **`fromService` injection** - backend URL automatically passed to frontend
- **`rootDir`** for monorepo subfolder deployment
- **Free tier** plans configured by default
- Auto-deploy on git push

---

## 🚀 Deployment Steps

### Option 1: Deploy via Render Blueprint (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial monorepo setup"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Go to Render Dashboard:**
   - Navigate to: https://dashboard.render.com/
   - Click **"Blueprints"** → **"New Blueprint Instance"**

3. **Connect your repository:**
   - Select your GitHub repository
   - Render will automatically detect `render.yaml`

4. **Deploy:**
   - Click **"Apply"**
   - Render will deploy both services simultaneously
   - Wait 5-10 minutes for Docker builds

5. **Access your application:**
   - Backend: `https://diabetes-backend-xxxx.onrender.com`
   - Frontend: `https://diabetes-frontend-xxxx.onrender.com`

### Option 2: Manual Deployment

#### Deploy Backend First:
1. Go to Render Dashboard → **"New Web Service"**
2. Connect your repository
3. Configure:
   - **Name:** `diabetes-backend`
   - **Environment:** Docker
   - **Root Directory:** `backend`
   - **Dockerfile Path:** `./Dockerfile`
   - **Plan:** Free
4. Click **"Create Web Service"**

#### Deploy Frontend Second:
1. Go to Render Dashboard → **"New Web Service"**
2. Connect your repository
3. Configure:
   - **Name:** `diabetes-frontend`
   - **Environment:** Docker
   - **Root Directory:** `frontend`
   - **Dockerfile Path:** `./Dockerfile`
   - **Plan:** Free
4. Add environment variable:
   - **Key:** `API_BASE_URL`
   - **Value:** `https://diabetes-backend-xxxx.onrender.com` (your backend URL)
5. Click **"Create Web Service"**

---

## 🔧 Local Development

### Backend (FastAPI)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### Frontend (React + Vite)

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend will be available at: http://localhost:5173

**Note:** Update the fallback API URL in `frontend/src/App.jsx` if needed:
```javascript
const API_BASE_URL = window.ENV_CONFIG?.API_BASE_URL || 'http://localhost:8000';
```

---

## 🐳 Docker Testing Locally

### Test Backend:
```bash
cd backend
docker build -t diabetes-backend .
docker run -p 8000:8000 -e FRONTEND_URL=http://localhost:80 diabetes-backend
```

### Test Frontend:
```bash
cd frontend
docker build -t diabetes-frontend .
docker run -p 80:80 -e API_BASE_URL=http://localhost:8000 diabetes-frontend
```

### Test Full Stack with Docker Compose:
Create `docker-compose.yml` in the root:
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - FRONTEND_URL=http://localhost:80

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    environment:
      - API_BASE_URL=http://localhost:8000
    depends_on:
      - backend
```

Run:
```bash
docker-compose up --build
```

---

## 🔑 How Runtime Config Injection Works

### Problem:
React builds create static files. Environment variables are baked in at build time, making it impossible to change the API URL without rebuilding.

### Solution:
1. **`config.js.template`** contains placeholder:
   ```javascript
   window.ENV_CONFIG = {
     API_BASE_URL: '${API_BASE_URL}'
   };
   ```

2. **`docker-entrypoint.sh`** runs at container startup and replaces `${API_BASE_URL}` with the actual value from the environment variable:
   ```bash
   envsubst '${API_BASE_URL}' < /usr/share/nginx/html/config.js.template > /usr/share/nginx/html/config.js
   ```

3. **`index.html`** loads `config.js` before the React app:
   ```html
   <script src="/config.js"></script>
   <script type="module" src="/src/main.jsx"></script>
   ```

4. **`App.jsx`** reads the injected value:
   ```javascript
   const API_BASE_URL = window.ENV_CONFIG?.API_BASE_URL || 'http://localhost:8000';
   ```

This allows the same Docker image to work in any environment! 🎉

---

## 🔒 CORS Configuration

The backend's CORS middleware is configured in `backend/main.py`:

```python
# Get frontend URL from environment
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

origins = [
    FRONTEND_URL,
    "http://localhost:5173",  # Local dev
    "http://localhost:3000",  # Alternative
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**On Render:** The `FRONTEND_URL` is automatically set via `fromService` in `render.yaml`.

---

## 📊 Monitoring & Debugging

### Check Health Endpoints:

**Backend:**
```bash
curl https://diabetes-backend-xxxx.onrender.com/health
```

**Frontend:**
```bash
curl https://diabetes-frontend-xxxx.onrender.com/health
```

### View Logs:
- Go to Render Dashboard
- Click on each service
- Navigate to **"Logs"** tab

### Common Issues:

1. **CORS errors:**
   - Verify `FRONTEND_URL` environment variable in backend
   - Check browser console for exact error

2. **API URL not injected:**
   - Check frontend logs for entrypoint script output
   - Verify `API_BASE_URL` environment variable
   - View generated `/config.js` in browser

3. **Container crashes:**
   - Check logs for build errors
   - Verify Dockerfile paths
   - Ensure health check endpoints return 200

---

## 🎨 Customization

### Update Backend Logic:
Edit `backend/main.py` → Add your ML model, database connections, etc.

### Update Frontend UI:
Edit `frontend/src/App.jsx` and `frontend/src/App.css` → Customize design and functionality

### Add Database:
1. Add a database service in `render.yaml`:
   ```yaml
   databases:
     - name: postgres-db
       databaseName: mydb
       user: myuser
       plan: free
   ```

2. Add environment variable to backend:
   ```yaml
   - key: DATABASE_URL
     fromDatabase:
       name: postgres-db
       property: connectionString
   ```

### Add Redis Cache:
```yaml
- type: redis
  name: redis-cache
  plan: free
  maxmemoryPolicy: allkeys-lru
```

---

## 📦 Production Checklist

- [x] Docker health checks configured
- [x] CORS properly configured
- [x] Environment variables set via `fromService`
- [x] Nginx caching rules configured
- [x] Security headers added
- [x] Multi-stage Docker builds for frontend
- [ ] Add authentication/authorization
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Configure custom domain
- [ ] Set up CI/CD pipeline
- [ ] Add rate limiting
- [ ] Implement logging

---

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

## 📄 License

MIT License - feel free to use this template for your projects!

---

## 🙏 Support

If you find this helpful, please ⭐ star the repository!

**Happy Deploying! 🚀**
