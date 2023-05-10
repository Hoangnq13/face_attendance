import torch
import numpy as np
import cv2
from torchvision import datasets, transforms
import os
import shutil
from tqdm import tqdm
import pickle
from PIL import Image

from config import DATA_DIR, DATA_ALIGN_DIR
from Model import Model
from DB.SQLite import SQLite
from utils import day_now, time_now
from FaceAlignment import FaceAlignment


def get_faces_align():
    if os.path.exists(DATA_ALIGN_DIR):
        shutil.rmtree(DATA_ALIGN_DIR)

    for name_person in tqdm(os.listdir(DATA_DIR)):
        if not os.path.exists(os.path.join(DATA_ALIGN_DIR, name_person)):
            os.makedirs(os.path.join(DATA_ALIGN_DIR, name_person))

        for path in os.listdir(os.path.join(DATA_DIR, name_person)):
            image_path = os.path.join(DATA_DIR, name_person, path)
            image_align = FaceAlignment.alignment(Image.open(image_path))[0]
            image_align = Image.fromarray(image_align)
            image_align_path = os.path.join(DATA_ALIGN_DIR, name_person, path)
            image_align.save(image_align_path)


def main():
    model_recognize = Model.load_pretrained_model()
    # Data augmentation and normalization for training
    # Just normalization for validation
    data_transforms = transforms.Compose([
        transforms.Resize(112),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])

    image_datasets = datasets.ImageFolder(DATA_ALIGN_DIR, data_transforms)
    dataloaders = torch.utils.data.DataLoader(image_datasets, batch_size=16,
                                              shuffle=False, num_workers=8)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    features = torch.tensor([])
    labels = torch.tensor([])
    with torch.no_grad():
        for inputs, label in dataloaders:
            feature, _ = model_recognize(inputs.to(device))
            labels = torch.cat([labels, label], 0)
            features = torch.cat([features, feature], 0)

    names_str = ""
    names = []
    for name in sorted(os.listdir(DATA_DIR)):
        names.append(name)
        names_str += f"{name}*"
    names_str = names_str[:-1]

    day = day_now()
    time = time_now()

    connectDb = SQLite("DB/Database.db")
    connectDb.createTable("DATA", "(Name TEXT, Day TEXT, Time TEXT)")
    check_bot = connectDb.getData("DATA", ["Name"], {"Name": names_str})
    if check_bot:
        connectDb.updateData("DATA", {"Day": day, "Time": time}, {"Name": names_str})
    else:
        connectDb.insertData("DATA", {"Name": names_str, "Day": day, "Time": time})

    labels = labels.type(torch.int)

    with open("data.pkl", "wb") as data:
        pickle.dump([features, labels, names], data)


if __name__ == "__main__":
    Model = Model()
    FaceAlignment = FaceAlignment()
    get_faces_align()
    main()
