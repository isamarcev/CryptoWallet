run:
	uvicorn base_api.config.app:app --port 8000 --reload

run_sockets:
	uvicorn sockets.config.app:app --port 8001 --reload
run_parser:
	python eth_node/eth_parser.py
