# Description

### Dash Power Grid Analysis

Dashboard visualization base on dash component Cytoscape

Clustering algorythm KMeans

![image](https://user-images.githubusercontent.com/83120622/173635762-6eaf443a-81e4-4e0c-b597-19eada4bce18.png)

## Pre-requisites 

HDF5 DataFile (structured "results/hour_{x}/[nodes, branches, gens]

Libraries from requirements.txt

Docker and docker-compose installed with linux containers. (optional)


## Building and running

PowerGridDocker version 

To build the project run "docker build . -t dash-app:latest" command.

Once the build finishes run "docker run -p 8050:8050 dash-app:latest". 

Application should start and be reachable at localhost:8050

## Functionalities

![image](https://user-images.githubusercontent.com/83120622/173636028-91889c60-e9eb-4831-9497-d94b29c7b8c0.png)

1- Choose hour 
2- Amount of clusters
3- Upload your HDF5 file (task file loaded as defoult)
4- Clusters Info
5- Hover Node Info
6- Generators Statistics
7- Node Balance(gen.generate - node.demand - branchFlow.from + branchFlow.to)

To observ information about power flow from and to node set cluters amount to 1, and tap the node
![image](https://user-images.githubusercontent.com/83120622/173636173-31b60985-5060-4f56-b932-f0a7c112b9d5.png)

