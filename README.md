# Aucition site

This is a proof-of-concept basic auction site.
dependencies: docker

## Start Project
To start this project, you must download it.
1. For development, you want to use the [docker compose copy.](https://github.com/Birds7-7birds/3855-api-project/blob/master/deployment/docker-compose%20copy.yml) as it points to the docker files for each microservice rather than docker images; otherwise, use the normal docker compose.

2. Update all the config files to point to the database you want to use, be it the storage service or a Kafka DNS.
    - If you have a Kafka cluster up and running and wish to connect it to, replace the Kafka DNS's in the [docker compose](https://github.com/Birds7-7birds/3855-api-project/blob/master/deployment/docker-compose.yml).
    - If you do not have a Kafka cluster, in the [docker compose](https://github.com/Birds7-7birds/3855-api-project/blob/master/deployment/docker-compose.yml), point the Kafka DNS to the storage service and switch to the local config of the storage service.

3. Run navigate to the Deployment directory and use  `docker compose up [file]`

