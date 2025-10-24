import { useState } from 'react'
import './App.css'

// Get API URL from runtime config injected by Nginx
const API_BASE_URL = window.ENV_CONFIG?.API_BASE_URL || 'http://localhost:8000';

function App() {
  const [formData, setFormData] = useState({
    glucose: '',
    insulin: '',
    bmi: '',
    age: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          glucose: parseFloat(formData.glucose),
          insulin: parseFloat(formData.insulin),
          bmi: parseFloat(formData.bmi),
          age: parseInt(formData.age)
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="card">
        <h1 className="title">Diabetes Detection System</h1>

        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="glucose">Glucose</label>
            <div className="input-wrapper">
              <input
                type="number"
                id="glucose"
                name="glucose"
                value={formData.glucose}
                onChange={handleChange}
                required
                min="0"
                step="0.1"
                placeholder="16"
              />
              <span className="unit">mg/dL</span>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="insulin">Insulin</label>
            <div className="input-wrapper">
              <input
                type="number"
                id="insulin"
                name="insulin"
                value={formData.insulin}
                onChange={handleChange}
                required
                min="0"
                step="0.1"
                placeholder="142"
              />
              <span className="unit">μU/mL</span>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="bmi">BMI</label>
            <div className="input-wrapper">
              <input
                type="number"
                id="bmi"
                name="bmi"
                value={formData.bmi}
                onChange={handleChange}
                required
                min="0"
                step="0.1"
                placeholder="29.4"
              />
              <span className="unit">kg/m²</span>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="age">Age</label>
            <div className="input-wrapper">
              <input
                type="number"
                id="age"
                name="age"
                value={formData.age}
                onChange={handleChange}
                required
                min="0"
                placeholder="45"
              />
              <span className="unit">years</span>
            </div>
          </div>

          <button type="submit" disabled={loading} className="predict-btn">
            {loading ? 'ANALYZING...' : 'PREDICT'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {result && (
          <div className="result">
            <h3 className="risk-title">Estimated Risk: {result.risk_percentage}%</h3>
            <p className="prediction-text">
              Prediction: <span className={result.prediction === 'High Risk' ? 'positive' : 'negative'}>
                {result.prediction === 'High Risk' ? 'Positive' : 'Negative'}
              </span>
            </p>
            <p className="model-info">Best model: Random Forest</p>
          </div>
        )}

        <div className="disclaimer">
          Educational demo only — not medical advice.
        </div>

        <footer className="footer">
          © 2025 Developed by <strong>Zobayer Al Mahmud</strong>
        </footer>
      </div>
    </div>
  )
}

export default App
