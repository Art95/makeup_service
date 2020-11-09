# Makeup Service Server
Service that allows user apply some makeup effects over video or picture with human face.
Based on the project https://github.com/zllrunning/face-makeup.PyTorch.

## Requirements
* Ubuntu 18.04 or higher
* Python 3.6 or higher
* Nvidia GPU
* CUDA drivers 11.0 or higher
* [Optional] Docker

## Starting application
There are 2 ways to run this app, using python virualenvs or docker.

#### Virtual environment approach
1. To create virtual environment in your terminal run:
```
    python3 -m pip install virtualenv
    python3 -m venv <PATH-FOR-VIRTUAL-ENV>
```
2. Go to folder where you want code to be cloned to
3. Pull project's code 
```
    git clone https://github.com/Art95/makeup_service.git
    cd makeup_service
```
4. To install project and related dependencies run:
```
    source <PATH-FOR-VIRTUAL-ENV>/bin/activate
    pip install -r requirements.txt .
```
5. Make sure $PATH and $LD_LIBRARY_PATH include CUDA libs (change *x*, *y* to your values):
```
    export PATH=/usr/local/cuda-x.y/bin:$PATH
    export LD_LIBRARY_PATH=/usr/local/cuda-x.y/lib64
```
6. [Optional] You can test application by executing
```
    pytest
```
7. Now start the server itself with (supported arguments are *--host*, *--port* and *--debug*):
```
    python makeup_service/server/app.py
```

#### Docker approach
There are 2 dockers available: with and without preinstalled project.

##### Docker with preinstalled project
Docker with preinstalled project is deployment ready and can be used to run service immediately.
Changes in code will demand docker rebuilding.

1. [Optional] If docker is not installed go to [installation guide](https://docs.docker.com/engine/install/ubuntu/)
2. [Optional] You can configure your system to avoid running *sudo* for docker commands [link](https://docs.docker.com/engine/install/linux-postinstall/)
3. Pull docker (alternatively, you can build image yourself by following __Note__ section below)
```
    sudo docker pull abaraniuk/makeup_service:dpl
```
4. Start docker:
```
    sudo docker run --name makeup_service_dpl --gpus all --network host -det -it abaraniuk/makeup_service:dpl
```
5. To stop and remove docker containers run:
```
    sudo docker stop makeup_service_dpl
    sudo docker rm makeup_service_dpl
```

__Note__: to build docker with preinstalled project go to folder where you want project's code to be and run:
```
    git clone https://github.com/Art95/makeup_service.git
    cd makeup_service

    git checkout origin/gc_deployment
    sudo docker build -t <NAME-FOR-IMAGE> .
```

##### Docker without preinstalled project
Docker without preinstalled project gives you higher control over execution and allows code change.
It is also using debug mode which gives more information but works slower.

1. [Optional] If docker is not installed go to [installation guide](https://docs.docker.com/engine/install/ubuntu/)
2. [Optional] You can configure your system to avoid running *sudo* for docker commands [link](https://docs.docker.com/engine/install/linux-postinstall/)
3. Pull docker (alternatively, you can build image yourself by following __Note__ section below)
```
    sudo docker pull abaraniuk/makeup_service:latest
```
4. Go to folder where you want code to be cloned to
5. Clone project's code 
```
    git clone https://github.com/Art95/makeup_service.git
    cd makeup_service
```
6. To start docker run
```
    sudo ./start.sh
```
7. To stop service run Ctrl+C and then
```
    sudo ./clean.sh
```

__Note__: you can look into start.sh and execute docker commands with needed parameters yourself
__Note__: to build docker without preinstalled project go to project's directory and run:
```
    sudo docker build -t <NAME-FOR-IMAGE> .
```

## How to use
There are 2 ways of using this service: using http requests or [client application](https://github.com/Art95/makeup_service_client) for this service.
You can also try 'console' approach.

#### Using http requests
In order to use service you will need application capable of doing http requests. You can use [Postman](https://www.postman.com/), for example.

##### To process image
Request body should be in form:
```
    {
        'hair_color': 'b, g, r',
        'upper_lip_color': 'b, g, r',
        'lower_lip_color': 'b, g, r',
        'source': file
    }
```
where b, g, r - color values for blue, green, red channels in range [0, 255].

Example:
```
    {
        'hair_color': '0, 255, 0',
        'upper_lip_color': '255, 0, 0',
        'lower_lip_color': '0, 0, 255',
        'source': test_image.jpg
    }
```

Request should be send to:
```
    http://<SERVER-ADDRESS>:<PORT>/image
```
   Example:
```
    http://127.0.0.1:5000/image
```

__Note__: In Postman "Send and download" button should be used to save returned file.

##### To process video
Body for request will be the same but video file with 'avi' extension should be provided in 'source'.
Request should be send to:
```
    http://<SERVER-ADDRESS>:<PORT>/video
```

#### Using client application
Client application is provided. In order to use it follow instructions in [client application](https://github.com/Art95/makeup_service_client).

#### Using console
Console version will only work with virtual environment installation.
To use this approach instead of command in step 7 in Virtual Environment instruction run
```
    python bin/main.py
```
You can set other options using arguments. Supported arguments are:
* --video-source (supported values: 0 - web camera, string - path to .avi video file)
* --flip-image (supported values True or False; sets if input images should be flipped)
* --hair-color (3 integer space separated values for b,g,r values of color code)
* --upper-lip-color (same as above)
* --lower-lip-color (same as above)

Example:
```
python bin/main.py --video-source ./test.avi --flip-image True --hair-color 230 50 20 --upper-lip-color 20 70 180 --lower-lip-color 20 70 180
```
