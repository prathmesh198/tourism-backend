import os
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from django.conf import settings

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, 'tourism_model.joblib')

def train_model():
    """
    Trains a simple Linear Regression model on synthetic data.
    Features: year, month
    Target: tourist_count
    """
    # Generate synthetic data
    years = np.repeat(np.arange(2015, 2025), 12)
    months = np.tile(np.arange(1, 13), 10)
    
    # Base count + yearly growth + seasonal variations (summer/winter peaks)
    base_count = 100000
    yearly_growth = (years - 2015) * 5000
    
    # Simple seasonal multipliers
    seasonal_multipliers = np.array([
        0.8, 0.9, 1.1, 1.2, 1.5, 1.6, 1.4, 1.2, 0.9, 1.0, 1.3, 1.4
    ])
    seasonality = np.tile(seasonal_multipliers, 10)
    
    tourist_count = (base_count + yearly_growth) * seasonality
    
    # Add some noise
    noise = np.random.normal(0, 5000, len(tourist_count))
    tourist_count = np.clip(tourist_count + noise, a_min=1000, a_max=None)

    df = pd.DataFrame({
        'year': years,
        'month': months,
        'tourist_count': tourist_count
    })

    X = df[['year', 'month']]
    y = df['tourist_count']

    model = LinearRegression()
    model.fit(X, y)

    # Save the model
    joblib.dump(model, MODEL_PATH)
    print(f"Model trained and saved to {MODEL_PATH}")

def predict_tourists(year, month):
    """
    Predicts tourist count for a given year and month.
    """
    if not os.path.exists(MODEL_PATH):
        train_model()
    
    model = joblib.load(MODEL_PATH)
    prediction = model.predict(pd.DataFrame({'year': [year], 'month': [month]}))
    return int(prediction[0])

if __name__ == "__main__":
    train_model()
