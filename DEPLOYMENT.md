# Deployment Guide

This guide explains how to build, push, and deploy the LangGraph Helper Agent to AWS Elastic Beanstalk.

## Docker Build and Push

### Prerequisites
- Docker installed and running
- Docker Hub account (kochurovskyi)
- Docker Hub credentials configured

### Build Docker Image

```bash
# Build the image
docker build -t kochurovskyi/dual-rag:latest .

# Tag for versioning (optional)
docker tag kochurovskyi/dual-rag:latest kochurovskyi/dual-rag:v1.0.0
```

### Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Push the image
docker push kochurovskyi/dual-rag:latest

# Push versioned tag (optional)
docker push kochurovskyi/dual-rag:v1.0.0
```

## AWS Elastic Beanstalk Deployment

### Prerequisites
- AWS account with Elastic Beanstalk access
- AWS CLI configured
- EB CLI installed (`pip install awsebcli`)

### Configuration

**Important**: Environment variables should be set in EB Console or via EB CLI, NOT in `Dockerrun.aws.json` (for security).

**Required Environment Variables:**
- `GOOGLE_API_KEY` (required)
- `AGENT_MODE` (default: "online")
- `TAVILY_API_KEY` (required for online mode)
- `POSTGRES_HOST` (required for online mode)
- `POSTGRES_PORT` (default: "5432")
- `POSTGRES_DB` (default: "documentation_search")
- `POSTGRES_USER` (default: "postgres")
- `POSTGRES_PASSWORD` (required for online mode)
- `POSTGRES_VECTOR_TABLE` (default: "langchain_document_vectors")

### Deploy to Elastic Beanstalk

```bash
# Initialize EB (first time only)
eb init -p docker -r eu-central-1 dual-rag-app

# Create environment (first time only)
eb create dual-rag-env

# Deploy updates
eb deploy

# Or deploy specific version
eb deploy dual-rag-env --version v1.0.0
```

### Environment Variables Setup

Set environment variables in EB console or via EB CLI:

```bash
# Set environment variables
eb setenv GOOGLE_API_KEY=your_key \
         AGENT_MODE=online \
         TAVILY_API_KEY=your_key \
         POSTGRES_HOST=your-host \
         POSTGRES_PASSWORD=your_password
```

### Manual Deployment via EB Console

1. Go to AWS Elastic Beanstalk Console
2. Create new application or select existing
3. Choose "Docker" platform
4. Upload `Dockerrun.aws.json` as source bundle
5. Configure environment variables
6. Deploy

## Image Details

- **Image Name**: `kochurovskyi/dual-rag:latest`
- **Port**: 8501 (Streamlit)
- **Health Check**: `/health` endpoint
- **Base Image**: Python 3.12-slim

## Notes

- The Docker image includes all dependencies
- Index data is pulled via Git LFS if needed
- Environment variables must be set in EB for API keys
- For production, use environment variables instead of hardcoding in Dockerrun.aws.json

