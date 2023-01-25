run:
	poetry run uvicorn base_api.config.app:app --port 4552 --reload

run_sockets:
	uvicorn sockets.config.app:app --reload --port 8001