import asyncio



'''
ClientHandler
'''
class Client(object):
    def __init__(self,pc, _id):
        self.pc = pc
        self.detection_queues = []
       	self.id = _id

    def add_new_detections(self,bbs):
        for bb in bbs:
            self.detection_queues.append(bb);

    async def close(self):
    	if self.pc is not None:
	    	try:
	    		await self.pc.close()
	    		self.pc = None
	    	except Exception as e:
	    		print(e)
	    		
