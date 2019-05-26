## Introduction

  FaceRTC is a real-time remote facial recognition service implemented using WebRTC to effectively handle communication between a web browser client and the facial recognition backend server.
	
  
  The idea is to make facial recognition accessible to any devices with connection to internet. (Behaves like a serverless application, doesn't require any installation on the client to perform facial recognition)

## WebRTC

  WebRTC is a free, open-source project that provides web browsers and mobile applications with real-time communication via simple application programming interfaces.

  I handle the communication from the client to the server by creating a Peer to Peer connection, making both the server and the client behave as nodes. The client would sending Webcam image data to the server via WebRTC. The server will then process the image (performs face detection and facial recognition), and send the result back to the client.

## Todo list:

  - ~~Architect a peer to peer connection for client<->server~~

  - ~~Webcam video streaming from client -> server~~

  - ~~Performs Face Detection on the server then send the image result with bounded face region back to the client~~

  - ~~Performs Facial Recognition on detected faces~~

  - Optimization: 
    * Implement trackers for faces on frame to improve Facial Recognition Acurracy (recognize a face through series of frames, instead of one), and to reduce face detection & face recognition load (not having to detect/recog for every frame):

  		* ~~Setup a working framework but not yet implemented a Tracking algorithm~~

    * Implement a more sophisticated `find_match` to find the best matching face_label for a given face feature (embeddings) in dataset.

    * Perform image processing in frontend (Use canvas to draw an UI on top of `<video>`). This would reduce bandwith load because backend will no longer have to send the entire `processed image` back to client. [Should be easy but I'm not very good at html :D]. 

        * Server only has to send locations&labels of faces to client for each frame. Client will then draw rectangle around those faces and put labels on top of them (This is currently done in the backend)


## Demo:

The server below is hosted on my macbook (Performance is not great but acceptable).

The webclient is completely seperated from the facial recognition backend server, no computation is done in the frontend besides sending/receiving image data to/from the server.

Demo on Phone Browser: https://www.youtube.com/watch?v=oWQg18o9fic


![simple demo on desktop browser](https://media.giphy.com/media/Uu5Qb8p5iG9nfdtmqL/giphy.gif)


Status: In-progress