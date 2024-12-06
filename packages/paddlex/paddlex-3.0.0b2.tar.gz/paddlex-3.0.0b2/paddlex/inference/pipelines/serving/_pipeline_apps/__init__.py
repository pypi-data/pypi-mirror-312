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

from typing import Any, Dict

from fastapi import FastAPI

from ...attribute_recognition import (
    PedestrianAttributeRecPipeline,
    VehicleAttributeRecPipeline,
)
from ...base import BasePipeline
from ...face_recognition import FaceRecPipeline
from ...formula_recognition import FormulaRecognitionPipeline
from ...layout_parsing import LayoutParsingPipeline
from ...ocr import OCRPipeline
from ...pp_shitu_v2 import ShiTuV2Pipeline
from ...ppchatocrv3 import PPChatOCRPipeline
from ...seal_recognition import SealOCRPipeline
from ...single_model_pipeline import (
    AnomalyDetection,
    ImageClassification,
    InstanceSegmentation,
    MultiLableImageClas,
    ObjectDetection,
    SemanticSegmentation,
    SmallObjDet,
    TSAd,
    TSCls,
    TSFc,
)
from ...table_recognition import TableRecPipeline
from ..app import create_app_config
from .anomaly_detection import create_pipeline_app as create_anomaly_detection_app
from .face_recognition import create_pipeline_app as create_face_recognition_app
from .formula_recognition import create_pipeline_app as create_formula_recognition_app
from .layout_parsing import create_pipeline_app as create_layout_parsing_app
from .image_classification import create_pipeline_app as create_image_classification_app
from .instance_segmentation import (
    create_pipeline_app as create_instance_segmentation_app,
)
from .multi_label_image_classification import (
    create_pipeline_app as create_multi_label_image_classification_app,
)
from .object_detection import create_pipeline_app as create_object_detection_app
from .ocr import create_pipeline_app as create_ocr_app
from .pedestrian_attribute_recognition import (
    create_pipeline_app as create_pedestrian_attribute_recognition_app,
)
from .vehicle_attribute_recognition import (
    create_pipeline_app as create_vehicle_attribute_recognition_app,
)
from .pp_shitu_v2 import create_pipeline_app as create_pp_shitu_v2_app
from .ppchatocrv3 import create_pipeline_app as create_ppchatocrv3_app
from .seal_recognition import create_pipeline_app as create_seal_recognition_app
from .semantic_segmentation import (
    create_pipeline_app as create_semantic_segmentation_app,
)
from .small_object_detection import (
    create_pipeline_app as create_small_object_detection_app,
)
from .table_recognition import create_pipeline_app as create_table_recognition_app
from .ts_ad import create_pipeline_app as create_ts_ad_app
from .ts_cls import create_pipeline_app as create_ts_cls_app
from .ts_fc import create_pipeline_app as create_ts_fc_app


# XXX (Bobholamovic): This is tightly coupled to the name-pipeline mapping,
# which is dirty but necessary. I want to keep the pipeline definition code
# untouched while adding the pipeline serving feature. Each pipeline app depends
# on a specific pipeline class, and a pipeline name must be provided (in the
# pipeline config) to specify the type of the pipeline.
def create_pipeline_app(
    pipeline: BasePipeline, pipeline_config: Dict[str, Any]
) -> FastAPI:
    pipeline_name = pipeline_config["Global"]["pipeline_name"]
    app_config = create_app_config(pipeline_config)
    if pipeline_name == "image_classification":
        if not isinstance(pipeline, ImageClassification):
            raise TypeError(
                "Expected `pipeline` to be an instance of `ImageClassification`."
            )
        return create_image_classification_app(pipeline, app_config)
    elif pipeline_name == "instance_segmentation":
        if not isinstance(pipeline, InstanceSegmentation):
            raise TypeError(
                "Expected `pipeline` to be an instance of `InstanceSegmentation`."
            )
        return create_instance_segmentation_app(pipeline, app_config)
    elif pipeline_name == "object_detection":
        if not isinstance(pipeline, ObjectDetection):
            raise TypeError(
                "Expected `pipeline` to be an instance of `ObjectDetection`."
            )
        return create_object_detection_app(pipeline, app_config)
    elif pipeline_name == "OCR":
        if not isinstance(pipeline, OCRPipeline):
            raise TypeError("Expected `pipeline` to be an instance of `OCRPipeline`.")
        return create_ocr_app(pipeline, app_config)
    elif pipeline_name == "semantic_segmentation":
        if not isinstance(pipeline, SemanticSegmentation):
            raise TypeError(
                "Expected `pipeline` to be an instance of `SemanticSegmentation`."
            )
        return create_semantic_segmentation_app(pipeline, app_config)
    elif pipeline_name == "table_recognition":
        if not isinstance(pipeline, TableRecPipeline):
            raise TypeError(
                "Expected `pipeline` to be an instance of `TableRecPipeline`."
            )
        return create_table_recognition_app(pipeline, app_config)
    elif pipeline_name == "ts_ad":
        if not isinstance(pipeline, TSAd):
            raise TypeError("Expected `pipeline` to be an instance of `TSAd`.")
        return create_ts_ad_app(pipeline, app_config)
    elif pipeline_name == "ts_cls":
        if not isinstance(pipeline, TSCls):
            raise TypeError("Expected `pipeline` to be an instance of `TSCls`.")
        return create_ts_cls_app(pipeline, app_config)
    elif pipeline_name == "ts_fc":
        if not isinstance(pipeline, TSFc):
            raise TypeError("Expected `pipeline` to be an instance of `TSFc`.")
        return create_ts_fc_app(pipeline, app_config)
    elif pipeline_name == "multi_label_image_classification":
        if not isinstance(pipeline, MultiLableImageClas):
            raise TypeError(
                "Expected `pipeline` to be an instance of `MultiLableImageClas`."
            )
        return create_multi_label_image_classification_app(pipeline, app_config)
    elif pipeline_name == "small_object_detection":
        if not isinstance(pipeline, SmallObjDet):
            raise TypeError("Expected `pipeline` to be an instance of `SmallObjDet`.")
        return create_small_object_detection_app(pipeline, app_config)
    elif pipeline_name == "anomaly_detection":
        if not isinstance(pipeline, AnomalyDetection):
            raise TypeError(
                "Expected `pipeline` to be an instance of `AnomalyDetection`."
            )
        return create_anomaly_detection_app(pipeline, app_config)
    elif pipeline_name == "PP-ChatOCRv3-doc":
        if not isinstance(pipeline, PPChatOCRPipeline):
            raise TypeError(
                "Expected `pipeline` to be an instance of `PPChatOCRPipeline`."
            )
        return create_ppchatocrv3_app(pipeline, app_config)
    elif pipeline_name == "seal_recognition":
        if not isinstance(pipeline, SealOCRPipeline):
            raise TypeError(
                "Expected `pipeline` to be an instance of `SealOCRPipeline`."
            )
        return create_seal_recognition_app(pipeline, app_config)
    elif pipeline_name == "formula_recognition":
        if not isinstance(pipeline, FormulaRecognitionPipeline):
            raise TypeError(
                "Expected `pipeline` to be an instance of `FormulaRecognitionPipeline`."
            )
        return create_formula_recognition_app(pipeline, app_config)
    elif pipeline_name == "layout_parsing":
        if not isinstance(pipeline, LayoutParsingPipeline):
            raise TypeError(
                "Expected `pipeline` to be an instance of `LayoutParsingPipeline`."
            )
        return create_layout_parsing_app(pipeline, app_config)
    elif pipeline_name == "pedestrian_attribute_recognition":
        if not isinstance(pipeline, PedestrianAttributeRecPipeline):
            raise TypeError(
                "Expected `pipeline` to be an instance of `PedestrianAttributeRecPipeline`."
            )
        return create_pedestrian_attribute_recognition_app(pipeline, app_config)
    elif pipeline_name == "vehicle_attribute_recognition":
        if not isinstance(pipeline, VehicleAttributeRecPipeline):
            raise TypeError(
                "Expected `pipeline` to be an instance of `VehicleAttributeRecPipeline`."
            )
        return create_vehicle_attribute_recognition_app(pipeline, app_config)
    elif pipeline_name == "PP-ShiTuV2":
        if not isinstance(pipeline, ShiTuV2Pipeline):
            raise TypeError(
                "Expected `pipeline` to be an instance of `ShiTuV2Pipeline`."
            )
        return create_pp_shitu_v2_app(pipeline, app_config)
    elif pipeline_name == "face_recognition":
        if not isinstance(pipeline, FaceRecPipeline):
            raise TypeError(
                "Expected `pipeline` to be an instance of `FaceRecPipeline`."
            )
        return create_face_recognition_app(pipeline, app_config)
    else:
        if BasePipeline.get(pipeline_name):
            raise ValueError(
                f"The {pipeline_name} pipeline does not support pipeline serving."
            )
        else:
            raise ValueError("Unknown pipeline name")
