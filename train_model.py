# train_model.py
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
import json
from datetime import datetime

def train_and_save_model():
    """
    Train a Random Forest classifier on the Iris dataset and save the model
    along with training metadata.
    """
    print("Starting model training...")
    
    # Create models directory if it doesn't exist
    os.makedirs('app/models', exist_ok=True)
    
    # Load and prepare data
    print("Loading Iris dataset...")
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Split data
    print("Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42,
        stratify=y
    )
    
    # Train the model
    print("Training Random Forest classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=3,
        n_jobs=-1  # Use all available cores
    )
    
    model.fit(X_train, y_train)
    
    # Make predictions
    print("Making predictions on test set...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, output_dict=True)
    conf_matrix = confusion_matrix(y_test, y_pred).tolist()
    
    # Prepare training metadata
    training_metadata = {
        'model_type': 'RandomForestClassifier',
        'model_version': 'v1',
        'training_date': datetime.now().isoformat(),
        'dataset': 'Iris',
        'dataset_size': len(X),
        'train_size': len(X_train),
        'test_size': len(X_test),
        'features': iris.feature_names,
        'target_names': iris.target_names.tolist(),
        'accuracy': float(accuracy),
        'hyperparameters': {
            'n_estimators': model.n_estimators,
            'random_state': model.random_state,
            'max_depth': model.max_depth
        },
        'classification_report': class_report,
        'confusion_matrix': conf_matrix,
        'feature_importances': model.feature_importances_.tolist()
    }
    
    # Save the model
    model_filename = 'app/models/model_v1.pkl'
    joblib.dump(model, model_filename)
    print(f"Model saved as {model_filename}")
    
    # Save training metadata
    metadata_filename = 'app/models/training_metadata_v1.json'
    with open(metadata_filename, 'w') as f:
        json.dump(training_metadata, f, indent=2)
    print(f"Training metadata saved as {metadata_filename}")
    
    # Print results
    print("\n" + "="*50)
    print("TRAINING RESULTS SUMMARY")
    print("="*50)
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Number of features: {X.shape[1]}")
    print(f"Number of classes: {len(np.unique(y))}")
    print("\nFeature importances:")
    for feature, importance in zip(iris.feature_names, model.feature_importances_):
        print(f"  {feature}: {importance:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))
    
    print("Model training completed successfully!")
    return model, training_metadata

def verify_model_load():
    """
    Verify that the saved model can be loaded correctly.
    """
    print("\nVerifying model can be loaded...")
    
    try:
        model = joblib.load('app/models/model_v1.pkl')
        
        # Test prediction with sample data
        sample_data = np.array([[5.1, 3.5, 1.4, 0.2]])
        prediction = model.predict(sample_data)
        prediction_proba = model.predict_proba(sample_data)
        
        print("✓ Model loaded successfully")
        print(f"✓ Sample prediction: {prediction[0]}")
        print(f"✓ Prediction probabilities: {prediction_proba[0]}")
        
        return True
        
    except Exception as e:
        print(f"✗ Model loading failed: {e}")
        return False

if __name__ == '__main__':
    print("="*60)
    print("ML MODEL TRAINING SCRIPT")
    print("="*60)
    
    try:
        # Train and save model
        model, metadata = train_and_save_model()
        
        # Verify model can be loaded
        load_success = verify_model_load()
        
        if load_success:
            print("\n✅ All operations completed successfully!")
            print(f"Model is ready for deployment in: D:\\Code\\ML_deploy\\app\\models\\")
        else:
            print("\n❌ Model verification failed!")
            
    except Exception as e:
        print(f"\n❌ Training failed with error: {e}")
        raise