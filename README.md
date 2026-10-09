# creatorIQ
Milestone 4: Testing, Deployment & Documentation

Project Overview

CreatorIQ is a creator analytics dashboard designed to track engagement, audience growth, social media performance, and revenue.

Technology Stack

- Backend: Python, FastAPI
- Frontend: React, Vite
- Containerization: Docker and Docker Compose
- Version Control: Git and GitHub

Features Tested

- Backend health endpoint
- Engagement analytics
- Audience growth analytics
- Growth trend analytics
- Social media analytics
- User registration and login validation
- Revenue summary and trends
- Sponsorship information and notifications
- CSV, Excel, and PDF report exports
- Frontend production build

Docker Deployment

The application uses Docker Compose to run two services:

Service| Port
Frontend| 5173
Backend| 8000

Run the Application

From the project root, execute:

docker compose up -d --build

Check service status:

docker compose ps

Stop the services:

docker compose down

Verification

The backend health endpoint returned "{"message":"CreatorIQ API is running"}". The frontend returned the expected HTML response. Analytics and authentication workflows were tested during development.

Limitations

The current social media analytics data includes sample data. External production integrations, persistent user storage, and cloud deployment require further configuration and verification.