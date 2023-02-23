run:
	uvicorn base_api.config.app:app --port 8000 --reload
run_sockets:
	uvicorn sockets.config.app:app --port 8001 --reload
run_parser:
	python eth_node/eth_parser.py
make celery:
	celery --app base_api.config.celery worker --loglevel=info
make run_ibay:
	uvicorn ibay.config.app:app --port 8005 --reload


run_prod:
	poetry run uvicorn base_api.config.app:app --host 0.0.0.0 --reload
run_sockets_prod:
	poetry run uvicorn sockets.config.app:app --host 0.0.0.0 --reload --port 8001
run_parser_prod:
	poetry run python eth_node/eth_parser.py
make celery_prod:
	poetry run celery --app base_api.config.celery worker --loglevel=info
make run_ibay_prod:
	poetry run uvicorn ibay.config.app:app --host 0.0.0.0 --reload --port 8005


