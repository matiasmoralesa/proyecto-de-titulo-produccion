"""
Entrenamiento del modelo de predicción de fallos
"""
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report, confusion_matrix
)
from django.conf import settings


class FailurePredictionTrainer:
    """Entrena y evalúa el modelo de predicción de fallos"""
    
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.feature_columns = [
            'vehicle_type',
            'days_since_last_maintenance',
            'operating_hours',
            'age_years',
            'failure_count_last_6_months',
            'maintenance_count_last_6_months',
            'avg_maintenance_interval_days',
            'failure_rate'
        ]
        self.model_path = os.path.join(
            settings.BASE_DIR,
            'ml_models',
            'failure_prediction_model.pkl'
        )
        self.encoders_path = os.path.join(
            settings.BASE_DIR,
            'ml_models',
            'label_encoders.pkl'
        )
    
    def prepare_data(self, data):
        """
        Prepara los datos para entrenamiento
        
        Args:
            data: Lista de diccionarios con features
            
        Returns:
            tuple: (X, y) features y target
        """
        df = pd.DataFrame(data)
        
        # Encode categorical variables
        if 'vehicle_type' in df.columns:
            le = LabelEncoder()
            df['vehicle_type_encoded'] = le.fit_transform(df['vehicle_type'])
            self.label_encoders['vehicle_type'] = le
        
        # Select features
        feature_cols = [
            'vehicle_type_encoded',
            'days_since_last_maintenance',
            'operating_hours',
            'age_years',
            'failure_count_last_6_months',
            'maintenance_count_last_6_months',
            'avg_maintenance_interval_days',
            'failure_rate'
        ]
        
        X = df[feature_cols].values
        y = df['will_fail'].values
        
        return X, y
    
    def train(self, data, test_size=0.2, random_state=42):
        """
        Entrena el modelo con los datos proporcionados
        
        Args:
            data: Lista de diccionarios con features y target
            test_size: Proporción de datos para test
            random_state: Semilla aleatoria
            
        Returns:
            dict: Métricas de evaluación
        """
        print("Preparando datos...")
        X, y = self.prepare_data(data)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state,
            stratify=y
        )
        
        print(f"Datos de entrenamiento: {len(X_train)}")
        print(f"Datos de prueba: {len(X_test)}")
        print(f"Distribución de clases: {np.bincount(y_train)}")
        
        # Train model
        print("\nEntrenando Random Forest...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            class_weight='balanced',
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        print("\nEvaluando modelo...")
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1_score': f1_score(y_test, y_pred, zero_division=0),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classification_report': classification_report(
                y_test, y_pred, zero_division=0
            )
        }
        
        # Cross-validation
        print("\nValidación cruzada...")
        cv_scores = cross_val_score(
            self.model, X_train, y_train, cv=5, scoring='f1'
        )
        metrics['cv_f1_mean'] = cv_scores.mean()
        metrics['cv_f1_std'] = cv_scores.std()
        
        # Feature importance
        feature_names = [
            'vehicle_type',
            'days_since_maintenance',
            'operating_hours',
            'age_years',
            'failure_count_6m',
            'maintenance_count_6m',
            'avg_maintenance_interval',
            'failure_rate'
        ]
        
        importances = self.model.feature_importances_
        feature_importance = dict(zip(feature_names, importances))
        metrics['feature_importance'] = feature_importance
        
        return metrics
    
    def save_model(self):
        """Guarda el modelo y encoders entrenados"""
        if self.model is None:
            raise ValueError("No hay modelo entrenado para guardar")
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Guardar modelo
        joblib.dump(self.model, self.model_path)
        print(f"Modelo guardado en: {self.model_path}")
        
        # Guardar encoders
        joblib.dump(self.label_encoders, self.encoders_path)
        print(f"Encoders guardados en: {self.encoders_path}")
    
    def load_model(self):
        """Carga el modelo y encoders guardados"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"No se encontró el modelo en: {self.model_path}"
            )
        
        self.model = joblib.load(self.model_path)
        self.label_encoders = joblib.load(self.encoders_path)
        print("Modelo y encoders cargados exitosamente")
    
    def predict(self, features):
        """
        Realiza predicción para un conjunto de features
        
        Args:
            features: Dict con features del activo
            
        Returns:
            dict: Predicción con probabilidad y riesgo
        """
        if self.model is None:
            self.load_model()
        
        # Encode vehicle type
        vehicle_type_encoded = self.label_encoders['vehicle_type'].transform(
            [features['vehicle_type']]
        )[0]
        
        # Prepare features
        X = np.array([[
            vehicle_type_encoded,
            features['days_since_last_maintenance'],
            features['operating_hours'],
            features['age_years'],
            features['failure_count_last_6_months'],
            features['maintenance_count_last_6_months'],
            features['avg_maintenance_interval_days'],
            features['failure_rate']
        ]])
        
        # Predict
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0][1]
        
        # Determine risk level
        if probability >= 0.8:
            risk_level = 'CRITICAL'
        elif probability >= 0.6:
            risk_level = 'HIGH'
        elif probability >= 0.4:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        return {
            'will_fail': bool(prediction),
            'failure_probability': float(probability),
            'risk_level': risk_level
        }
