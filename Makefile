# =============================
#      MAKEFILE - GENEWEB
# =============================

PROJECT_DIR = geneweb-python
DOCKER_DIR = geneweb-python/docker
REQUIREMENTS_PATH = $(PROJECT_DIR)/requirements.txt
DOCKER_COMPOSE = docker compose -f $(DOCKER_DIR)/docker-compose.yml
PYTEST = pytest -v --cov=geneweb --disable-warnings
PYTHON = python3.10

all: requirements audit conventions test build

requirements:
	@echo "Install python requirements..."
	@pip install -r $(REQUIREMENTS_PATH) || (echo "❌ Module python failed!" && exit 1)
	@echo "✅ Python requirements successfully!"

test:
	@echo "🧪 Running pytest on all tests..."
	@cd $(PROJECT_DIR) && $(PYTEST) tests/ || (echo "❌ Tests failed!" && exit 1)
	@echo "✅ All tests passed successfully!"

build:
	@echo "🐳 Building and launching docker containers..."
	@$(DOCKER_COMPOSE) up --build
	@echo "🚀 Containers started successfully!"

audit:
	@echo "Running pip-audit to detect any vulnerabilities..."
	@pip-audit -r ./$(PROJECT_DIR)/requirements.txt || (echo "❌ Vulnerability found!" && exit 1)
	@echo "✅ No audit founds!"

conventions:
	@echo "Running conventions pycodestyle(PEP8)..."
	@pycodestyle . || (echo "❌ Conventions error found!" && exit 1)
	@echo "✅ No conventions error founds!"

clean:
	@echo "🧹 Cleaning containers and Python caches..."
	@$(DOCKER_COMPOSE) down || true
	@echo "🔍 Searching and removing Python cache folders..."
	@ROOT_DIR="$(PROJECT_DIR)" ; \
	DIRS_TO_DELETE="__pycache__ .python_cache .pytest_cache .coverage" ; \
	for DIR_NAME in $$DIRS_TO_DELETE; do \
		find "$$ROOT_DIR" -type d -name "$$DIR_NAME" -exec rm -rf {} + 2>/dev/null || true; \
	done ; \
	find "$$ROOT_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true ; \
	find "$$ROOT_DIR" -type f -name ".coverage" -delete 2>/dev/null || true ; \
	echo "✅ Cache cleanup done!"

fclean: clean
	@echo "🔥 Removing Docker images..."
	@docker image prune -af --filter "label=geneweb" || true
	@echo "✅ Full clean complete!"

re: fclean all

admin:
	@echo "👑 Launching Admin interface..."
	@cd $(PROJECT_DIR) && $(PYTHON) -m geneweb.gwsetup $(ARGS)

user:
	@echo "🙋 Launching User interface..."
	@cd $(PROJECT_DIR) && $(PYTHON) -m geneweb.gwd $(ARGS)

stop:
	@$(DOCKER_COMPOSE) down

.PHONY: all test build clean fclean re admin user logs stop
