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

from typing import List

import numpy as np
import pycocotools.mask as mask_util
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing_extensions import Annotated, TypeAlias

from .....utils import logging
from ...single_model_pipeline import InstanceSegmentation
from .. import utils as serving_utils
from ..app import AppConfig, create_app
from ..models import Response, ResultResponse


class InferRequest(BaseModel):
    image: str


BoundingBox: TypeAlias = Annotated[List[float], Field(min_length=4, max_length=4)]


class Mask(BaseModel):
    rleResult: str
    size: Annotated[List[int], Field(min_length=2, max_length=2)]


class Instance(BaseModel):
    bbox: BoundingBox
    categoryId: int
    score: float
    mask: Mask


class InferResult(BaseModel):
    instances: List[Instance]
    image: str


def _rle(mask: np.ndarray) -> str:
    rle_res = mask_util.encode(np.asarray(mask[..., None], order="F", dtype="uint8"))[0]
    return rle_res["counts"].decode("utf-8")


def create_pipeline_app(
    pipeline: InstanceSegmentation, app_config: AppConfig
) -> FastAPI:
    app, ctx = create_app(
        pipeline=pipeline,
        app_config=app_config,
        app_aiohttp_session=True,
    )

    @app.post(
        "/instance-segmentation",
        operation_id="infer",
        responses={422: {"model": Response}},
    )
    async def _infer(request: InferRequest) -> ResultResponse[InferResult]:
        pipeline = ctx.pipeline
        aiohttp_session = ctx.aiohttp_session

        try:
            file_bytes = await serving_utils.get_raw_bytes(
                request.image, aiohttp_session
            )
            image = serving_utils.image_bytes_to_array(file_bytes)

            result = (await pipeline.infer(image))[0]

            instances: List[Instance] = []
            for obj, mask in zip(result["boxes"], result["masks"]):
                rle_res = _rle(mask)
                mask = Mask(rleResult=rle_res, size=mask.shape)
                instances.append(
                    Instance(
                        bbox=obj["coordinate"],
                        categoryId=obj["cls_id"],
                        score=obj["score"],
                        mask=mask,
                    )
                )
            output_image_base64 = serving_utils.base64_encode(
                serving_utils.image_to_bytes(result.img)
            )

            return ResultResponse(
                logId=serving_utils.generate_log_id(),
                errorCode=0,
                errorMsg="Success",
                result=InferResult(instances=instances, image=output_image_base64),
            )

        except Exception as e:
            logging.exception(e)
            raise HTTPException(status_code=500, detail="Internal server error")

    return app
