# CI/CD Pipeline Setup 🚀

This project now has a comprehensive CI/CD pipeline set up using GitHub Actions! Here's everything you need to know.

## 🏗️ Pipeline Overview

The CI/CD pipeline consists of several stages:

1. **Testing** - Runs tests across multiple Python versions
2. **Code Quality** - Linting and formatting checks
3. **Security Scanning** - Security vulnerability detection
4. **Build & Deploy** - Creates deployment packages
5. **Notifications** - Success/failure notifications

## 📁 New Files Added

```
.github/workflows/ci-cd.yml    # Main CI/CD pipeline
.flake8                       # Flake8 configuration
pyproject.toml               # Python tool configurations
tests/                       # Test directory
├── __init__.py
└── test_app.py             # Basic tests for your Flask app
Dockerfile                   # Container configuration
docker-compose.yml          # Local development setup
Makefile                    # Development commands
CI_CD_README.md            # This file
```

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   make install
   ```

2. **Run tests:**
   ```bash
   make test
   ```

3. **Start development server:**
   ```bash
   make dev
   ```

4. **Run all checks locally:**
   ```bash
   make ci
   ```

### Docker Development

1. **Build and run with Docker:**
   ```bash
   make docker-run
   ```

2. **Stop containers:**
   ```bash
   make docker-stop
   ```

3. **View logs:**
   ```bash
   make docker-logs
   ```

## 🔧 Available Commands

Run `make help` to see all available commands:

- `make install` - Install dependencies
- `make test` - Run tests with coverage
- `make lint` - Run linting checks
- `make format` - Format code with Black
- `make security` - Run security scan
- `make clean` - Clean up generated files
- `make docker-build` - Build Docker image
- `make docker-run` - Run with Docker Compose
- `make dev` - Start development server
- `make ci` - Run CI checks locally

## 🧪 Testing

The pipeline includes comprehensive testing:

- **Unit Tests** - Tests for Flask endpoints and functions
- **Coverage Reports** - Code coverage analysis
- **Multiple Python Versions** - Tests on Python 3.9, 3.10, 3.11

### Running Tests Locally

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=server --cov-report=html

# Run in watch mode (re-runs on file changes)
pytest tests/ -v -f
```

## 📊 Code Quality

### Linting (Flake8)
- Checks for syntax errors
- Enforces code style
- Configurable rules in `.flake8`

### Formatting (Black)
- Automatic code formatting
- Consistent code style
- Configuration in `pyproject.toml`

### Security (Bandit)
- Security vulnerability scanning
- Generates security reports
- Integrated into CI pipeline

## 🐳 Docker Support

### Production Dockerfile
- Multi-stage build for optimization
- Security best practices
- Health checks included

### Development with Docker Compose
- Easy local development setup
- Volume mounting for live code changes
- Environment variable management

## 🔄 CI/CD Pipeline Details

### Triggers
- Push to `main` or `develop` branches
- Pull requests to `main` branch

### Jobs

1. **Test Job**
   - Matrix testing across Python versions
   - Dependency caching for speed
   - Coverage reporting

2. **Security Scan Job**
   - Runs after tests pass
   - Bandit security scanning
   - Artifact upload for results

3. **Build & Deploy Job**
   - Only runs on `main` branch
   - Creates deployment package
   - Ready for deployment to cloud platforms

4. **Notification Job**
   - Always runs (success or failure)
   - Ready for Slack/Discord integration

## 🚀 Deployment Options

The pipeline creates deployment artifacts that can be deployed to:

- **Heroku** - Add Heroku deployment steps
- **AWS** - Deploy to ECS, Lambda, or EC2
- **Google Cloud** - Deploy to Cloud Run or GKE
- **Azure** - Deploy to App Service or AKS

### Example: Heroku Deployment

Add these steps to the `build-and-deploy` job:

```yaml
- name: Deploy to Heroku
  uses: akhileshns/heroku-deploy@v3.12.14
  with:
    heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
    heroku_app_name: "your-app-name"
    heroku_email: "your-email@example.com"
```

## 🔐 Environment Variables

The pipeline uses these environment variables (set in GitHub Secrets):

- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `TWILIO_AUTH_TOKEN` - Twilio auth token
- `LANGFLOW_API_URL` - Langflow API endpoint
- `LANGFLOW_API_KEY` - Langflow API key
- `GOOGLE_API_KEY` - Google Search API key
- `GOOGLE_CSE_ID` - Google Custom Search Engine ID

## 📈 Monitoring & Notifications

### Success Notifications
- Pipeline completion status
- Test results summary
- Deployment status

### Failure Notifications
- Detailed error messages
- Failed step identification
- Quick fix suggestions

## 🛠️ Customization

### Adding New Tests
1. Create test files in `tests/` directory
2. Follow naming convention: `test_*.py`
3. Use pytest fixtures and mocking

### Modifying Pipeline
1. Edit `.github/workflows/ci-cd.yml`
2. Add new jobs or steps as needed
3. Configure environment-specific settings

### Adding New Tools
1. Update `requirements.txt` with new dependencies
2. Add tool configuration files
3. Update pipeline steps

## 🎯 Next Steps

1. **Push to GitHub** - The pipeline will automatically run
2. **Set up Secrets** - Add environment variables in GitHub
3. **Configure Deployment** - Add deployment steps for your platform
4. **Add Notifications** - Integrate with Slack/Discord
5. **Monitor & Optimize** - Track pipeline performance

## 🆘 Troubleshooting

### Common Issues

1. **Tests Failing**
   - Check test output for specific errors
   - Ensure all dependencies are installed
   - Verify test data and mocks

2. **Linting Errors**
   - Run `make format` to auto-fix formatting
   - Check `.flake8` configuration
   - Review code style guidelines

3. **Docker Issues**
   - Check Docker daemon is running
   - Verify port availability
   - Review Docker logs with `make docker-logs`

### Getting Help

- Check GitHub Actions logs for detailed error messages
- Review the test output for specific failures
- Use `make help` to see available commands

---

🎉 **Your CI/CD pipeline is ready! Push your code and watch the magic happen!** 