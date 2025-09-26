# setup.py
from setuptools import setup, find_packages

setup(
    name="ml-model-api",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==2.3.3",
        "numpy==1.24.3",
        "scikit-learn==1.3.0",
        "joblib==1.3.2",
        "gunicorn==21.2.0",
        "python-dotenv==1.0.0",
        "flasgger==0.9.5",
        "Flask-Limiter==3.5.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.0",
            "pytest-flask==1.3.0",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A production-ready ML model deployment API",
    keywords="flask ml machine-learning api",
    python_requires=">=3.8",
)