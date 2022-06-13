# Description

### Dash Power Grid Analysis

Dashboard visualization base on dash component Cytoscape

Clustering algorythm KMeans

![image](https://user-images.githubusercontent.com/83120622/173416579-67854f65-9579-484f-88f4-7e2453f9db80.png)

## Pre-requisites 

HDF5 DataFile (structured "results/hour_{x}/[nodes, branches, gens]

Libraries from requirements.txt

Docker and docker-compose installed with linux containers. (optional)


## Building and running

To build the project run docker-compose build command.

Once the build finishes run docker-compose up -d. Application should start and be reachable at localhost

## Functionalities

![image](https://user-images.githubusercontent.com/83120622/173417134-e625a243-3292-4c7b-b94f-1107fc998de6.png)

1- Choose hour 
2- Amount of clusters
3- Upload your HDF5 file (task file loaded as defoult)
4- Clusters Info
5- Hover Node Info
6- Generators Statistics
7- Node Balance

To observ information about power flow from and to node set cluters amount to 1, and tap the node
![image](https://user-images.githubusercontent.com/83120622/173417738-33debf5c-0347-4064-98de-ece631f3e822.png)

