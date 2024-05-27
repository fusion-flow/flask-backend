This is the backend of the navigational chatbot which assist people with aphasia to navigate a wordpress website. Processing inputs from multiple modalities such text, audio, and video that is taken from frontend and sending output back to frontend is implemented in the backend. The inputs will be sent to different models according to their type. Following design diagram shows the communication between all the components.

![Design](https://github.com/fusion-flow/flask-backend/assets/83814896/ce9579bc-bd5f-4b1b-a340-1e745e4f06eb)

We get the inputs from the chatbot activated in the WordPress website as a WordPress plugin. The audio, video and text inputs are then communicated to the backend using websockets. Backend would be a combination of multiple models and the main backend would be developed using Flask. There are 3 main endpoints for transcription, gesture recognition and intent classification. The models are deployed with docker and the docker images are used to call the models. Here the Flask backend would be communicating the respective inputs to the respective models as follows,

- The audio input would be sent to the transcription model which would use Whisper of OpenAI to transcribe the audio input. The transcribed audio would be sent back to the Flask backend.
- The video input taken from the video camera would be sent to the backend as frames of the video taken during a specified interval. Those frames would be sent to the gesture recognition model and the model will output the detected number. 
- The text inputs and the transcribed text would be sent to the intent classifier model and it would output separate intents classified using the classifier. 

The intents and the detected gestures would be sent to the fusion component. The intents from each model will be fused in the fusion model and the selected intent/s would be sent to the Flask backend where the dialog manager generate the chatbot response. The generated response would be emitted to the frontend through the websocket and displayed in the chatbot UI.

# flask-backend

Main backend is implimented in this project using Flask. Following is the guidance to setup the project locally.

## Backend setup

You can assign port values to the following variables as desired.

PORT_TXTAI

PORT_TRANSCRIPTION
PORT_GESTURE

### Flask Backend Setup

* Clone the code of flask-backend from [https://github.com/fusion-flow/flask-backend](https://github.com/fusion-flow/flask-backend).
* Create a .env file in the root folder, copy content from the .env.example and add values for the env variable like the following.

CLASSIFICATION_MODEL_ENDPOINT=http://localhost:PORT_TXTAI

TRANSCRIPTION_MODEL_ENDPOINT=[http://localhost:](http://localhost:8000)PORT_TRANSCRIPTION

RECOGNIZER_MODEL_ENDPOINT=http://localhost:PORT_GESTURE

CLIENT_URL=[http://fusionflow2.local/](http://fusionflow2.local/)

* Create a virtual environment to run the code. (Python version=3.9.12).
* Install libraries

  * pip install -r requirements.txt
* Run the backend using the following command.
* python app.py

### Txtai api

* Pull the docker image from the docker hub.

  * docker pull awesomenipun/txtai-api
* Run the docker image.
* docker run -p PORT_TXTAI:8000 awesomenipun/txtai-api
* Go to the fastapi - [http://localhost:PORT_TXTAI/docs#/](http://localhost:8080/docs#/)
* Add the keywords from the following doc using /add post request.

[https://docs.google.com/document/d/1tsNlhrdAzFWb2l1u4SSbKJqBZgFQs9T-eu-eAX3b53M/edit?usp=sharing](https://docs.google.com/document/d/1tsNlhrdAzFWb2l1u4SSbKJqBZgFQs9T-eu-eAX3b53M/edit?usp=sharing)

* Index those data using /index endpoint.

### Gesture Recognition Model Setup

* Pull the docker image from the docker hub.
  * docker pull awesomenipun/gesture-recognition-1:latest
* Run the docker image.
* docker run -p PORT_GESTURE:80 awesomenipun/gesture-recognition-1:latest
* For LOCAL_PORT you can use any available port in local machine.

### Transcription Model Setup

* Pull the docker image from the docker hub.
  * docker pull sanduaye/whisper-api:latest
* Run the docker image.
* docker run -p PORT_TRANSCRIPTION:8000 sanduaye/whisper-api:latest
