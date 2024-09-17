# make help                # Print makefile reference
help:
	@grep -e "^\# make" Makefile |  cut -c 3-

# make tests               # Test repo
tests:
	python -m unittest discover -s /Users/johnny/PycharmProjects/enc-server-py/test -t /Users/johnny/PycharmProjects/enc-server-py/test

# make server-be-cmd       # Run BE server in terminal
server-be-cmd:
	ENC_SERVER_GO_CONFIG_PATH='config/config.cmd.yaml' PYTHONPATH=. python cmd/beserver/beserver.py

# make client-be-cmd       # Run BE client in terminal
client-be-cmd:
	ENC_SERVER_GO_CONFIG_PATH='config/config.cmd.yaml' PYTHONPATH=. python cmd/beclient/beclient.py

# make server-fe-cmd       # Run FE server in terminal
server-fe-cmd:
	ENC_SERVER_GO_CONFIG_PATH='config/config.cmd.yaml' PYTHONPATH=. python cmd/feserver/feserver.py

# make client-fe-cmd       # Run FE client in terminal
client-fe-cmd:
	ENC_SERVER_GO_CONFIG_PATH='config/config.cmd.yaml' PYTHONPATH=. python cmd/feclient/feclient.py
