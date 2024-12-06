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


import PIL
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

from ...utils.fonts import PINGFANG_FONT_FILE_PATH
from ..utils.color_map import get_colormap
from .base import CVResult


class TopkResult(CVResult):

    def _to_img(self):
        """Draw label on image"""
        labels = self.get("label_names", self["class_ids"])
        label_str = f"{labels[0]} {self['scores'][0]:.2f}"

        image = self._img_reader.read(self["input_path"])
        image_size = image.size
        draw = ImageDraw.Draw(image)
        min_font_size = int(image_size[0] * 0.02)
        max_font_size = int(image_size[0] * 0.05)
        for font_size in range(max_font_size, min_font_size - 1, -1):
            font = ImageFont.truetype(
                PINGFANG_FONT_FILE_PATH, font_size, encoding="utf-8"
            )
            if tuple(map(int, PIL.__version__.split("."))) <= (10, 0, 0):
                text_width_tmp, text_height_tmp = draw.textsize(label_str, font)
            else:
                left, top, right, bottom = draw.textbbox((0, 0), label_str, font)
                text_width_tmp, text_height_tmp = right - left, bottom - top
            if text_width_tmp <= image_size[0]:
                break
            else:
                font = ImageFont.truetype(PINGFANG_FONT_FILE_PATH, min_font_size)
        color_list = get_colormap(rgb=True)
        color = tuple(color_list[0])
        font_color = tuple(self._get_font_colormap(3))
        if tuple(map(int, PIL.__version__.split("."))) <= (10, 0, 0):
            text_width, text_height = draw.textsize(label_str, font)
        else:
            left, top, right, bottom = draw.textbbox((0, 0), label_str, font)
            text_width, text_height = right - left, bottom - top

        rect_left = 3
        rect_top = 3
        rect_right = rect_left + text_width + 3
        rect_bottom = rect_top + text_height + 6

        draw.rectangle([(rect_left, rect_top), (rect_right, rect_bottom)], fill=color)

        text_x = rect_left + 3
        text_y = rect_top
        draw.text((text_x, text_y), label_str, fill=font_color, font=font)
        return image

    def _get_font_colormap(self, color_index):
        """
        Get font colormap
        """
        dark = np.array([0x14, 0x0E, 0x35])
        light = np.array([0xFF, 0xFF, 0xFF])
        light_indexs = [0, 3, 4, 8, 9, 13, 14, 18, 19]
        if color_index in light_indexs:
            return light.astype("int32")
        else:
            return dark.astype("int32")


class MLClassResult(TopkResult):
    def _to_img(self):
        """Draw label on image"""
        image = self._img_reader.read(self["input_path"])
        label_names = self["label_names"]
        scores = self["scores"]
        image = image.convert("RGB")
        image_width, image_height = image.size
        font_size = int(image_width * 0.06)

        font = ImageFont.truetype(PINGFANG_FONT_FILE_PATH, font_size)
        text_lines = []
        row_width = 0
        row_height = 0
        row_text = "\t"
        for label_name, score in zip(label_names, scores):
            text = f"{label_name}({score})\t"
            if int(PIL.__version__.split(".")[0]) < 10:
                text_width, row_height = font.getsize(text)
            else:
                text_width, row_height = font.getbbox(text)[2:]
            if row_width + text_width <= image_width:
                row_text += text
                row_width += text_width
            else:
                text_lines.append(row_text)
                row_text = "\t" + text
                row_width = text_width
        text_lines.append(row_text)
        color_list = get_colormap(rgb=True)
        color = tuple(color_list[0])
        new_image_height = image_height + len(text_lines) * int(row_height * 1.2)
        new_image = Image.new("RGB", (image_width, new_image_height), color)
        new_image.paste(image, (0, 0))

        draw = ImageDraw.Draw(new_image)
        font_color = tuple(self._get_font_colormap(3))
        for i, text in enumerate(text_lines):
            if int(PIL.__version__.split(".")[0]) < 10:
                text_width, _ = font.getsize(text)
            else:
                text_width, _ = font.getbbox(text)[2:]
            draw.text(
                (0, image_height + i * int(row_height * 1.2)),
                text,
                fill=font_color,
                font=font,
            )
        return new_image
