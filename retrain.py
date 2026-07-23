import os
import logging
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from app.ai.pattern_detector import PatternDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_and_merge_data():
    base_dir = r"d:\GitHub_Repository\ksp-ai-module\crime_vision_visualization_dataset\data"
    
    logger.info("Loading datasets...")
    cases_df = pd.read_csv(os.path.join(base_dir, "CaseMaster.csv"))
    accused_df = pd.read_csv(os.path.join(base_dir, "Accused.csv"))
    
    logger.info("Merging datasets...")
    merged_df = pd.merge(cases_df, accused_df, on="CaseMasterID", how="inner")
    return merged_df

def preprocess_features(df):
    logger.info("Preprocessing features...")
    features = ['latitude', 'longitude', 'Year', 'Month', 'AgeYear', 'GenderID', 'CrimeHead']
    df = df.dropna(subset=features)
    X = df[features].copy()
    
    label_encoders = {}
    for col in ['GenderID', 'CrimeHead']:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
        
    y_hotspot = (df['GravityOffence'] == 'Heinous').astype(int).values
    y_risk = ((df['GravityOffence'] == 'Heinous') | (df['AgeYear'] > 30)).astype(int).values
    
    return X.values, y_hotspot, y_risk, label_encoders

def main():
    try:
        df = load_and_merge_data()
        X_train, y_hotspot, y_risk, label_encoders = preprocess_features(df)
        
        detector = PatternDetector()
        detector.train_models(X_train, y_hotspot, y_risk)
        
        # Save to the new app/ai location
        model_path = os.path.join("app", "ai", "trained_model.pkl")
        joblib.dump(detector, model_path)
        logger.info(f"Model successfully saved to {model_path}")
        
        encoder_path = os.path.join("app", "ai", "label_encoders.pkl")
        joblib.dump(label_encoders, encoder_path)
        logger.info(f"Label encoders saved to {encoder_path}")
        
    except Exception as e:
        logger.error(f"Error during training: {str(e)}")

if __name__ == "__main__":
    main()
