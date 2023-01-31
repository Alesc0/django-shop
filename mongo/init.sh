#! /bin/bash

mongoimport --host mongodb --db dbproj --collection products --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --file /mongo-seed/products.json --authenticationDatabase admin
mongoimport --host mongodb --db dbproj --collection users --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --file /mongo-seed/users.json --authenticationDatabase admin