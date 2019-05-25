import asyncio


import numpy as np
import threading


'''
ClientHandler
'''
import cv2
import threading


'''
Tracker framework
will implement in the future
'''
class FaceTracker(object):
    def __init__(self, registering = False, label = "Detecting..."):
        self.faces = []
        self.recog_results = {} # {"possible lable" --> count}
        self.embeddings = []
        self.emb_pointer = 0 #pointer to unprocessed embedding
        self.lock = threading.Lock()
        self.bb = None
        self.active = False
        self.recognized = registering
        self.registering = registering
        if registering:
            self.label = label

    def merge_new_embeddings(self, embs):
        self.lock.acquire()
        for i in range(len(embs)):
            self.embeddings.append(embs[i])

        self.lock.release()


    def move_emb_pointer(self, offset):
        self.lock.acquire()
        self.emb_pointer += offset
        self.lock.release()

    def add_new_recog_result(self, result):
        if not self.registering:
            self.lock.acquire()
            if result not in self.recog_results:
                self.recog_results[result] = 0
            self.recog_results[result] += 1
            self.lock.release()

    def update_label(self):
        print(self.recog_results)
        if not self.registering:
            if len(self.recog_results) > 0:
                max_index = np.argmax(self.recog_results.values())
                self.label = list(self.recog_results.keys())[max_index]
                self.recognized = True
            else:
                self.label = "Detecting..."
                self.recognized = False

    def add_new_face(self, face_img, bb):
        '''
        @param face_img 160x160 face image
        @param bb boundning box of the face on frame (used for tracking algorithm)
        '''
        self.faces.append(face_img)
        self.bb = bb
        self.active = True

    def add_new_embeddings(self, emb):
        self.lock.release()
        self.embeddings.append(emb)
        self.lock.release()

    def purge_faces(self):
        self.lock.acquire()
        self.faces.clear()
        self.lock.release()

  
class Client(object):
    def __init__(self, pc, _id, dataset, face_recog):
        self.pc = pc
        self.detection_queues = []
        self.id = _id
        self.registering = False # is the client trying to register a new face
        self.trackers = {} #list of face trackers
        self.count = 0
        self.lock = threading.Lock()
        self.default_label = "Detecting..."


        '''
        global static stuff
        '''
        self.face_recog = face_recog
        self.dataset = dataset #global face features dataset


    def update_tracker_recog_result(self, tracker):
        if(tracker.emb_pointer < len(tracker.embeddings)):
            tracker.lock.acquire()
            processing_embs = tracker.embeddings[tracker.emb_pointer:]
            tracker.lock.release()
            for emb in processing_embs:
                tracker.add_new_recog_result(self.dataset.find_match(emb))
            tracker.move_emb_pointer(len(processing_embs)) #update unprocessed embedding pointer
            tracker.update_label() #determine the updated label based on the new recog result

    def generate_trackers_face_features(self):
        for tracker in self.trackers.values():
            if len(tracker.faces) > 0: #generate in a batch of 5
                tracker.merge_new_embeddings(self.face_recog.get_features(tracker.faces))
                tracker.purge_faces()
            if not tracker.registering:
                self.update_tracker_recog_result(tracker)
        

    def add_new_detections(self,bbs):
        for bb in bbs:
            self.detection_queues.append(bb)

    def add_new_face(self, raw_face_img, bb, desize_size = 160):
        try:
            face_tracker = FaceTracker(registering = self.registering, label = self.default_label)
            face_tracker.add_new_face(cv2.resize(raw_face_img,(desize_size,desize_size)), bb)
            self.trackers[self.count] = face_tracker
            self.count += 1
        except Exception as e:
            print(e)

    def purge_trackers(self):
        remove_list = []
        for track_id in self.trackers:
            if self.trackers[track_id].recognized:
                self.dataset.update_label(self.trackers[track_id].label, self.trackers[track_id].embeddings)
                remove_list.append(track_id)
        self.lock.acquire()
        for track_id in remove_list:
            del self.trackers[track_id]
        self.lock.release()


    def toggle_register_mode(self, label):
        self.registering = True
        self.default_label = label

    def toggle_recognition_mode(self):
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
        self.clients[self.id] = Client(pc, self.id,self.dataset, self.face_recog)
        self.id+=1;
        return self.id - 1;



    def generate_client_face_features(self, _id):
        '''
        Generate face features for a clients
            @param _id client_id
        '''
        assert _id in self.clients
        client = self.clients[_id]
        client.generate_trackers_face_features();
            

    def recognition_loop(self):
        for client_id in self.clients:
            generate_client_face_features(self, client_id)
            # if not self.clients.registering:
            #     update_client_recog_results(self, client_id)

    def get_client(self, _id):
        assert _id in self.clients
        return self.clients[_id]

    async def on_shutdown(self):
        coros = [self.clients[_id].close() for _id in self.clients]
        await asyncio.gather(*coros)
        self.clients.clear()

    async def remove_client(self, _id):
        assert _id in self.clients
        await self.clients[_id].close()



