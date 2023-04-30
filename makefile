NAME=evil-twin
VERSION=0.0.1

help: ## Get help for Makefile
	@echo "\n#### $(NAME) $(VERSION) ####\n"
	@echo "Available targets:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "\n"

build: ## Build software
	@g++ -o $(NAME) -O3 $(wildcard main.cpp src/*.cpp)

run: ## Run software
	@./$(NAME)

docker-build: ## Build docker image
	@docker build -t $(NAME) .

docker-run: ## Run docker image
	@docker run -it --rm $(NAME)
	
clean: ## Remove program and output files
	@rm -f $(NAME) *.txt