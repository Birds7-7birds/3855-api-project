# Auction-a-Bidding-and-Listing-Solution


## Introduction
Post and bid on items while having low latency, high avaliable. Built using Python, Flask, SQLite, Kafka and React

## Services
- Dashboard: React website that lets you see the number of items and bids as well as the highest value bid
- Receiver: validate and forward incoming requests to the processing node
- Storage: save needed data to database
- Processing: process incoming requests and send what is needed to the storage node
- Audit: centralized logging system
- Health Check: verify all nodes are up and running correctly and alerts when one or more is not

## Start Project
To start this project, you must download it.
1. Navigate to the `deployment` directory

2. Run `docker compose up -f [docker-compose_kafka.yml](https://github.com/XavierElChantiry/Auction-a-Bidding-and-Listing-Solution/blob/master/deployment/docker-compose_kafka.yml)` to start a kafka cluster.

3. Set an enviroment variable called `KAFKA_DNS` to the IP of the kafka cluster. if you ran it locally, localhost should work. If you are using powershell use: `New-Item -Path Env:\KAFKA_DNS -Value 'IP_OF_CLUSTER'`

4. For development, you want to use `docker compose up -f [docker-compose_using_dockerfile.yml](https://github.com/XavierElChantiry/Auction-a-Bidding-and-Listing-Solution/blob/master/deployment/docker-compose_using_dockerfile)` as it points to the docker files for each microservice rather than docker images; otherwise, if you have pushed images of these services to dockerhub you can use `docker compose up`.

5. The dashboard should be visible on `[http://localhost:3000](http://localhost:3000)`

## Troubleshooting
- If this does not work, chances are the app_conf.yml did not pick up the enviroment varibale for kafka dns, try hardcoding it and rebuilding images with `docker compose up -f [docker-compose_kafka.yml](https://github.com/XavierElChantiry/Auction-a-Bidding-and-Listing-Solution/blob/master/deployment/docker-compose_kafka.yml) --Build`

## Interacting with the Microservices
The services are setup with API end points, to place a bit or list an item, you need to make post requests to the receiver enpoints. The 2 main endpoints are:
`/listItem` which requires a json body that looks like so
```
{
   "itemID":"string",
   "sellerID":"string",
   "description":"string",
   "maxCount":integers,
   "minPrice":integers,
   "instaBuyPrice":integers,
   "closingTime":"2022-12-15 10:10:04"
}
```
and `/bid` which requires a json body that looks like so
```
{
   "itemID":"string",
   "bidderID":"string",
   "bidID":"string",
   "bidCount": integers,
   "bidPrice": integers,
   "bidTime":"2022-09-15 10:10:04",
}
```

There are other Endpoints such as healthchecks, but they are not designed to be used by people. They are nicely displayed in the openapi.yml for each service if you have intest.

### Foot note
This is a great template to start off from if you have intest in building a Microservice based Architecture. This had storage healthchecks and cenralized logging making debugging easy, uses openapi so its very easy to read and a kafka cluster providing low latency.

There are also a  python_build.groovy in the jenkins directory that can be used to make a new image build each time a commit is made, if you want to use a CI system
