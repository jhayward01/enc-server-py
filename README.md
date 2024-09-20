# enc-server-py

This portfolio project implements a web-based encryption application 
in Python. It reimplements [the original Go version](https://github.com/jhayward01/enc-server-go).  Two microservices 
are defined in this project - a _front-end_ and _back-end_ service. Both contain 
client and server components.

The _front-end_ service defines three endpoints:

* _StoreRecord_ - This endpoint accepts requests to store a record 
associated with a user ID. The records are encrypted with a 
randomly-generated 32-bit key using AES in GCM mode. User IDs 
are encrypted similarly with a fixed internal AES key (intended 
to provided user anonymity on the data store). Encrypted user IDs
and records are transmitted to the _back-end_ service, and the record 
AES key is returned to the user.
	
* _RetrieveRecord_ - This endpoint accepts requests for record retrieval
via a user ID and AES key. The microservice requests the encrypted 
record from the _back-end_ service, decrypts the record with the AES 
key, and returns it to the user. 

* _DeleteRecord_ - This endpoint accepts requests for record deletion via a user ID. 
	
The _back-end_ service defines three parallel endpoints for storing and retrieving 
encrypted user data. This microservice interacts with a MongoDB instance to provide 
persistent storage of data.

## Installation ##
1. Install project dependencies in a local virtual environment running Python 3.11.
    ```
    make install
    ```

## Running Microservices in Docker Compose (Recommended) ##
1. Start the microservices in _docker-compose_.
    ```
    make up
    ```
    
2. Run the _front-end_ client with trial data.
    ```
    make feclient
    ```

3. Stop the microservices.
    ```
    make down
    ```
    
## Running Microservices on Command Line ##
1. Start a local MongoDB instance with default port 27017 exposed.

2. Start the microservices in separate terminals.
    ```
    make beserver-cmd
    make feserver-cmd
    ```
    
3. In third terminal, run the _front-end_ client with trial data.
    ```
    make feclient-cmd
    ```
    
## Running Microservices in Kubernetes ##
1. Start local Kubernetes cluster.
    ```
    make start-cluster
    ```
    
2. Verify cluster pods are available, and set up port-forwarding.
    ```
    LOCAL_HOST_PORT=7777 && REMOTE_PORT=7777
    FE_POD_NAME=$(minikube kubectl -- get pods | grep enc-server-py-fe | cut -f1 -d' ')
    minikube kubectl -- port-forward $FE_POD_NAME $LOCAL_HOST_PORT:$REMOTE_PORT &
    ```
    
3. Run the _front-end_ client with trial data.
    ```
    make feclient
    ```
    
4. Stop local Kubernetes cluster.
    ```
    make stop-cluster
    ```

## Makefile Commands ##
```
make help                # Print makefile reference
make tests               # Run unit tests (requires local mongodb instance)
make itests              # Run integration tests
make beserver-cmd        # Run BE server in terminal
make beclient-cmd        # Run BE client in terminal
make feserver-cmd        # Run FE server in terminal
make feclient-cmd        # Run FE client in terminal
make beserver            # Run BE server
make beclient            # Run BE client
make feserver            # Run FE server
make feclient            # Run FE client
make up                  # Start BE/FE servers in docker-compose
make down                # Stop BE/FE servers in docker-compose
make start-cluster       # Start application in local Kubernetes cluster
make stop-cluster        # Stop application in local Kubernetes cluster
```
 
## Repo Contents ##
* [cmd](cmd) - Defines main applications for all services.

* [config](config) - Contains microservice configurations for running on _docker-compose_ and command line. 
    * Microservice components will load configuration file `config/config.json` by default - this path may be 
    overridden with environment variable `ENC_SERVER_PY_CONFIG_PATH`.
    * Components will log to directory `/tmp/enc-server-go-logs` by default - this path may be overridden 
    with environment variable `ENC_SERVER_PY_LOG_DIR`.
    * Components will also log to standard output by default - this may be overridden by setting environment 
    variable `ENC_SERVER_PY_LOG_STDOUT` to false.

* [deployments](deployments) - Defines Kubernetes scripts and configurations.

* [enc_server](enc_server) - Defines clients, servers, and utilities for all microservices.

	* [fe](enc_server/fe) - Front-end service providing data encryption.
	
		* [client](enc_server/fe/client)
		
		* [server](enc_server/fe/server)

	* [be](enc_server/be) - Back-end service providing data storage.
	
		* [client](enc_server/be/client)
		
		* [server](enc_server/be/server)
	
	* [utils](enc_server/utils) - Defines shared utilities, including configuration readers, logging, database 
    clients, and network IO.

* [test](test) - Defines unit and integration tests.

## Further Work ##

* Implement alternate HTTP/GRPC service communication.
