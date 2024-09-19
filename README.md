# enc-server-py

This project implements an encryption service in Python. It reimplements 
[the original Go version](https://github.com/jhayward01/enc-server-go).

Two microservices are defined in this project - a front-end and back-end 
service. Both contain client and server components.

The _front-end_ service defines three endpoints:

* _StoreRecord_ - This endpoint accepts requests to store a record associated with a user ID. The records are encrypted with a randomly-generated 32-bit key using AES in GCM mode. User IDs are encrypted similarly with a fixed internal AES key (intended to provided user anonymity on the data store). Encrypted user IDs and records are transmitted to the _back-end_ service, and the record AES key is returned to the user.
	
* _RetrieveRecord_ - This endpoint accepts requests for record retrieval via a user ID and AES key. The microservice requests the encrypted record from the _back-end_ service, decrypts the record with the AES key, and returns it to the user. 

* _DeleteRecord_ - This endpoint accepts requests for record deletion via a user ID. 
	
The _back-end_ service defines three related endpoints for storing and retrieving encrypted user data. This microservice interacts with a MongoDB instance to provide persistent storage of data. (Note: this could have been implemented solely as data store client, but was done as a full microservice to add depth to the project.)

## Running Microservices in Docker (Recommended) ##
1. Start the microservices in _docker-compose_.
    ```
    make servers
    ```
    
2. Run the _front-end_ client with trial data.
    ```
    make client
    ```
    
## Running Microservices on Command Line ##
1. Start a local MongoDB instance with default port 27017 exposed.

2. Start the microservices in seperate terminals.
    ```
    make server-be-cmd
    make server-fe-cmd
    ```
    
2. In third terminal, run the _front-end_ client with trial data.
    ```
    make client
    ```
    
## Running Microservices in Kubernetes ##
1. Start local Kubernetes cluster.
    ```
    make start-cluster
    ```
    
2. Verify cluster pods are available, and set up port-forwarding.
    ```
    LOCAL_HOST_PORT=7777 && REMOTE_PORT=7777
    KC_POD_NAME=$(minikube kubectl -- get pods | grep enc-server-py-fe | cut -f1 -d' ')
    minikube kubectl -- port-forward $KC_POD_NAME $LOCAL_HOST_PORT:$REMOTE_PORT &
    ```
    
3. Run the _front-end_ client with trial data.
    ```
    make client
    ```
    
4. Stop local Kubernetes cluster.
    ```
    stop-cluster
    ```

## Makefile Commands ##
```
make help                # Print makefile reference
make fmt                 # Run format and static analysis tools
make build               # Build repo
make tests               # Test repo
make build-all           # Format, build, and test repo
make install-client-fe   # Install FE client
make install-client-be   # Install BE client
make install-server-fe   # Install FE server
make install-server-be   # Install BE server
make install-servers     # Install BE/FE servers
make all                 # Install all binaries
make client              # Run FE client
make servers             # Run BE/FE servers in docker-compose
make itests              # Run integration tests
make stop                # Stop BE/FE servers in docker-compose
make server-be-cmd       # Run BE server in terminal
make server-fe-cmd       # Run FE server in terminal
make start-cluster       # Start application in local Kubernetes cluster
make stop-cluster        # Stop application in local Kubernetes cluster
```
 
## Repo Contents ##
* [cmd](cmd) - Defines main applications for all services.

* [config](config) - Contains microservice configurations for running on _docker-compose_ and command line. 
    * _Microservice components will load configuration file `config/config.json` by default - this path may be overriden with environment variable `ENC_SERVER_GO_CONFIG_PATH`._
    * _Components will log to directory `/tmp/enc-server-go-logs` by default - this path may be overriden with environment variable `ENC_SERVER_GO_LOG_DIR`._
    * _Components will also log to standard output by default - this may be overriden by setting environment variable `ENC_SERVER_GO_LOG_STDOUT` to false._

* [deployments](deployments) - Defines optional Kubernetes scripts and configurations.

* [pkg](pkg) - Defines interfaces, clients, and servers for all microservices.

	* [fe](pkg/fe) - Front-end service providing data encryption.
	
		* [client](pkg/fe/client)
		
		* [server](pkg/fe/server)

	* [be](pkg/be) - Back-end service providing data storage.
	
		* [client](pkg/be/client)
		
		* [server](pkg/be/server)
	
	* [utils](utils) - Defines shared utilities, including configuration readers, logging, database clients, and network IO.

* [test](test) - Defines integration tests.

## Further Work ##

* Implement alternate HTTP/GRPC service communication.
