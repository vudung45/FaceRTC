## Introduction

  FaceRTC is a real-time remote facial recognition service implemented using WebRTC to effectively handle communication between a web browser client and the facial recognition backend server.
	
  
  The idea is to make facial recognition accessible to any devices with connection to internet. (Behaves like a serverless application, doesn't require any installation on the client to perform facial recognition)

## WebRTC

  WebRTC is a free, open-source project that provides web browsers and mobile applications with real-time communication via simple application programming interfaces.

# Implementation 
 - Utilize WebRTC to establish a p2p connection between client web browser and server.
 - Client sends stream of camera images to the backend service. Those images are later asynchronously processed.
 - Detection&Recognition results are then sent back to the webbrowser for presentation accordingly.

## Todo list:

  - ~~Architect a peer to peer connection for client<->server~~

  - ~~Webcam video streaming from client -> server~~

  - ~~Performs Face Detection on the server then send the image result with bounded face region back to the client~~

  - ~~Performs Facial Recognition on detected faces~~

  - Optimization: 
    * Implement trackers for faces on frame to improve Facial Recognition Acurracy (recognize a face through series of frames, ignore motion blur, etc.):

  		* ~~Setup a working framework but not yet implemented a Tracking algorithm~~

    * Implement a more sophisticated `find_match` to find the best matching face_label for a given face feature (embeddings) in dataset.
		* Kd-tree search ( currently simple linear search )
    * Perform image processing at the frontend (Use canvas to draw an UI on top of `<video>`). This would significantly reduce bandwith load, because we currently are sending the entire processed frame back to the browser. [Should be easy but I'm not very good at html :D]. 

## Demo:

The server below is hosted on my macbook (Performance is not great but acceptable).

The webclient could be ran on a seperate machine, no computation is heavy computation is done via the web client.
Demo on Phone Browser: https://www.youtube.com/watch?v=oWQg18o9fic


![simple demo on desktop browser](https://media.giphy.com/media/Uu5Qb8p5iG9nfdtmqL/giphy.gif)


Status: In-progress
