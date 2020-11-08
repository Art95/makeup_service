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
1. In your terminal run:
```
    python3 -m pip install virtualenv
    python3 -m venv <PATH-FOR-VIRTUAL-ENV>
```
2. Go to folder where you want code to be cloned to
3. Run 
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
7. Now run the server itself with (Supported arguments are *--host*, *--port* and *--debug*):
```
    python makeup_service/server/app.py
```

#### Docker approach
1. [Optional] If docker is not installed go to [installation guide](https://docs.docker.com/engine/install/ubuntu/)
2. [Optional] You can configure your system to avoid running *sudo* for docker commands [link](https://docs.docker.com/engine/install/linux-postinstall/)
3. Run
```
    sudo docker pull abaraniuk/makeup_service:latest
```
4. Go to folder where you want code to be cloned to
5. Run 
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

## How to use
There are 2 ways of using this service: using http requests or [client application](https://github.com/Art95/makeup_service_client) for this service.

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
