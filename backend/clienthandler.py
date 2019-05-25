import asyncio


import numpy as np
import threading
'''
ClientHandler
'''
class Client(object):
    def __init__(self,pc, _id):
        self.pc = pc
        self.detection_queues = []
        self.id = _id
        self.registering = False # is the client trying to register a new face
        self.embeddings = []
        self.recog_results = {} # {"possible lable" --> count}
        self.faces = []
        self.label = "Detecting..."
        self.lock = threading.Lock()

    def add_new_detections(self,bbs):
        for bb in bbs:
            self.detection_queues.append(bb);


    def update_label():
        if(recog_result > 0):
            max_index = np.argmax(self.recog_result.values())
            self.label = self.recog_results.keys()[max_index]
        else:
            self.label = "Detecting"

    def add_new_face(self, raw_face_img, desize_size = 160):
        self.lock.acquire()
        self.faces.append(cv2.resize(raw_face_img,(desize_size,desize_size)))
        self.lock.release()

    def purge_faces(self):
        self.lock.acquire()
        self.faces.clear()
        self.lock.release()

    def add_new_embeddings(self, emb):
        self.lock.release()
        self.embeddings.append(emb)
        self.lock.release()


    def toggle_register_mode():
        self.registering = True

    def toggle_recognition_mode():
        self.registering = False

    async def close(self):
        if self.pc is not None:
            try:
                await self.pc.close()
                self.pc = None
            except Exception as e:
                print(e)

'''
Manage all clients
'''
class ClientManager(object):
    def __init__(self, dataset, face_recog):
        self.clients = dict() #a dictionary of clients
        self.id = 0
        self.face_recog = face_recog
        self.dataset = dataset #global face features dataset

    def create_new_client(self, pc):
        self.clients[self.id] = Client(pc, self.id)
        self.id+=1;
        return self.id - 1;

    def generate_client_face_features(self, _id):
        '''
        Generate face features for a clients
            @param _id client_id
        '''
        assert _id in self.clients
        if len(self.clients[_id].faces) > 5: #generate in a batch of 5
            self.face_recog.get_features(self.clients[_id].faces)
            self.clients[_id].purge_faces()
            if not self.clients[_id].registering:
                self.clients[_id].update_label()
        # else do nothing



    def get_client(self, _id):
        assert _id in self.clients
        return self.clients[_id]

    async def on_shutdown(self):
        coros = [self.clients[_id].pc.close() for _id in self.clients]
        await asyncio.gather(*coros)
        self.clients.clear()

    async def remove_client(self, _id):
        assert _id in self.clients
        await self.clients[_id].close()



