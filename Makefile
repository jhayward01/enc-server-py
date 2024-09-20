# make help                # Print makefile reference
help:
	@grep -e "^\# make" Makefile |  cut -c 3-

# make tests               # Run unit tests
tests:
	python -m unittest discover -s test -t test

# make itests              # Run integration tests
itests:
	./test/itests.sh

 # make install            # Install requirements
install:
	pip install -r requirements.txt

# make beserver-cmd        # Run BE server in terminal
beserver-cmd:
	ENC_SERVER_PY_CONFIG_PATH='config/config.cmd.yaml' PYTHONPATH=. python cmd/beserver/beserver.py

# make beclient-cmd        # Run BE client in terminal
beclient-cmd:
	ENC_SERVER_PY_CONFIG_PATH='config/config.cmd.yaml' PYTHONPATH=. python cmd/beclient/beclient.py

# make feserver-cmd        # Run FE server in terminal
feserver-cmd:
	ENC_SERVER_PY_CONFIG_PATH='config/config.cmd.yaml' PYTHONPATH=. python cmd/feserver/feserver.py

# make feclient-cmd        # Run FE client in terminal
feclient-cmd:
	ENC_SERVER_PY_CONFIG_PATH='config/config.cmd.yaml' PYTHONPATH=. python cmd/feclient/feclient.py

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

# make up                  # Start BE/FE servers in docker-compose
up:
	docker compose up -d --build

# make down                # Stop BE/FE servers in docker-compose
down:
	docker compose down

# make start-cluster       # Start application in local Kubernetes cluster
start-cluster:
	./deployments/minikube/start_cluster.sh

# make stop-cluster        # Stop application in local Kubernetes cluster
stop-cluster:
	./deployments/minikube/stop_cluster.sh
