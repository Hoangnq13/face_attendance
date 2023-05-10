from insightface.app import FaceAnalysis
import numpy as np
from PIL import ImageDraw

#tải mô hình huấn luyện sẵn SCRFD
class FaceDetection:
    def __init__(self):
        super(FaceDetection, self).__init__()
        # load model Face Detection (SCRFD - Lib: Insightface)
        app = FaceAnalysis(allowed_modules=['detection'], providers=['CPUExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(640, 640))
        self.app = app
#trích xuất khuôn mặt
    def prepareFaces(self, image):
        faces = self.app.get(np.array(image))
        return faces
#lấy tọa độ mặt
    def get_bbox(self, image) -> list:
        faces = self.prepareFaces(image)
        bbox = []
        for i in range(len(faces)):
            bbox.append(faces[i].bbox)
        return bbox
#cắt khuôn mặt
    def detection(self, image) -> list:
        bbox = self.get_bbox(image)
        faces_crop = []
        for box in bbox:
            face = image.crop(box)
            faces_crop.append(face)
        return faces_crop
# Vẽ khuôn
    def detection2(self, image):
        draw = ImageDraw.Draw(image)
        bbox = self.get_bbox(image)
        for box in bbox:
            draw.rectangle([(box[0], box[1]), (box[2], box[3])], outline='green', width=3)
        del draw
        return image