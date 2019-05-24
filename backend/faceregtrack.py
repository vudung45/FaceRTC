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


def start_worker(loop,task):
    """Switch to new event loop and run forever"""
    asyncio.set_event_loop(loop)
    print("new worker created")

    loop.run_until_complete(task)

class FacialRecognitionTrack(VideoStreamTrack):

    def __init__(self, face_detector, client, track=None):
        super().__init__()  # don't forget this!
        self.counter = 0
        self.stream = None
        self.frames = []
        self.running = False
        self.face_detector = face_detector
        self.client = client
        # current_loop = asyncio.get_event_loop();
        # self.worker_loop = asyncio.new_event_loop();
        # asyncio.set_event_loop(current_loop)
        # worker = threading.Thread(target=start_worker,args=(self.worker_loop,self.poll_frames()))
        # worker.start()


    def update(self,stream):
        print("updated stream")
        self.stream = stream
        # if not self.running:
        #     self.running = True
        #     print("added new task")
        #     self.worker_loop.create_task(self.poll_frames());

    async def poll_frames(self):

        while True:
            if(self.stream):
                t1 = self.worker_loop.create_task(self.stream.recv())
                frame = await t1;
                self.frames.append(frame.to_nd_array())
            else:
                await asyncio.sleep(0.001)
                pass
            

    async def recv(self):
        if self.stream:
            v_frame = await self.stream.recv()
            image = v_frame.to_ndarray(format="bgr24");
            try:
                #parrellel this shit
                rects, points = self.face_detector.detect_face(image)
                for (i,rect) in enumerate(rects):
                    cv2.rectangle(image,(rect[0],rect[1]),(rect[2],rect[3]),(255,0,0))
                new_frame = av.VideoFrame.from_ndarray(image, format="bgr24")
                new_frame.pts = v_frame.pts
                new_frame.time_base = v_frame.time_base
                v_frame = new_frame
                self.client.add_new_detections(rects);
            except Exception as e:
                print(e)
            return v_frame
        else:
            frame = await super().recv();
            return frame


