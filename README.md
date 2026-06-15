# CampusWatt ⚡

**A Causal-Predictive Energy Intelligence Platform for Smart University Campuses**

CampusWatt is an intelligent energy management platform that combines machine learning, causal inference, and platform engineering principles to help educational institutions understand, forecast, and optimize energy consumption. The system transforms raw energy and environmental data into actionable recommendations that support sustainability, operational efficiency, and data-driven decision-making.

---

## Overview

Traditional campus energy management systems focus on monitoring consumption after it occurs. CampusWatt goes further by forecasting future energy demand, estimating the impact of operational interventions, and providing decision support for campus administrators.

The platform is designed to be domain-agnostic and adaptable to universities, colleges, and other educational institutions without requiring institution-specific code changes.

---

## Key Features

### Predictive Analytics

* Energy consumption forecasting
* Peak demand prediction
* Trend analysis and anomaly detection

### Causal Intelligence

* Treatment effect estimation
* Intervention impact analysis
* Policy evaluation and decision support

### Feature Engineering Pipeline

* Weather-based energy indicators
* Building utilization metrics
* Academic activity indices
* Energy intensity calculations

### Platform Engineering Components

* Automated preprocessing pipeline
* Modular data ingestion workflow
* Reproducible feature generation
* Scalable model deployment architecture

---

## System Architecture

```text
Raw Data Sources
       │
       ▼
Data Ingestion Layer
       │
       ▼
Feature Engineering Pipeline
       │
       ▼
Feature Store
       │
 ┌─────┴─────┐
 ▼           ▼

Predictive   Causal
Models       Models

 └─────┬─────┘
       ▼

Recommendation Engine
       │
       ▼

API Services
       │
       ▼

Dashboard
```

---

## Data Sources

### Energy Data

* ASHRAE Energy Prediction Dataset

### Environmental Data

* Weather observations
* Temperature
* Humidity
* Atmospheric pressure
* Precipitation

### Building Data

* Building characteristics
* Floor area
* Building type
* Site information

### Academic Activity Data

* Semester cycles
* Holidays
* Examination periods
* Academic calendar events

---

## Project Structure

```text
CampusWatt/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── feature_store/
│
├── notebooks/
│
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── feature_engineering/
│   ├── models/
│   ├── causal/
│   ├── api/
│   └── dashboard/
│
├── tests/
│
├── docker/
│
├── docs/
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/campuswatt.git
cd campuswatt
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Linux / macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Data Pipeline

### Preprocess Data

```bash
python src/preprocessing/preprocess.py
```

### Generate Features

```bash
python src/feature_engineering/features.py
```

### Train Models

```bash
python src/models/train.py
```

### Run Causal Analysis

```bash
python src/causal/estimate_effects.py
```

---

## Machine Learning Pipeline

```text
Raw Data
    │
    ▼
Cleaning
    │
    ▼
Feature Engineering
    │
    ▼
Feature Selection
    │
    ▼
Model Training
    │
    ▼
Forecast Generation
    │
    ▼
Evaluation
```

---

## Technologies Used

### Data Engineering

* Polars
* Pandas
* NumPy

### Machine Learning

* Scikit-Learn
* LightGBM
* XGBoost

### Causal Inference

* EconML
* DoWhy

### Backend

* FastAPI

### Database

* PostgreSQL

### DevOps

* Docker
* GitHub Actions

### Visualization

* Streamlit

---

## Research Objectives

1. Forecast campus energy consumption using machine learning models.
2. Identify key drivers of energy demand.
3. Estimate the impact of operational interventions through causal inference.
4. Develop an intelligent decision support platform for campus sustainability initiatives.

---

## Future Work

* Real-time IoT integration
* Building-level digital twins
* Reinforcement learning for energy optimization
* Multi-campus deployment
* Automated intervention recommendations

---

## License

This project is developed for academic research, platform engineering, and smart campus innovation initiatives.

---

## Authors

Developed as part of the Smart Innovation Campus Challenge and Platform Engineering coursework.

**CampusWatt**
*Turning energy data into intelligent campus decisions.*
