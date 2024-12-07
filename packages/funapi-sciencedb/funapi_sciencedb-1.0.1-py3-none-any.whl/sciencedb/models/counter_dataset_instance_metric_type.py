from enum import Enum


class COUNTERDatasetInstanceMetricType(str, Enum):
    TOTAL_DATASET_INVESTIGATIONS = "total-dataset-investigations"
    TOTAL_DATASET_REQUESTS = "total-dataset-requests"
    UNIQUE_DATASET_INVESTIGATIONS = "unique-dataset-investigations"
    UNIQUE_DATASET_REQUESTS = "unique-dataset-requests"

    def __str__(self) -> str:
        return str(self.value)
