# Deployment Documentation

> **Status:** 🚧 Coming Soon - Being Organized

This directory will contain comprehensive deployment documentation for various platforms and scenarios.

## Planned Content

### DOCKER.md
- Docker setup and configuration
- Docker Compose usage
- Container customization
- Volume management
- Networking setup

### CLOUD.md
- Google Cloud Platform deployment
- AWS deployment
- Azure deployment
- Heroku deployment
- Platform comparisons

### DESKTOP_ON_CLOUD.md
- VNC-based desktop access
- noVNC web interface
- Remote desktop configuration
- Performance optimization

### WORKFLOW_CONFIGURATION.md
- GitHub Actions setup
- CI/CD pipeline configuration
- Automated testing
- Automated releases
- Deployment automation

## For Now

Until this directory is fully populated, please refer to:

- **[../DEPLOYMENT.md](../../DEPLOYMENT.md)** - Main cloud deployment guide (in root)
- **[../development/DESKTOP_ON_CLOUD.md](../development/DESKTOP_ON_CLOUD.md)** - VNC deployment
- **[../development/WORKFLOW_CONFIGURATION.md](../development/WORKFLOW_CONFIGURATION.md)** - CI/CD workflows

## Quick Links

### One-Click Cloud Deploy
See [DEPLOYMENT.md](../../DEPLOYMENT.md) for:
- Google Cloud Run deployment
- One-click deploy button
- Environment configuration
- Cloud Storage setup

### Docker Deployment
```bash
# Basic Docker run
docker run -p 5000:5000 ghcr.io/primoscope/coomerdl

# Docker Compose
docker-compose up -d
```

### Local Development
See [../development/BUILDING.md](../development/BUILDING.md) for local setup.

---

**Estimated Availability:** Phase 5 of documentation reorganization  
**See:** [../DOCUMENTATION_REORGANIZATION.md](../DOCUMENTATION_REORGANIZATION.md) for timeline
