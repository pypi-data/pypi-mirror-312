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


import os
import os.path as osp

import re
import numpy as np
from PIL import Image
import cv2
import math
import json
import tempfile
from tokenizers import Tokenizer as TokenizerFast

from ....utils import logging
from ..base import BaseComponent

__all__ = [
    "OCRReisizeNormImg",
    "LaTeXOCRReisizeNormImg",
    "CTCLabelDecode",
    "LaTeXOCRDecode",
]


class OCRReisizeNormImg(BaseComponent):
    """for ocr image resize and normalization"""

    INPUT_KEYS = ["img", "img_size"]
    OUTPUT_KEYS = ["img"]
    DEAULT_INPUTS = {"img": "img", "img_size": "img_size"}
    DEAULT_OUTPUTS = {"img": "img"}

    def __init__(self, rec_image_shape=[3, 48, 320]):
        super().__init__()
        self.rec_image_shape = rec_image_shape

    def resize_norm_img(self, img, max_wh_ratio):
        """resize and normalize the img"""
        imgC, imgH, imgW = self.rec_image_shape
        assert imgC == img.shape[2]
        imgW = int((imgH * max_wh_ratio))

        h, w = img.shape[:2]
        ratio = w / float(h)
        if math.ceil(imgH * ratio) > imgW:
            resized_w = imgW
        else:
            resized_w = int(math.ceil(imgH * ratio))
        resized_image = cv2.resize(img, (resized_w, imgH))
        resized_image = resized_image.astype("float32")
        resized_image = resized_image.transpose((2, 0, 1)) / 255
        resized_image -= 0.5
        resized_image /= 0.5
        padding_im = np.zeros((imgC, imgH, imgW), dtype=np.float32)
        padding_im[:, :, 0:resized_w] = resized_image
        return padding_im

    def apply(self, img, img_size):
        """apply"""
        imgC, imgH, imgW = self.rec_image_shape
        max_wh_ratio = imgW / imgH
        w, h = img_size[:2]
        wh_ratio = w * 1.0 / h
        max_wh_ratio = max(max_wh_ratio, wh_ratio)
        img = self.resize_norm_img(img, max_wh_ratio)
        return {"img": img}


class LaTeXOCRReisizeNormImg(BaseComponent):
    """for ocr image resize and normalization"""

    INPUT_KEYS = "img"
    OUTPUT_KEYS = "img"
    DEAULT_INPUTS = {"img": "img"}
    DEAULT_OUTPUTS = {"img": "img"}

    def __init__(self, rec_image_shape=[3, 48, 320]):
        super().__init__()
        self.rec_image_shape = rec_image_shape

    def pad_(self, img, divable=32):
        threshold = 128
        data = np.array(img.convert("LA"))
        if data[..., -1].var() == 0:
            data = (data[..., 0]).astype(np.uint8)
        else:
            data = (255 - data[..., -1]).astype(np.uint8)
        data = (data - data.min()) / (data.max() - data.min()) * 255
        if data.mean() > threshold:
            # To invert the text to white
            gray = 255 * (data < threshold).astype(np.uint8)
        else:
            gray = 255 * (data > threshold).astype(np.uint8)
            data = 255 - data

        coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
        a, b, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
        rect = data[b : b + h, a : a + w]
        im = Image.fromarray(rect).convert("L")
        dims = []
        for x in [w, h]:
            div, mod = divmod(x, divable)
            dims.append(divable * (div + (1 if mod > 0 else 0)))
        padded = Image.new("L", dims, 255)
        padded.paste(im, (0, 0, im.size[0], im.size[1]))
        return padded

    def minmax_size_(
        self,
        img,
        max_dimensions,
        min_dimensions,
    ):
        if max_dimensions is not None:
            ratios = [a / b for a, b in zip(img.size, max_dimensions)]
            if any([r > 1 for r in ratios]):
                size = np.array(img.size) // max(ratios)
                img = img.resize(tuple(size.astype(int)), Image.BILINEAR)
        if min_dimensions is not None:
            # hypothesis: there is a dim in img smaller than min_dimensions, and return a proper dim >= min_dimensions
            padded_size = [
                max(img_dim, min_dim)
                for img_dim, min_dim in zip(img.size, min_dimensions)
            ]
            if padded_size != list(img.size):  # assert hypothesis
                padded_im = Image.new("L", padded_size, 255)
                padded_im.paste(img, img.getbbox())
                img = padded_im
        return img

    def norm_img_latexocr(self, img):
        # CAN only predict gray scale image
        shape = (1, 1, 3)
        mean = [0.7931, 0.7931, 0.7931]
        std = [0.1738, 0.1738, 0.1738]
        scale = np.float32(1.0 / 255.0)
        min_dimensions = [32, 32]
        max_dimensions = [672, 192]
        mean = np.array(mean).reshape(shape).astype("float32")
        std = np.array(std).reshape(shape).astype("float32")

        im_h, im_w = img.shape[:2]
        if (
            min_dimensions[0] <= im_w <= max_dimensions[0]
            and min_dimensions[1] <= im_h <= max_dimensions[1]
        ):
            pass
        else:
            img = Image.fromarray(np.uint8(img))
            img = self.minmax_size_(self.pad_(img), max_dimensions, min_dimensions)
            img = np.array(img)
            im_h, im_w = img.shape[:2]
            img = np.dstack([img, img, img])
        img = (img.astype("float32") * scale - mean) / std
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        divide_h = math.ceil(im_h / 16) * 16
        divide_w = math.ceil(im_w / 16) * 16
        img = np.pad(
            img, ((0, divide_h - im_h), (0, divide_w - im_w)), constant_values=(1, 1)
        )
        img = img[:, :, np.newaxis].transpose(2, 0, 1)
        img = img.astype("float32")
        return img

    def apply(self, img):
        """apply"""
        img = self.norm_img_latexocr(img)
        return {"img": img}


class BaseRecLabelDecode(BaseComponent):
    """Convert between text-label and text-index"""

    INPUT_KEYS = ["pred"]
    OUTPUT_KEYS = ["rec_text", "rec_score"]
    DEAULT_INPUTS = {"pred": "pred"}
    DEAULT_OUTPUTS = {"rec_text": "rec_text", "rec_score": "rec_score"}

    ENABLE_BATCH = True

    def __init__(self, character_str=None, use_space_char=True):
        super().__init__()
        self.reverse = False
        character_list = (
            list(character_str)
            if character_str is not None
            else list("0123456789abcdefghijklmnopqrstuvwxyz")
        )
        if use_space_char:
            character_list.append(" ")

        character_list = self.add_special_char(character_list)
        self.dict = {}
        for i, char in enumerate(character_list):
            self.dict[char] = i
        self.character = character_list

    def pred_reverse(self, pred):
        """pred_reverse"""
        pred_re = []
        c_current = ""
        for c in pred:
            if not bool(re.search("[a-zA-Z0-9 :*./%+-]", c)):
                if c_current != "":
                    pred_re.append(c_current)
                pred_re.append(c)
                c_current = ""
            else:
                c_current += c
        if c_current != "":
            pred_re.append(c_current)

        return "".join(pred_re[::-1])

    def add_special_char(self, character_list):
        """add_special_char"""
        return character_list

    def decode(self, text_index, text_prob=None, is_remove_duplicate=False):
        """convert text-index into text-label."""
        result_list = []
        ignored_tokens = self.get_ignored_tokens()
        batch_size = len(text_index)
        for batch_idx in range(batch_size):
            selection = np.ones(len(text_index[batch_idx]), dtype=bool)
            if is_remove_duplicate:
                selection[1:] = text_index[batch_idx][1:] != text_index[batch_idx][:-1]
            for ignored_token in ignored_tokens:
                selection &= text_index[batch_idx] != ignored_token

            char_list = [
                self.character[text_id] for text_id in text_index[batch_idx][selection]
            ]
            if text_prob is not None:
                conf_list = text_prob[batch_idx][selection]
            else:
                conf_list = [1] * len(selection)
            if len(conf_list) == 0:
                conf_list = [0]

            text = "".join(char_list)

            if self.reverse:  # for arabic rec
                text = self.pred_reverse(text)

            result_list.append((text, np.mean(conf_list).tolist()))
        return result_list

    def get_ignored_tokens(self):
        """get_ignored_tokens"""
        return [0]  # for ctc blank

    def apply(self, pred):
        """apply"""
        preds = np.array(pred)
        if isinstance(preds, tuple) or isinstance(preds, list):
            preds = preds[-1]
        preds_idx = preds.argmax(axis=2)
        preds_prob = preds.max(axis=2)
        text = self.decode(preds_idx, preds_prob, is_remove_duplicate=True)
        return [{"rec_text": t[0], "rec_score": t[1]} for t in text]


class CTCLabelDecode(BaseRecLabelDecode):
    """Convert between text-label and text-index"""

    def __init__(self, character_list=None, use_space_char=True):
        super().__init__(character_list, use_space_char=use_space_char)

    def apply(self, pred):
        """apply"""
        preds = np.array(pred[0])
        preds_idx = preds.argmax(axis=2)
        preds_prob = preds.max(axis=2)
        text = self.decode(preds_idx, preds_prob, is_remove_duplicate=True)
        return [{"rec_text": t[0], "rec_score": t[1]} for t in text]

    def add_special_char(self, character_list):
        """add_special_char"""
        character_list = ["blank"] + character_list
        return character_list


class LaTeXOCRDecode(BaseComponent):
    """Convert between latex-symbol and symbol-index"""

    INPUT_KEYS = ["pred"]
    OUTPUT_KEYS = ["rec_text"]
    DEAULT_INPUTS = {"pred": "pred"}
    DEAULT_OUTPUTS = {"rec_text": "rec_text"}

    def __init__(self, character_list=None):
        super().__init__()
        character_list = character_list
        temp_path = tempfile.gettempdir()
        rec_char_dict_path = os.path.join(temp_path, "latexocr_tokenizer.json")
        try:
            with open(rec_char_dict_path, "w") as f:
                json.dump(character_list, f)
        except Exception as e:
            print(f"创建 latexocr_tokenizer.json 文件失败, 原因{str(e)}")
        self.tokenizer = TokenizerFast.from_file(rec_char_dict_path)

    def post_process(self, s):
        text_reg = r"(\\(operatorname|mathrm|text|mathbf)\s?\*? {.*?})"
        letter = "[a-zA-Z]"
        noletter = "[\W_^\d]"
        names = [x[0].replace(" ", "") for x in re.findall(text_reg, s)]
        s = re.sub(text_reg, lambda match: str(names.pop(0)), s)
        news = s
        while True:
            s = news
            news = re.sub(r"(?!\\ )(%s)\s+?(%s)" % (noletter, noletter), r"\1\2", s)
            news = re.sub(r"(?!\\ )(%s)\s+?(%s)" % (noletter, letter), r"\1\2", news)
            news = re.sub(r"(%s)\s+?(%s)" % (letter, noletter), r"\1\2", news)
            if news == s:
                break
        return s

    def decode(self, tokens):
        if len(tokens.shape) == 1:
            tokens = tokens[None, :]

        dec = [self.tokenizer.decode(tok) for tok in tokens]
        dec_str_list = [
            "".join(detok.split(" "))
            .replace("Ġ", " ")
            .replace("[EOS]", "")
            .replace("[BOS]", "")
            .replace("[PAD]", "")
            .strip()
            for detok in dec
        ]
        return [str(self.post_process(dec_str)) for dec_str in dec_str_list]

    def apply(self, pred):
        preds = np.array(pred[0])
        text = self.decode(preds)
        return {"rec_text": text[0]}
