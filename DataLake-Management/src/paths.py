from enum import Enum

class TABLES(Enum):
    TRAIN = '../tables/github-pipelines/'
    TEST = '../tables/commercial-pipelines/'

class TRAIN_EVAL(Enum):
    TRAIN = './train_eval/training/'
    EVAL = './train_eval/evaluation/'

DATASET = '../processedDataset/'