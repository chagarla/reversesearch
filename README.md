# Reverse Search Agent – Setup & Troubleshooting Guide

This document summarizes the full setup process and troubleshooting steps taken to get the **Reverse Search Agent** running successfully on **Streamlit Cloud**.

---

## 🚀 Project Overview

* A **Streamlit app** that takes an **answer** as input and generates **possible questions** that could logically lead to that answer.
* Uses the **OpenAI Python SDK** for language model calls.
* Hosted on **Streamlit Cloud** with GitHub integration.

---

## 🛠️ Setup Steps

### 1. Install Dependencies (Local Dev)

* Installed the correct OpenAI SDK:

  ```bash
  pip install openai
  ```
* Installed Streamlit:

  ```bash
  pip install streamlit
  ```
* (Optional) Installed dotenv for local API key management:

  ```bash
  pip install python-dotenv
  ```

### 2. API Key Setup

* Obtained an **OpenAI API key** from [platform.openai.com](https://platform.openai.com).
* Options used for setting it up:

  * **PyCharm Env Vars**: added `OPENAI_API_KEY=your_key` in Run Config → Environment variables.
  * **Direct Code (quick test)**:

    ```python
    client = OpenAI(api_key="your_api_key_here")
    ```
  * **.env file (cleaner)** with `python-dotenv`:

    ```env
    OPENAI_API_KEY=your_api_key_here
    ```

### 3. Quota Fix

* Encountered **`429 insufficient_quota`** errors.
* Solution: Added billing details on OpenAI account (trial credits had expired).

### 4. Streamlit Cloud Deployment

* Created `requirements.txt` in repo root:

  ```
  streamlit
  openai
  python-dotenv
  ```
* Committed & pushed to GitHub.
* Streamlit Cloud auto-installed dependencies.

### 5. API Key in Streamlit Cloud

* Set secret key under **App Settings → Secrets**:

  ```toml
  OPENAI_API_KEY="your_real_api_key_here"
  ```
* Updated code to load key from env:

  ```python
  import os
  from openai import OpenAI

  client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
  ```

---

## 🐞 Troubleshooting Log

1. **Wrong package install** → Accidentally installed `OpenAPI`, fixed with `pip uninstall openapi` + `pip install openai`.
2. **API key missing** → Fixed by setting env vars in PyCharm / .env / Streamlit secrets.
3. **Quota exceeded** → Enabled billing on OpenAI platform.
4. **Module not found (Streamlit)** → Fixed by adding `streamlit` to `requirements.txt`.
5. **Secrets management** → Moved API key to Streamlit Cloud secrets to avoid hardcoding.

---

## ✅ Final State

* Fully functional **Reverse Search Agent** deployed on Streamlit Cloud.
* Users can:

  1. Enter an answer.
  2. Select a domain (Math, History, Coding, etc.).
  3. See validated possible questions.
* App is clean, shareable via Streamlit Cloud link.

---

## 📂 Minimal Repo Structure

```
reverse-search-agent/
│
├── app.py              # Main Streamlit app code
├── requirements.txt    # Dependencies for Streamlit Cloud
├── .env (optional)     # Local dev secrets (not committed)
└── README.md           # Setup instructions
```

---

This doc should serve as a quick reference for setup, troubleshooting, and deployment. Future contributors can follow these steps to replicate the environment or extend the project.
