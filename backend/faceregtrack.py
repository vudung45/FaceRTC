from aiortc import (
    RTCIceCandidate,
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
)
class FacialRecognitionTrack(VideoStreamTrack):

    def __init__(self, track=None):
        super().__init__()  # don't forget this!
        self.counter = 0
        self.stream = track

    def update(self,stream):
        self.stream = stream
    

    async def recv(self):
        if self.stream:
            frame = await self.stream.recv();
            return frame
        else:
            frame = await super().recv();
            return frame
