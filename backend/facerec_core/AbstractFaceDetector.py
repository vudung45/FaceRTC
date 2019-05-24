from abc import ABC, abstractmethod 


class AbstractDetector(ABC):
	@abstractmethod
	def detect_face(self, img, *args):
		pass