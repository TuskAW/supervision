from contextlib import ExitStack as DoesNotRaise
from typing import List, Tuple

import pytest

from supervision.dataset.formats.coco import classes_to_coco_categories, coco_categories_to_classes, \
    group_coco_annotations_by_image_id


def generate_cock_coco_annotation(
    annotation_id: int = 0,
    image_id: int = 0,
    category_id: int = 0,
    bbox: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0),
    area: float = 0.0
) -> dict:
    return {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_id,
        "bbox": list(bbox),
        "area": area,
        "iscrowd": 0
    }


@pytest.mark.parametrize(
    "coco_categories, expected_result, exception",
    [
        (
            [],
            [],
            DoesNotRaise()
        ),  # empty coco categories
        (
            [
                {
                    "id": 0,
                    "name": "fashion-assistant",
                    "supercategory": "none"
                }
            ],
            [],
            DoesNotRaise()
        ),  # single coco category with supercategory == "none"
        (
            [
                {
                    "id": 0,
                    "name": "fashion-assistant",
                    "supercategory": "none"
                },
                {
                    "id": 1,
                    "name": "baseball cap",
                    "supercategory": "fashion-assistant"
                }
            ],
            [
                "baseball cap"
            ],
            DoesNotRaise()
        ),  # two coco categories; one with supercategory == "none" and one with supercategory != "none"
        (
            [
                {
                    "id": 0,
                    "name": "fashion-assistant",
                    "supercategory": "none"
                },
                {
                    "id": 1,
                    "name": "baseball cap",
                    "supercategory": "fashion-assistant"
                },
                {
                    "id": 2,
                    "name": "hoodie",
                    "supercategory": "fashion-assistant"
                }
            ],
            [
                "baseball cap",
                "hoodie"
            ],
            DoesNotRaise()
        ),  # three coco categories; one with supercategory == "none" and two with supercategory != "none"
        (
            [
                {
                    "id": 0,
                    "name": "fashion-assistant",
                    "supercategory": "none"
                },
                {
                    "id": 2,
                    "name": "hoodie",
                    "supercategory": "fashion-assistant"
                },
                {
                    "id": 1,
                    "name": "baseball cap",
                    "supercategory": "fashion-assistant"
                }
            ],
            [
                "baseball cap",
                "hoodie"
            ],
            DoesNotRaise()
        ),  # three coco categories; one with supercategory == "none" and two with supercategory != "none" (different order)
    ]
)
def test_coco_categories_to_classes(
    coco_categories: List[dict],
    expected_result: List[str],
    exception: Exception
) -> None:
    with exception:
        result = coco_categories_to_classes(coco_categories=coco_categories)
        assert result == expected_result


@pytest.mark.parametrize(
    "classes, exception",
    [
        (
            [],
            DoesNotRaise()
        ),  # empty classes
        (
            [
                "baseball cap"
            ],
            DoesNotRaise()
        ),  # single class
        (
            [
                "baseball cap",
                "hoodie"
            ],
            DoesNotRaise()
        ),  # two classes
    ]
)
def test_classes_to_coco_categories_and_back_to_classes(classes: List[str], exception: Exception) -> None:
    with exception:
        coco_categories = classes_to_coco_categories(classes=classes)
        result = coco_categories_to_classes(coco_categories=coco_categories)
        assert result == classes


@pytest.mark.parametrize(
    "coco_annotations, expected_result, exception",
    [
        (
            [],
            {},
            DoesNotRaise()
        ),  # empty coco annotations
        (
            [
                generate_cock_coco_annotation(annotation_id=0, image_id=0, category_id=0)
            ],
            {
                0: [
                    generate_cock_coco_annotation(annotation_id=0, image_id=0, category_id=0)
                ]
            },
            DoesNotRaise()
        ),  # single coco annotation
        (
            [
                generate_cock_coco_annotation(annotation_id=0, image_id=0, category_id=0),
                generate_cock_coco_annotation(annotation_id=1, image_id=1, category_id=0)
            ],
            {
                0: [
                    generate_cock_coco_annotation(annotation_id=0, image_id=0, category_id=0)
                ],
                1: [
                    generate_cock_coco_annotation(annotation_id=1, image_id=1, category_id=0)
                ]
            },
            DoesNotRaise()
        ),  # two coco annotations
        (
            [
                generate_cock_coco_annotation(annotation_id=0, image_id=0, category_id=0),
                generate_cock_coco_annotation(annotation_id=1, image_id=1, category_id=1),
                generate_cock_coco_annotation(annotation_id=2, image_id=1, category_id=2),
                generate_cock_coco_annotation(annotation_id=3, image_id=2, category_id=3),
                generate_cock_coco_annotation(annotation_id=4, image_id=3, category_id=1),
                generate_cock_coco_annotation(annotation_id=5, image_id=3, category_id=2),
                generate_cock_coco_annotation(annotation_id=5, image_id=3, category_id=3),
            ],
            {
                0: [
                    generate_cock_coco_annotation(annotation_id=0, image_id=0, category_id=0),
                ],
                1: [
                    generate_cock_coco_annotation(annotation_id=1, image_id=1, category_id=1),
                    generate_cock_coco_annotation(annotation_id=2, image_id=1, category_id=2),
                ],
                2: [
                    generate_cock_coco_annotation(annotation_id=3, image_id=2, category_id=3),
                ],
                3: [
                    generate_cock_coco_annotation(annotation_id=4, image_id=3, category_id=1),
                    generate_cock_coco_annotation(annotation_id=5, image_id=3, category_id=2),
                    generate_cock_coco_annotation(annotation_id=5, image_id=3, category_id=3),
                ]
            },
            DoesNotRaise()
        ),  # two coco annotations
    ]
)
def test_group_coco_annotations_by_image_id(
    coco_annotations: List[dict],
    expected_result: dict,
    exception: Exception
) -> None:
    with exception:
        result = group_coco_annotations_by_image_id(coco_annotations=coco_annotations)
        assert result == expected_result
