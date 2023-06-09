import numpy as np
import cv2
from PIL import Image
from skimage import transform as trans

from FaceDetection import FaceDetection


class FaceAlignment(FaceDetection):
    #chuyển đổi khuôn mặt về kích thước chuẩn
    def __init__(self):
        # super(FaceAnalysis, self).__init__()
        super().__init__()
        self.arcface_dst = np.array(
            [[38.2946, 51.6963], [73.5318, 51.5014], [56.0252, 71.7366], [41.5493, 92.3655], [70.7299, 92.2041]],
            dtype=np.float32)
#được sử dụng để tính toán ma trận biến đổi để chuẩn hóa các khuôn mặt đã cắt về một kích thước chuẩn
    def estimate_norm(self, lmk, image_size=112):
        assert lmk.shape == (5, 2)

        ratio = float(image_size) / 112.0
        diff_x = 0

        dst = self.arcface_dst * ratio
        dst[:, 0] += diff_x
        tform = trans.SimilarityTransform()
        tform.estimate(lmk, dst)
        M = tform.params[0:2, :]
        return M
#Phương thức norm_crop trả về hình ảnh sau khi được chuẩn hóa và cắt kích thước về image_size
    def norm_crop(self, img, landmark, image_size=112):
        M = self.estimate_norm(landmark, image_size)
        warped = cv2.warpAffine(img, M, (image_size, image_size), borderValue=0.0)
        return warped
#canh chỉnh khuôn mặt trên ảnh input
    def alignment(self, image):
        faces = self.prepareFaces(image)
        faces_align = []
        for i in range(len(faces)):
            # align = self.norm_crop(cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB), faces[i].kps)
            align = self.norm_crop(np.array(image), faces[i].kps)
            align = Image.fromarray(align).resize((112, 112))
            align = np.array(align)
            faces_align.append(align)
        return faces_align
