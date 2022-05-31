.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

all:
	docker-compose -f docker-compose.yml -f keto.yml -f kratos.yml -f hydra.yml up

with_kratos:
	docker-compose -f docker-compose.yml -f kratos.yml up

with_keto:
	docker-compose -f docker-compose.yml -f keto.yml up

down:
	docker-compose -f docker-compose.yml -f keto.yml -f kratos.yml down --remove-orphans
