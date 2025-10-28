# =============================
#      MAKEFILE - GENEWEB
# =============================

PROJECT_DIR = geneweb-python
DOCKER_COMPOSE = docker compose -f $(PROJECT_DIR)/docker-compose.yml
PYTEST = pytest -v --disable-warnings
PYTHON = python3.10

all: test build

test:
	@echo "🧪 Running pytest on all tests..."
	@cd $(PROJECT_DIR) && $(PYTEST) tests/ || (echo "❌ Tests failed!" && exit 1)
	@echo "✅ All tests passed successfully!"

build:
	@echo "🐳 Building and launching docker containers..."
	@$(DOCKER_COMPOSE) up --build
	@echo "🚀 Containers started successfully!"

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
