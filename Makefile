run:
	poetry run uvicorn base_api.config.app:app --port 8000 --reload

run_sockets:
	uvicorn sockets.config.app:app --reload --port 8001