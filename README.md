# Description
### To do

Replace node Balance Table with Plot(contains information only about nodes with balance != 0)

Check other clustering algorythms

Publish on Heroku

Data validation

Exeption Class

### Dash Power Grid Analysis

Dashboard visualization base on dash component Cytoscape

Clustering algorythm KMeans

Note: Nodes with generator in lates version marked as squers (images to update)


![image](https://user-images.githubusercontent.com/83120622/173435540-a10cf463-f9c6-41f4-a3e0-f7c11090581d.png)

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

![image](https://user-images.githubusercontent.com/83120622/173435875-32061c3e-525f-4cc9-bda4-b30bad6ea685.png)

1- Choose hour 
2- Amount of clusters
3- Upload your HDF5 file (task file loaded as defoult)
4- Clusters Info
5- Hover Node Info
6- Generators Statistics
7- Node Balance(gen.generate - node.demand - branchFlow.from + branchFlow.to)

To observ information about power flow from and to node set cluters amount to 1, and tap the node
![image](https://user-images.githubusercontent.com/83120622/173435656-9e76d0e3-c830-47db-9349-22f2ea82bc6d.png)

