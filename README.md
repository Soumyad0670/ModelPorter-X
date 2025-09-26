# 🧠 ML Deploy

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python" />
  <img src="https://img.shields.io/badge/Machine%20Learning-Deployed-success?logo=tensorflow" />
  <img src="https://img.shields.io/badge/Framework-FastAPI%20%7C%20Flask-orange?logo=fastapi" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" />
</p>  

<p align="center">
  <b>A complete end-to-end Machine Learning model deployment project 🚀</b><br>
  From training ➝ saving ➝ serving ➝ exposing APIs ➝ testing in production.
</p>  

---

## 📌 Features

* ✅ Train ML models with reproducible pipelines
* ✅ Save models using `joblib` / `pickle`
* ✅ REST API endpoints with **FastAPI** / **Flask**
* ✅ Frontend integration (optional)
* ✅ Dockerized for easy deployment
* ✅ CI/CD ready (GitHub Actions / Jenkins)
* ✅ Cloud deployment (Heroku / AWS / Azure / GCP)

---

## 📂 Project Structure

```
ML_deploy/
│── data/                # Dataset(s)
│── notebooks/           # Jupyter notebooks for EDA & training
│── models/              # Saved ML/DL models (.pkl, .h5, etc.)
│── src/                 # Core source code
│   ├── train.py         # Model training script
│   ├── predict.py       # Inference script
│   ├── utils.py         # Helper functions
│── app/                 # Deployment code
│   ├── main.py          # FastAPI/Flask entrypoint
│   ├── routes/          # API routes
│   └── templates/       # Frontend templates (if any)
│── tests/               # Unit & integration tests
│── requirements.txt     # Python dependencies
│── Dockerfile           # Docker image build
│── README.md            # Project documentation
```

---

## ⚡ Quickstart

### 🔧 1. Clone the repo

```bash
git clone https://github.com/your-username/ML_deploy.git
cd ML_deploy
```

### 📦 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 🏋️ 3. Train the model

```bash
python src/train.py
```

### 🤖 4. Run API server

```bash
# For FastAPI
uvicorn app.main:app --reload

# For Flask
python app/main.py
```

### 🌍 5. Test the endpoint

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for FastAPI Swagger UI.

Example `cURL` request:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"feature1": 10, "feature2": 5.6, "feature3": 1}'
```

---

## 🐳 Docker Deployment

```bash
# Build image
docker build -t ml-deploy .

# Run container
docker run -p 8000:8000 ml-deploy
```

---

## ☁️ Cloud Deployment

* **Heroku** → Push code, add Procfile, deploy
* **AWS** → Use Elastic Beanstalk / EC2
* **GCP** → Deploy on Cloud Run
* **Azure** → App Service

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📊 Example

Prediction response from API:

```json
{
  "prediction": "Spam",
  "confidence": 0.92
}
```

---

## 👨‍💻 Contributing

1. Fork this repo
2. Create a new branch (`feature-xyz`)
3. Commit changes
4. Open a PR 🚀

---

## 📜 License

This project is licensed under the **MIT License**.

---
