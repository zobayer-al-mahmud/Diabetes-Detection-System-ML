// Diabetes Predictor Frontend JavaScript
// Handles form submission, API communication, and result display

const API_BASE_URL = 'http://localhost:8000';

// DOM elements
const form = document.getElementById('predictionForm');
const resultsDiv = document.getElementById('results');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const inputs = {
    glucose: document.getElementById('glucose'),
    insulin: document.getElementById('insulin'),
    bmi: document.getElementById('bmi'),
    age: document.getElementById('age')
};

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    console.log('Diabetes Predictor loaded');
    
    // Add form submission handler
    form.addEventListener('submit', handleFormSubmission);
    
    // Add input validation
    Object.values(inputs).forEach(input => {
        input.addEventListener('input', validateInput);
        input.addEventListener('blur', validateInput);
    });
    
    // Check API health on load
    checkAPIHealth();
});

// Handle form submission
async function handleFormSubmission(event) {
    event.preventDefault();
    
    // Clear previous results
    hideAllMessages();
    
    // Validate inputs
    const validationResult = validateAllInputs();
    if (!validationResult.isValid) {
        showError(validationResult.message);
        return;
    }
    
    // Show loading
    showLoading();
    
    try {
        // Prepare prediction data
        const predictionData = preparePredictionData();
        
        // Make prediction request
        const result = await makePrediction(predictionData);
        
        // Display results
        showResults(result);
        
    } catch (error) {
        console.error('Prediction error:', error);
        showError(error.message || 'Failed to get prediction. Please try again.');
    } finally {
        hideLoading();
    }
}

// Validate individual input
function validateInput(event) {
    const input = event.target;
    const value = parseFloat(input.value);
    
    // Remove any existing error styling
    input.classList.remove('error');
    
    // Skip validation if empty (optional fields)
    if (input.value.trim() === '') {
        return;
    }
    
    // Check for negative values
    if (value < 0) {
        input.classList.add('error');
        showWarning(`${input.labels[0].textContent} cannot be negative`);
        return;
    }
    
    // Special validation for specific fields
    if ((input.id === 'glucose' || input.id === 'insulin' || input.id === 'bmi') && value === 0) {
        showWarning(`Warning: ${input.labels[0].textContent} value of 0 may affect prediction accuracy`);
    }
    
    if (input.id === 'age' && value > 0 && value < 1) {
        showWarning('Age should be a whole number');
    }
    
    if (input.id === 'bmi' && value > 0 && (value < 10 || value > 60)) {
        showWarning('BMI value seems unusual. Please double-check.');
    }
}

// Validate all inputs before submission
function validateAllInputs() {
    const values = {};
    let hasValidInput = false;
    
    // Collect and validate input values
    for (const [key, input] of Object.entries(inputs)) {
        const value = input.value.trim();
        
        if (value !== '') {
            const numValue = parseFloat(value);
            
            // Check for invalid numbers
            if (isNaN(numValue)) {
                return {
                    isValid: false,
                    message: `${input.labels[0].textContent} must be a valid number`
                };
            }
            
            // Check for negative values
            if (numValue < 0) {
                return {
                    isValid: false,
                    message: `${input.labels[0].textContent} cannot be negative`
                };
            }
            
            values[key] = numValue;
            hasValidInput = true;
        }
    }
    
    // Ensure at least one input is provided
    if (!hasValidInput) {
        return {
            isValid: false,
            message: 'Please provide at least one health parameter for prediction'
        };
    }
    
    return { isValid: true, values };
}

// Prepare data for API request
function preparePredictionData() {
    const data = {
        Pregnancies: null,
        Glucose: null,
        BloodPressure: null,
        SkinThickness: null,
        Insulin: null,
        BMI: null,
        DiabetesPedigreeFunction: null,
        Age: null
    };
    
    // Map form inputs to API fields
    const inputMapping = {
        glucose: 'Glucose',
        insulin: 'Insulin',
        bmi: 'BMI',
        age: 'Age'
    };
    
    // Set values from form inputs
    for (const [inputId, apiField] of Object.entries(inputMapping)) {
        const value = inputs[inputId].value.trim();
        if (value !== '') {
            data[apiField] = parseFloat(value);
        }
    }
    
    console.log('Prediction data:', data);
    return data;
}

// Make prediction API call
async function makePrediction(data) {
    const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
}

// Check API health
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            const data = await response.json();
            console.log('API health check passed:', data);
        } else {
            console.warn('API health check failed');
        }
    } catch (error) {
        console.warn('Could not reach API:', error.message);
    }
}

// Display prediction results
function showResults(result) {
    const riskPercentage = Math.round(result.prob * 100);
    const label = result.label;
    const modelName = result.best_model;
    
    // Update result content
    const riskElement = resultsDiv.querySelector('.risk-percentage');
    const labelElement = resultsDiv.querySelector('.prediction-label');
    const modelElement = resultsDiv.querySelector('.best-model-info');
    
    riskElement.textContent = `Estimated Risk: ${riskPercentage}%`;
    labelElement.textContent = `Prediction: ${label}`;
    labelElement.className = `prediction-label ${label.toLowerCase()}`;
    modelElement.textContent = `Best model: ${modelName}`;
    
    // Show results
    resultsDiv.classList.remove('hidden');
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show loading state
function showLoading() {
    loadingDiv.classList.remove('hidden');
    
    // Disable form
    const submitBtn = form.querySelector('.predict-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Analyzing...';
}

// Hide loading state
function hideLoading() {
    loadingDiv.classList.add('hidden');
    
    // Re-enable form
    const submitBtn = form.querySelector('.predict-btn');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Predict';
}

// Show error message
function showError(message) {
    const errorMessage = errorDiv.querySelector('.error-message');
    errorMessage.textContent = message;
    errorDiv.classList.remove('hidden');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorDiv.classList.add('hidden');
    }, 5000);
}

// Show warning message (temporary)
function showWarning(message) {
    console.warn(message);
    
    // You could implement a toast notification here
    // For now, we'll just log it
}

// Hide all message divs
function hideAllMessages() {
    resultsDiv.classList.add('hidden');
    loadingDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
}

// Utility function to format numbers
function formatNumber(num, decimals = 1) {
    return Number(num).toFixed(decimals);
}

// Handle network errors gracefully
window.addEventListener('online', () => {
    console.log('Connection restored');
});

window.addEventListener('offline', () => {
    showError('No internet connection. Please check your connection and try again.');
});