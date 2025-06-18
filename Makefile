.PHONY: help install test lint format clean docker-build docker-run docker-stop

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

test: ## Run tests
	pytest tests/ -v --cov=server --cov-report=html --cov-report=term-missing

test-watch: ## Run tests in watch mode
	pytest tests/ -v --cov=server --cov-report=term-missing -f

lint: ## Run linting
	flake8 server/ tests/
	black --check --diff server/ tests/

format: ## Format code with black
	black server/ tests/

security: ## Run security scan
	bandit -r server/ -f json -o bandit-report.json

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/ bandit-report.json

docker-build: ## Build Docker image
	docker build -t hackathon-langflow .

docker-run: ## Run Docker container
	docker-compose up --build

docker-stop: ## Stop Docker containers
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

dev: ## Start development server
	FLASK_ENV=development FLASK_DEBUG=1 python -m flask run --host=0.0.0.0 --port=5000

prod: ## Start production server
	FLASK_ENV=production python -m flask run --host=0.0.0.0 --port=5000

ci: ## Run CI checks locally
	make lint
	make test
	make security

all: ## Run all checks
	make install
	make lint
	make test
	make security 