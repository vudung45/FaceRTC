
import numpy as np
import threading
class FaceDataManager(object):
    def __init__(self):
        self.dataset = {}
        self.lock = threading.Lock()


    def update_label(self, label, embs):
        self.lock.acquire()
        if label != "Unknown" and len(embs) > 0:
            if not label in self.dataset:
                self.dataset[label] = []
            for i in range(len(embs)):
                self.dataset[label].append(embs[i])
        #print(self.dataset)
        self.lock.release()

    def find_match(self, emb, threshold = 0.7):
        '''
        Given a single embedding, find the closest match
            * TO DO: implement a more sophisicated way to find best match *
        '''
        current_min = threshold # i know this is dirty :D
        best_subject = "Unknown"
        for subject in self.dataset:
            distances = [np.sqrt(np.sum(np.square(e-emb))) for e in self.dataset[subject]]
            min_distance = min(distances)
            print(min_distance)
            if min_distance < current_min:
                best_subject = subject
                current_min = min_distance
        return best_subject

