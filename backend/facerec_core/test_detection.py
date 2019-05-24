from facerec_core.mtcnn_detect import MTCNNDetect
import cv2
from facerec_core.tf_graph import FaceRecGraph
MTCNNGraph = FaceRecGraph();
face_detect = MTCNNDetect(MTCNNGraph, scale_factor=2); #scale_factor, rescales image for faster detection

img = cv2.imread("./facerec_core/testimage.jpg")

print(img)
print(face_detect.detect_face(img)[0])
