NAME=twiner
PYTHON=python3
VERSION=0.0.1

help: ## Get help for Makefile
	@echo "\n#### $(NAME) v$(VERSION) ####\n"
	@echo "Available targets:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "\n"

install: ## Install requirements locally
	pip3 install -r requirements.txt

install-dev: ## Install requirements for development
	pip3 install -r requirements-dev.txt

lint: ## Run linter
	@$(PYTHON) -m pylint $(NAME).py

test: ## Run tests
	sudo $(PYTHON) -m pytest -s test/

docker-build: ## Build docker image
	@docker build --no-cache -t $(NAME) .

docker-run: ## Run discord bot inside docker container
	@docker run --privileged --network=host --name twiner $(NAME)

docker-sh: ## Shell into docker container
	@docker run --network=host --privileged -it $(NAME) sh

docker-remove: ## Remove docker container
	@docker container rm $(NAME)

run: ## Run discord bot locally
	@$(PYTHON) $(NAME).py

clean: ## Clean cache and pyc files
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete

.PHONY: help docker-build docker-run docker-sh docker-remove run install install-dev test lint clean