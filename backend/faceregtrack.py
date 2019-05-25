import cv2 
from aiortc import (
    RTCIceCandidate,
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
)
import av
import asyncio
import numpy as np
import threading
import cv2
from PIL import Image


def start_worker(loop):
    """Switch to new event loop and run forever"""
    asyncio.set_event_loop(loop)

    loop.run_forever()



class FacialRecognitionTrack(VideoStreamTrack):

    def __init__(self, face_detector, client, track=None):
        super().__init__()  # don't forget this!
        self.counter = 0
        self.stream = None
        self.frames = []
        self.face_detector = face_detector
        self.client = client
        current_loop = asyncio.get_event_loop();
        current_loop.create_task(self.poll_frames());
        
        # self.worker_loop = asyncio.new_event_loop();
        # worker = threading.Thread(target=start_worker,args=(self.worker_loop,))
        # worker.start()
        # self.worker_loop.create_task(self.poll_frames());


    def update(self,stream):
        print("updated stream")
        self.stream = stream

    async def poll_frames(self):
        while True:
            if(self.stream):
                v_frame = await self.stream.recv();
                self.client.purge_trackers(); #because we dont have a tracking algo so do this for now
                image = v_frame.to_ndarray(format="bgr24");
                try:
                #parrellel this shit
                    rects, points = self.face_detector.detect_face(image)
                    for (i,rect) in enumerate(rects):
                        self.client.add_new_detections(rects);
                        self.client.add_new_face(image[min(0,rect[1]):max(len(image),rect[3]),min(0,rect[0]):max(len(image),rect[2])], rect)
                except Exception as e:
                    print(e)
                for tracker in self.client.trackers.values():
                    if tracker.active:
                        cv2.rectangle(image,(tracker.bb[0],tracker.bb[1]),(tracker.bb[2],tracker.bb[3]),(255,0,0))
                self.client.generate_trackers_face_features()
                new_frame = av.VideoFrame.from_ndarray(image, format="bgr24")
                new_frame.pts = v_frame.pts
                new_frame.time_base = v_frame.time_base
                v_frame = new_frame
                self.frames.append(v_frame)
            else:
                await asyncio.sleep(0.001)
                pass

            

    async def recv(self):
        while len(self.frames) == 0:
            #might not be the best idea but im new to asyncio :D
            await asyncio.sleep(0.001) 
        v_frame = None
        if len(self.frames) > 0:
            v_frame = self.frames.pop(0);
        return v_frame


