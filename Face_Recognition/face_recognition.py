import numpy as np
import torch
import pickle
import time
from PIL import Image, ImageDraw, ImageFont
from torchvision import transforms

from DB.SQLite import SQLite
from FaceAlignment import FaceAlignment
from Model import Model
from config import THRESHOLD
from utils import day_now, time_now


class FaceRecognition(FaceAlignment, Model, SQLite):
    def __init__(self):
        super(FaceRecognition, self).__init__()
        self.model_recognize = self.load_pretrained_model()#load prertain model
        with open("data.pkl", "rb") as f: #đọc tệp dữ liệu và lưu vào features, labels, names
            data = pickle.load(f)
        self.features = data[0]
        self.labels = data[1]
        self.names = data[2]

    def extract_face(self, image):
        bbox = self.get_bbox(image)#nhận ảnh
        draw = ImageDraw.Draw(image)
        for box in bbox:
            draw.rectangle([(box[0], box[1]), (box[2], box[3])], outline='green', width=3) #vẽ box trên mặt
        del draw
        return image

    @staticmethod
    def to_input(pil_rgb_image):

        data_transforms = transforms.Compose([
            transforms.Resize(112), #chuẩn hóa ảnh
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]) #chuẩn hóa giá trị ảnh
        ])
        tensor = data_transforms(pil_rgb_image)
        tensor = torch.unsqueeze(tensor, 0)
        return tensor
#phát hiện khuôn mặt trong ảnh và đặc trưng
    def detect(self, image):
        faces = self.prepareFaces(image)
        boxes = []
        faces_crop = []
        for i in range(len(faces)):
            boxes.append(faces[i].bbox)
            align = self.norm_crop(np.array(image), faces[i].kps)
            align = Image.fromarray(align).resize((112, 112))
            faces_crop.append(align)
        return image, faces_crop, boxes

    def recognition(self, image_input):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        start = time.time()

        image, faces_crop, boxes = self.detect(image_input)

        print(f"Time detection: {time.time() - start}")

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font='arial.ttf', size=np.floor(1.5e-2 * image_input.size[1] + 0.5).astype('int32'))
        for box in boxes:
            draw.rectangle([(box[0], box[1]), (box[2], box[3])], outline='green', width=3)

        for i in range(len(faces_crop)):
            inputs = self.to_input(faces_crop[i])
            feature, _ = self.model_recognize(inputs.to(device))
            score = (feature @ self.features.T).detach()

            if torch.max(score) > THRESHOLD:
                index = torch.argmax(score)
                id = self.labels[index]
                text = self.names[id]
            else:
                text = 'Unknow'

            text_width, text_height = draw.textsize(text, font=font)
            draw.text((boxes[i][0] + 5, boxes[i][3] - text_height - 5), text, fill="yellow", font=font)

        del draw
        print(f"Time Recognition {time.time() - start}")
        return image

    def webcam(self, image_input):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        image, faces_crop, boxes = self.detect(image_input)

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font='font/arial.ttf',
                                  size=np.floor(4e-2 * image_input.size[1] + 0.5).astype('int32'))

        connectDb = SQLite("DB/Database.db")
        connectDb.createTable("Attendance", "(Name TEXT, Day TEXT, Time TEXT)")

        for box in boxes:
            draw.rectangle([(box[0], box[1]), (box[2], box[3])], outline='green', width=3)

        for i in range(len(faces_crop)):
            inputs = self.to_input(faces_crop[i])
            feature, _ = self.model_recognize(inputs.to(device))
            score = (feature @ self.features.T).detach()

            if torch.max(score) > THRESHOLD:
                index = torch.argmax(score)
                id = self.labels[index]
                text = self.names[id]
                day = day_now()
                time_vn = time_now()
                connectDb.insertData("Attendance", {"Name": text, "Day": day, "Time": time_vn})
            else:
                text = 'Unknow'

            text_width, text_height = draw.textsize(text, font=font)
            draw.text((boxes[i][0] + 5, boxes[i][3] - text_height - 5), text, fill="yellow", font=font)

        del draw
        return image
