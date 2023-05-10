# import cv2
# from insightface.app import FaceAnalysis
# from insightface.data import get_image as ins_get_image
#
# app = FaceAnalysis(allowed_modules=['detection'], providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
# app.prepare(ctx_id=0, det_size=(640, 640))
# img = ins_get_image('t1')
# faces = app.get(img)
# rimg = app.draw_on(img, faces)
# cv2.imwrite("./t1_output.jpg", rimg)
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)