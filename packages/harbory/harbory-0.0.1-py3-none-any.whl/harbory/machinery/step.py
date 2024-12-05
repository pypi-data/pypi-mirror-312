from collections.abc import Iterator
from typing import Any, Optional, Union

from harbory.workflow import step, use_step_logger

from .archive import MachineryArchive
from .data import DataSource
from .format import MachineryArchiveFormat
from .model import Model, T_EvaluationParams, T_PredictionParams, T_SetupParams
from .processor import Processor
from .types import T_Example, T_Prediction


@step(
    "harbory.machinery.train",
    format=MachineryArchiveFormat(),
)
def train(
    model: Model[T_Example, T_Prediction, Any, T_SetupParams, Any, T_EvaluationParams],
    train_dataset: DataSource[T_Example],
    valid_dataset: Optional[DataSource[T_Example]] = None,
    test_dataset: Optional[DataSource[T_Example]] = None,
    setup: Optional[T_SetupParams] = None,
    evaluation: Optional[T_EvaluationParams] = None,
    preprocessor: Optional[Processor[T_Example, T_Example, Any, Any]] = None,
) -> MachineryArchive[Model[T_Example, T_Prediction, Any, T_SetupParams, Any, T_EvaluationParams]]:
    logger = use_step_logger(default="harbory.machinery.train")

    logger.info("Loading datasets...")
    train_dataset_iterator = train_dataset.load()
    valid_dataset_iterator = valid_dataset.load() if valid_dataset is not None else None
    test_dataset_iterator = test_dataset.load() if test_dataset is not None else None

    if preprocessor is not None:
        train_dataset_iterator = preprocessor(train_dataset_iterator)
        if valid_dataset_iterator is not None:
            valid_dataset_iterator = preprocessor(valid_dataset_iterator)
        if test_dataset_iterator is not None:
            test_dataset_iterator = preprocessor(test_dataset_iterator)

    logger.info("Start training...")
    model.setup(setup)
    model.train(train_dataset_iterator, valid_dataset_iterator)

    if test_dataset_iterator is not None:
        logger.info("Start evaluation on test dataset...")
        metrics = model.evaluate(test_dataset_iterator)
        logger.info(f"Test metrics: {metrics}")

    return MachineryArchive(model=model)


@step("harbory.machinery.predict")
def predict(
    model: Union[
        Model[T_Example, T_Prediction, Any, Any, T_PredictionParams, Any],
        MachineryArchive[Model[T_Example, T_Prediction, Any, Any, T_PredictionParams, Any]],
    ],
    dataset: DataSource[T_Example],
    setup: Optional[T_PredictionParams] = None,
    params: Optional[T_PredictionParams] = None,
    preprocessor: Optional[Processor[T_Example, T_Example, Any, Any]] = None,
    postprocessor: Optional[Processor[T_Prediction, T_Prediction, Any, Any]] = None,
    batch_size: Optional[int] = None,
    max_workers: Optional[int] = None,
) -> Iterator[T_Prediction]:
    logger = use_step_logger(default="harbory.machinery.predict")

    if isinstance(model, MachineryArchive):
        model = model.model

    model.setup(setup)

    logger.info("Loading dataset...")
    dataset_iterator = dataset.load()

    if preprocessor is not None:
        dataset_iterator = preprocessor(dataset_iterator)

    logger.info("Start prediction...")
    prediction_iterator = model.predict(
        dataset_iterator,
        params=params,
        batch_size=batch_size,
        max_workers=max_workers,
    )

    if postprocessor is not None:
        prediction_iterator = postprocessor(prediction_iterator)

    return prediction_iterator


@step("harbory.machinery.evaluate")
def evaluate(
    model: Union[
        Model[T_Example, T_Prediction, Any, T_SetupParams, Any, T_EvaluationParams],
        MachineryArchive[Model[T_Example, T_Prediction, Any, Any, Any, T_EvaluationParams]],
    ],
    dataset: DataSource[T_Example],
    setup: Optional[T_SetupParams] = None,
    params: Optional[T_EvaluationParams] = None,
    preprocessor: Optional[Processor[T_Example, T_Example, Any, Any]] = None,
) -> dict[str, Any]:
    logger = use_step_logger(default="harbory.machinery.evaluate")

    if isinstance(model, MachineryArchive):
        model = model.model

    model.setup(setup)

    logger.info("Loading dataset...")
    dataset_iterator = dataset.load()

    if preprocessor is not None:
        dataset_iterator = preprocessor(dataset_iterator)

    logger.info("Start evaluation...")
    metrics = model.evaluate(dataset_iterator, params=params)

    return metrics
