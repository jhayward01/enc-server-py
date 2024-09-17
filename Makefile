# make help                # Print makefile reference
help:
	@grep -e "^\# make" Makefile |  cut -c 3-

# make tests               # Test repo
tests:
	python -m unittest discover -s /Users/johnny/PycharmProjects/enc-server-py/test -t /Users/johnny/PycharmProjects/enc-server-py/test

install:				   # Install requirements
	pip install -r requirements.txt

# make beserver-cmd        # Run BE server in terminal
beserver-cmd:
	ENC_SERVER_GO_CONFIG_PATH='config/config.cmd.yaml' PYTHONPATH=. python cmd/beserver/beserver.py

# make beclient-cmd        # Run BE client in terminal
beclient-cmd:
	ENC_SERVER_GO_CONFIG_PATH='config/config.cmd.yaml' PYTHONPATH=. python cmd/beclient/beclient.py

# make feserver-cmd        # Run FE server in terminal
feserver-cmd:
	ENC_SERVER_GO_CONFIG_PATH='config/config.cmd.yaml' PYTHONPATH=. python cmd/feserver/feserver.py

# make feclient-cmd        # Run FE client in terminal
feclient-cmd:
	ENC_SERVER_GO_CONFIG_PATH='config/config.cmd.yaml' PYTHONPATH=. python cmd/feclient/feclient.py

# make beserver            # Run BE server
beserver:
	PYTHONPATH=. python cmd/beserver/beserver.py

# make beclient            # Run BE client
beclient:
	PYTHONPATH=. python cmd/beclient/beclient.py

# make feserver            # Run FE server
feserver:
	PYTHONPATH=. python cmd/feserver/feserver.py

# make feclient            # Run FE client
feclient:
	PYTHONPATH=. python cmd/feclient/feclient.py

# make up                  # Run BE/FE servers in docker-compose
up:
	docker compose up -d --build

# make down                # Stop BE/FE servers in docker-compose
down:
	docker compose down
