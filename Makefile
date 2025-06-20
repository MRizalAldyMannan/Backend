.PHONY: install run test clean clean-all init-db format lint help

# Default target
help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  run        - Run the Flask application"
	@echo "  test       - Run tests"
	@echo "  clean      - Clean up cache files"
	@echo "  clean-all  - Complete project cleanup (removes DB, migrations, etc.)"
	@echo "  init-db    - Initialize database with sample data"
	@echo "  format     - Format code with black"
	@echo "  lint       - Run flake8 linting"

install:
	pip install -r requirements.txt

run:
	python run.py

test:
	pytest tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -f *.log

clean-all:
	@echo "🧹 Complete project cleanup..."
	@echo "⚠️  This will remove all runtime artifacts, database files, and migrations!"
	@read -p "Do you want to continue? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		$(MAKE) clean; \
		rm -rf instance/; \
		rm -rf migrations/; \
		rm -f .env; \
		rm -rf .vscode/; \
		rm -rf .idea/; \
		rm -f .DS_Store; \
		rm -f Thumbs.db; \
		rm -rf venv/; \
		rm -rf env/; \
		rm -rf .venv/; \
		echo "✅ Project cleaned successfully!"; \
		echo "📋 Ready to share as zip file!"; \
	else \
		echo "❌ Cleanup cancelled."; \
	fi

init-db:
	python init_db.py

format:
	black .

lint:
	flake8 app/ tests/ --max-line-length=88 --ignore=E203,W503 