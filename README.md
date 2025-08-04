# Notejam (Django)

> The Django “Notejam” application for creating and organizing notes & “pads”  
> Backed by PostgreSQL, Fargate‐deployed, with S3+CloudFront for static assets

---

## 🔗 Repositories

- **Application code**: https://github.com/Joshua-Igoni/CPnotejam  
- **Infra (Terraform)**: https://github.com/Joshua-Igoni/CPterraform

---

## 🏗️ Project Layout
```graphql
django/
└── notejam/
├── manage.py
├── notejam/ # project settings & URLs
├── notes/ # Note app: models, views, tests
├── pads/ # Pad app: models, views, tests
├── users/ # Auth: signup, signin, password reset
├── templates/ # HTML templates
├── static/ # local static files (overridden by S3)
├── dockerfile # for building the container
└── requirements.txt # Python dependencies
```
---

## 🚀 Quick Start (Local/Docker)

### 1. Clone & Setup

```bash
git clone git@github.com:Joshua-Igoni/CPnotejam.git
cd CPnotejam/django/notejam
python -m venv venv && source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
Visit: http://localhost:8000/

🧪 Testing
```bash
python manage.py test --verbosity 2
```
Ensures all notes, pads, and users tests pass.

🐳 **Docker**
```bash
# build & tag
docker build -t notejam-app:latest .
# run
docker compose -f docker-compose.yml up --build
```
🌐 **CI/CD (GitHub Actions)**
1. **App Pipeline (.github/workflows/app.yml)**

- Tests on push/PR to CPassignment

- Build & Push Docker image to ECR (via GitHub OIDC)

- Trigger Infra workflow in CPterraform with image_uri

2. **Infra Pipeline (CPterraform repo)**

- Terraform plan & apply on dispatch, consuming image_uri

- Invalidates CloudFront after deploy

🔒 **Security & Secrets**

- Uses GitHub OIDC for AWS role assumption, you can find the policy.json file in terraform repo.

- AWS_ROLE_ARN, DB_PASSWORD stored in GitHub Secrets

## workflow
when you push code to this default branch, it runs tests, builds the app container, pushes it to amazon ECR and triggers terraform deploy pipeline.
terraform provissions the infrastructure if not already provissioned, and provides you with cloudfront url which you can use to access the application.
