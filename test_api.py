"""
Test script demonstrating the complete ML pipeline workflow
Run this after starting the backend server
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_user_registration():
    """Test user registration"""
    print("\n=== Testing User Registration ===")
    response = requests.post(
        f"{BASE_URL}/api/users/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_user_login(username="testuser"):
    """Test user login"""
    print("\n=== Testing User Login ===")
    response = requests.post(
        f"{BASE_URL}/api/users/login?username={username}"
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_dataset_upload(file_path="datasets/sonar.csv"):
    """Test dataset upload"""
    print("\n=== Testing Dataset Upload ===")
    
    # Check if file exists, if not create a dummy one
    import os
    if not os.path.exists(file_path):
        print(f"Note: {file_path} not found. Create one before testing.")
        return None
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f"{BASE_URL}/api/datasets/upload",
            files=files,
            params={"user_id": 1}
        )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_list_datasets(user_id=1):
    """Test list datasets"""
    print("\n=== Testing List Datasets ===")
    response = requests.get(
        f"{BASE_URL}/api/datasets",
        params={"user_id": user_id}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_start_training(dataset_id=1, model_type="RandomForest"):
    """Test starting model training"""
    print("\n=== Testing Model Training ===")
    response = requests.post(
        f"{BASE_URL}/api/training/train",
        json={
            "dataset_id": dataset_id,
            "model_type": model_type,
            "test_size": 0.2,
            "random_state": 42
        },
        params={"user_id": 1}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_training_status(model_id=1):
    """Test getting training status"""
    print("\n=== Testing Training Status ===")
    response = requests.get(
        f"{BASE_URL}/api/training/status/{model_id}"
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_list_models(user_id=1):
    """Test list trained models"""
    print("\n=== Testing List Models ===")
    response = requests.get(
        f"{BASE_URL}/api/training/models",
        params={"user_id": user_id}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_make_prediction(model_id=1):
    """Test making a prediction"""
    print("\n=== Testing Prediction ===")
    # Example features (60 features for sonar dataset)
    features = [0.0262, 0.0582, 0.1099, 0.1083, 0.0974, 0.1264, 0.0800, 0.0696,
                0.1005, 0.1352, 0.1113, 0.1092, 0.1040, 0.0947, 0.1149, 0.0946,
                0.1223, 0.0818, 0.0906, 0.1007, 0.1026, 0.1184, 0.1008, 0.0807,
                0.1123, 0.0931, 0.1151, 0.1084, 0.1032, 0.1080, 0.1071, 0.1021,
                0.1030, 0.1081, 0.1059, 0.1106, 0.1166, 0.1178, 0.1169, 0.1164,
                0.1072, 0.1092, 0.1088, 0.1228, 0.1253, 0.1165, 0.1190, 0.1090,
                0.1253, 0.0854, 0.0830, 0.1064, 0.1176, 0.1023, 0.0837, 0.0966,
                0.1158, 0.1186, 0.0788, 0.0963]
    
    response = requests.post(
        f"{BASE_URL}/api/predictions/predict/{model_id}",
        json={"features": features},
        params={"user_id": 1}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_prediction_history(model_id=1, user_id=1):
    """Test getting prediction history"""
    print("\n=== Testing Prediction History ===")
    response = requests.get(
        f"{BASE_URL}/api/predictions/history/{model_id}",
        params={"user_id": user_id, "limit": 10}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_model_metrics(model_id=1, user_id=1):
    """Test getting model metrics"""
    print("\n=== Testing Model Metrics ===")
    response = requests.get(
        f"{BASE_URL}/api/predictions/metrics/{model_id}",
        params={"user_id": user_id}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_health_check():
    """Test health check"""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def run_full_workflow():
    """Run the complete workflow"""
    print("\n" + "="*60)
    print("ROCK VS MINE ML BACKEND - FULL WORKFLOW TEST")
    print("="*60)
    
    # 1. Health check
    test_health_check()
    
    # 2. Register user
    user = test_user_registration()
    user_id = user.get("id", 1)
    
    # 3. Login
    test_user_login()
    
    # 4. List datasets (before upload)
    test_list_datasets(user_id)
    
    # 5. Upload dataset (if file exists)
    dataset = test_dataset_upload()
    dataset_id = dataset.get("id", 1) if dataset else 1
    
    # 6. List datasets (after upload)
    test_list_datasets(user_id)
    
    # 7. Start training
    training = test_start_training(dataset_id)
    model_id = training.get("model_id", 1)
    
    # 8. Check training status (may be queued or training)
    time.sleep(2)  # Wait a bit for training to start
    test_training_status(model_id)
    
    # 9. List models
    test_list_models(user_id)
    
    # Note: Prediction tests will fail if model is not trained yet
    # Wait for training to complete before making predictions
    print("\n" + "="*60)
    print("Waiting for model training to complete (max 60 seconds)...")
    print("="*60)
    
    max_wait = 60
    start_time = time.time()
    while time.time() - start_time < max_wait:
        status = test_training_status(model_id)
        if status.get("status") == "trained":
            print("\nModel training completed!")
            break
        time.sleep(5)
    
    # 10. Make prediction (once training is done)
    try:
        test_make_prediction(model_id)
    except Exception as e:
        print(f"Prediction test skipped (model may not be trained): {e}")
    
    # 11. Get prediction history
    try:
        test_prediction_history(model_id, user_id)
    except Exception as e:
        print(f"Prediction history test skipped: {e}")
    
    # 12. Get model metrics
    try:
        test_model_metrics(model_id, user_id)
    except Exception as e:
        print(f"Metrics test skipped: {e}")
    
    print("\n" + "="*60)
    print("WORKFLOW TEST COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    try:
        run_full_workflow()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to backend server!")
        print("Make sure the backend is running: python main.py")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
