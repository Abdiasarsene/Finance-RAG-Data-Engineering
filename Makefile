# ====== MAIN DEFAULT ======
default: radon bandit ruff mypy
	@echo "Default pipeline done"

# ====== QUALITY CODE ======
ruff:
	@echo "Format & Linting"
	@ruff check . --fix

radon: 
	@echo "Cyclo Analysis"
	@radon mi . -s

bandit:
	@echo "Code Analysis"
	@bandit -r . -ll

# ====== EXTERNAL SERVICES ======
milvus: 
	@echo "Milvus Connection"
	@python test_milvus_connection.py

rabbitmq:
	@echo "RabbitMQ Connection"
	@python test_rabbitmq_connection.py

minio:
	@echo "Minio Connection"
	@python test_milvus_connection.py

# ====== INTEGRATION TEST WITH MOCK ======
test_base_worker:
	@echo "Test Base Worker"
	@python test_base_worker.py

test_full_pipeline:
	@echo "Test Full Pipeline"
	@python test_full_pipeline.py

test_business_files:
	@echo "Test Business File"
	@python test_business_files.py

tests: test_business_files test_full_pipeline
	@echo "Integration Test with Mock"

# ====== DOCKER ======
stack-on: 
	@echo "Docker Stack"
	@docker compose -f docker-compose.stack.yaml up -d

stack-off: 
	@echo "Docker Stack"
	@docker compose -f docker-compose.stack.yaml down

observability-on: 
	@echo "Docker Observability"
	@docker compose -f docker-compose.observability.yaml up -d

observability-off: 
	@echo "Docker Observability Off"
	@docker compose -f docker-compose.observability.yaml down

on: stack-on observability-on
	@echo All external services up

off: stack-off observability-off
	@echo All external services exited