# copyright (c) 2024 PaddlePaddle Authors. All Rights Reserve.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
import random
import numpy as np
import cv2
import PIL
from PIL import Image, ImageDraw, ImageFont

from ...utils.fonts import PINGFANG_FONT_FILE_PATH
from .base import CVResult


class OCRResult(CVResult):

    def get_minarea_rect(self, points):
        bounding_box = cv2.minAreaRect(points)
        points = sorted(list(cv2.boxPoints(bounding_box)), key=lambda x: x[0])

        index_a, index_b, index_c, index_d = 0, 1, 2, 3
        if points[1][1] > points[0][1]:
            index_a = 0
            index_d = 1
        else:
            index_a = 1
            index_d = 0
        if points[3][1] > points[2][1]:
            index_b = 2
            index_c = 3
        else:
            index_b = 3
            index_c = 2

        box = np.array(
            [points[index_a], points[index_b], points[index_c], points[index_d]]
        ).astype(np.int32)

        return box

    def _to_img(
        self,
    ):
        """draw ocr result"""
        # TODO(gaotingquan): mv to postprocess
        drop_score = 0.5

        boxes = self["dt_polys"]
        txts = self["rec_text"]
        scores = self["rec_score"]
        image = self._img_reader.read(self["input_path"])
        h, w = image.height, image.width
        img_left = image.copy()
        img_right = np.ones((h, w, 3), dtype=np.uint8) * 255
        random.seed(0)
        draw_left = ImageDraw.Draw(img_left)
        if txts is None or len(txts) != len(boxes):
            txts = [None] * len(boxes)
        for idx, (box, txt) in enumerate(zip(boxes, txts)):
            try:
                if scores is not None and scores[idx] < drop_score:
                    continue
                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                )
                box = np.array(box)
                if len(box) > 4:
                    pts = [(x, y) for x, y in box.tolist()]
                    draw_left.polygon(pts, outline=color, width=8)
                    box = self.get_minarea_rect(box)
                    height = int(0.5 * (max(box[:, 1]) - min(box[:, 1])))
                    box[:2, 1] = np.mean(box[:, 1])
                    box[2:, 1] = np.mean(box[:, 1]) + min(20, height)
                draw_left.polygon(box, fill=color)
                img_right_text = draw_box_txt_fine(
                    (w, h), box, txt, PINGFANG_FONT_FILE_PATH
                )
                pts = np.array(box, np.int32).reshape((-1, 1, 2))
                cv2.polylines(img_right_text, [pts], True, color, 1)
                img_right = cv2.bitwise_and(img_right, img_right_text)
            except:
                continue

        img_left = Image.blend(image, img_left, 0.5)
        img_show = Image.new("RGB", (w * 2, h), (255, 255, 255))
        img_show.paste(img_left, (0, 0, w, h))
        img_show.paste(Image.fromarray(img_right), (w, 0, w * 2, h))
        return img_show


def draw_box_txt_fine(img_size, box, txt, font_path):
    """draw box text"""
    box_height = int(
        math.sqrt((box[0][0] - box[3][0]) ** 2 + (box[0][1] - box[3][1]) ** 2)
    )
    box_width = int(
        math.sqrt((box[0][0] - box[1][0]) ** 2 + (box[0][1] - box[1][1]) ** 2)
    )

    if box_height > 2 * box_width and box_height > 30:
        img_text = Image.new("RGB", (box_height, box_width), (255, 255, 255))
        draw_text = ImageDraw.Draw(img_text)
        if txt:
            font = create_font(txt, (box_height, box_width), font_path)
            draw_text.text([0, 0], txt, fill=(0, 0, 0), font=font)
        img_text = img_text.transpose(Image.ROTATE_270)
    else:
        img_text = Image.new("RGB", (box_width, box_height), (255, 255, 255))
        draw_text = ImageDraw.Draw(img_text)
        if txt:
            font = create_font(txt, (box_width, box_height), font_path)
            draw_text.text([0, 0], txt, fill=(0, 0, 0), font=font)

    pts1 = np.float32(
        [[0, 0], [box_width, 0], [box_width, box_height], [0, box_height]]
    )
    pts2 = np.array(box, dtype=np.float32)
    M = cv2.getPerspectiveTransform(pts1, pts2)

    img_text = np.array(img_text, dtype=np.uint8)
    img_right_text = cv2.warpPerspective(
        img_text,
        M,
        img_size,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255),
    )
    return img_right_text


def create_font(txt, sz, font_path):
    """create font"""
    font_size = int(sz[1] * 0.8)
    font = ImageFont.truetype(font_path, font_size, encoding="utf-8")
    if int(PIL.__version__.split(".")[0]) < 10:
        length = font.getsize(txt)[0]
    else:
        length = font.getlength(txt)

    if length > sz[0]:
        font_size = int(font_size * sz[0] / length)
        font = ImageFont.truetype(font_path, font_size, encoding="utf-8")
    return font
