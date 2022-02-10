from asyncio.windows_events import NULL
from copy import deepcopy
from typing import Type
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from cv2 import cv2
from numpy.lib.type_check import imag
from keras import backend as K

from services.libs.util import ImageChunker
from services.libs.pconv_model import PConvUnet


class InpaintModel():
    def __init__(self, config):
        self.config = config
        
    def process_inpaint(self, img):
        im, mask = self.preprocess_data(img.copy())
        print(type(im))
        return self.inpaint_img(im, mask)

    def preprocess_data(self, img):
        print("preprocess_data")
        im = img.copy() / 255
        buffer = img.copy() / 255
        im[:, :, 2] = im[:, :, 0]
        im[:, :, 0] = buffer[:, :, 2]

        mask = Image.open(self.config.path_to_masc).resize((512, 512)).convert('RGB')
        mask = np.array(mask)
        print(mask)
        mask[mask!=0] = 2
        mask[mask==0] = 1
        mask[mask==2] = 0
        im[mask==0] = 1

        imgs, masks = [], []

        imgs.append(np.asarray(im))
        masks.append(np.asarray(mask))

        print(np.asarray(im).shape)
        return np.asarray(im).copy(), mask

    def inpaint_img(self, img, mask):

        model = PConvUnet(vgg_weights=None, inference_only=True)
        model.load(self.config.path_to_inpaint_weights, train_bn=False)

        chunker = ImageChunker(512, 512, 30)

        # Process sample
        chunked_images = chunker.dimension_preprocess(deepcopy(img))
        chunked_masks = chunker.dimension_preprocess(deepcopy(mask))
        pred_imgs = model.predict([chunked_images, chunked_masks])
        cv2.imwrite(self.config.path_to_inpaintprediction, cv2.cvtColor(pred_imgs[0] * 255 , cv2.COLOR_BGR2RGB))
        K.clear_session()
        return cv2.cvtColor(pred_imgs[0] * 255 , cv2.COLOR_BGR2RGB)