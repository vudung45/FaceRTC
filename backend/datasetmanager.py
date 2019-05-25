
import numpy as np

class FaceDataManager(object):
	def __init__(self):
		self.dataset = {}


	def update_label(self, label, embs):
		if label != "Unknown":
			if label in self.dataset:
				self.dataset[label] += embs
			else:
				self.dataset[label] = embs

	def find_match(self, emb, threshold = 0.7):
		'''
		Given a single embedding, find the closest match
			* TO DO: implement a more sophisicated way to find best match *
		'''
		current_min = threshold # i know this is dirty :D
		best_subject = "Unknown"
		for subject in self.dataset:
			distances = [numpy.linalg.norm(emb - e) for e in self.dataset[subject]]
			min_distance = min(distances)
			if min_distance < current_min:
				best_subject = subject
		return best_subject

