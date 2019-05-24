import argparse
import asyncio
import json
import logging
import os
import platform
import ssl

from aiohttp import web

from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer

from faceregtrack import FacialRecognitionTrack
from facerec_core.mtcnn_detect import MTCNNDetect
from facerec_core.tf_graph import FaceRecGraph
from clienthandler import Client
ROOT = os.path.dirname(__file__)


async def index(request):
    content = open(os.path.join(ROOT, "../frontend/client.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def main_js(request):
    content = open(os.path.join(ROOT, "../frontend/js/main.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)

async def video_stream_js(request):
    content = open(os.path.join(ROOT, "../frontend/js/video_stream.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)


async def offer(request):
    params = await request.json()
    print(params);
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    new_client = Client(pc)
    clients.add(Client(pc))

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        print("ICE connection state is %s" % pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            await pc.close()
            clients.discard(new_client)

    faceregtrack = FacialRecognitionTrack(face_detect, new_client);

    @pc.on("track")
    def on_track(track):
        print("Track %s received" % track.kind)
        if track.kind == "video":
            faceregtrack.update(track);
            


    await pc.setRemoteDescription(offer)

    for t in pc.getTransceivers():
        if t.kind == "video":
            pc.addTrack(faceregtrack)


    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    print("Connection with client formed")
    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )




clients = set()



async def on_shutdown(app):
    coros = [client.pc.close() for client in clients]
    await asyncio.gather(*coros)
    clients.clear()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FaceRTC")
    parser.add_argument("--cert-file", help="SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", help="SSL key file (for HTTPS)")
    parser.add_argument(
        "--port", type=int, default=8080, help="Port for HTTP server (default: 8080)"
    )
    parser.add_argument("--verbose", "-v", action="count")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if args.cert_file:
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(args.cert_file, args.key_file)
    else:
        ssl_context = None

    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    app.router.add_get("/", index)
    app.router.add_get("/js/main.js", main_js)
    app.router.add_get("/js/video_stream.js", video_stream_js)
    app.router.add_post("/offer", offer)
    MTCNNGraph = FaceRecGraph();
    face_detect = MTCNNDetect(MTCNNGraph, scale_factor=2); #scale_factor, rescales image for faster detection
    web.run_app(app, port=args.port, ssl_context=ssl_context, host="127.0.0.1")
