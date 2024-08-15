import os
import sys
from typing import Tuple

import joblib
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.datasets import ImageFolder

from Xray.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
)
from Xray.entity.config_entity import DataTransformationConfig
from Xray.exception import XRayException
from Xray.logger import logging



'''
Transformation parameter  terms

Resize: Resize the input image to the given image
CenterCrop: Crops the given image at the center
ColorJitter: Randomly change the brightness, contrast, saturation and hue of an image.
RandomHorizontalFlip: Horizontally flip the given image randomly with a given probability
RandomRotation: Rotate the image by angle
ToTensor: Convert numpy.ndarray to tensor
Normalize: Normalize a float tensor image with mean and standard deviation.
'''


class DataTransformation:
    def __init__(
        self,
        data_transformation_config: DataTransformationConfig,
        data_ingestion_artifact: DataIngestionArtifact,
    ):
        self.data_transformation_config = data_transformation_config

        self.data_ingestion_artifact = data_ingestion_artifact

    def transforming_training_data(self) -> transforms.Compose:
        try:
            logging.info(
                "Entered the transforming_training_data method of Data transformation class"
            )

            train_transform: transforms.Compose = transforms.Compose(
                [
                    transforms.Resize(self.data_transformation_config.RESIZE),
                    transforms.CenterCrop(self.data_transformation_config.CENTERCROP),
                    transforms.ColorJitter(
                        **self.data_transformation_config.color_jitter_transforms
                    ),
                    transforms.RandomHorizontalFlip(),
                    transforms.RandomRotation(
                        self.data_transformation_config.RANDOMROTATION
                    ),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        **self.data_transformation_config.normalize_transforms
                    ),
                ]
            )

            logging.info(
                "Exited the transforming_training_data method of Data transformation class"
            )

            return train_transform

        except Exception as e:
            raise XRayException(e, sys)
        


    def transforming_testing_data(self) -> transforms.Compose:
        logging.info(
            "Entered the transforming_testing_data method of Data transformation class"
        )

        try:
            test_transform: transforms.Compose = transforms.Compose(
                [
                    transforms.Resize(self.data_transformation_config.RESIZE),
                    transforms.CenterCrop(self.data_transformation_config.CENTERCROP),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        **self.data_transformation_config.normalize_transforms
                    ),
                ]
            )

            logging.info(
                "Exited the transforming_testing_data method of Data transformation class"
            )

            return test_transform

        except Exception as e:
            raise XRayException(e, sys)
        


    '''
    Creating data loader:

    - For our usecase will be using the default data loader for PyTorch
    - We will be creating 2 data loaders one for training data and other for the test data
    - Batch size is a hyperparameter which we can tweak according to our need and system
    - we can provide Image shuffling True for training data and False for test data
    - Pin memory is used to transfer the loaded dataset from CPU to GPU
    '''

    
    def data_loader(
        self, train_transform: transforms.Compose, test_transform: transforms.Compose
    ) -> Tuple[DataLoader, DataLoader]:
        try:
            logging.info("Entered the data_loader method of Data transformation class")

            train_data: Dataset = ImageFolder(
                os.path.join(self.data_ingestion_artifact.train_file_path),
                transform=train_transform,
            )

            test_data: Dataset = ImageFolder(
                os.path.join(self.data_ingestion_artifact.test_file_path),
                transform=test_transform,
            )

            logging.info("Created train data and test data paths")

            train_loader: DataLoader = DataLoader(
                train_data, **self.data_transformation_config.data_loader_params
            )

            test_loader: DataLoader = DataLoader(
                test_data, **self.data_transformation_config.data_loader_params
            )

            logging.info("Exited the data_loader method of Data transformation class")

            return train_loader, test_loader

        except Exception as e:
            raise XRayException(e, sys)
        


    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info(
                "Entered the initiate_data_transformation method of Data transformation class"
            )

            train_transform: transforms.Compose = self.transforming_training_data()

            test_transform: transforms.Compose = self.transforming_testing_data()

            os.makedirs(self.data_transformation_config.artifact_dir, exist_ok=True)

            joblib.dump(
                train_transform, self.data_transformation_config.train_transforms_file
            )

            joblib.dump(
                test_transform, self.data_transformation_config.test_transforms_file
            )

            train_loader, test_loader = self.data_loader(
                train_transform=train_transform, test_transform=test_transform
            )

            data_transformation_artifact: DataTransformationArtifact = DataTransformationArtifact(
                transformed_train_object=train_loader,
                transformed_test_object=test_loader,
                train_transform_file_path=self.data_transformation_config.train_transforms_file,
                test_transform_file_path=self.data_transformation_config.test_transforms_file,
            )

            logging.info(
                "Exited the initiate_data_transformation method of Data transformation class"
            )

            return data_transformation_artifact

        except Exception as e:
            raise XRayException(e, sys)