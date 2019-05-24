


'''
ClientHandler
'''
class Client(object):
    def __init__(self,pc):
        self.pc = pc
        self.detection_queues = []

    def add_new_detections(self,bbs):
        for bb in bbs:
            self.detection_queues.append(bb);
