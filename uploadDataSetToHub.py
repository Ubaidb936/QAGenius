import config 
from datasets import Dataset, DatasetDict
import pandas as pd

datasetName  = config.datasetName
file_path = config.file_path



if datasetName is None:
    raise ValueError("datasetName is None. Please set the datasetName in config.py.")
if file_path is None:
    raise ValueError("file_path is None. Please set the local file_path in config.py.")


##Push the dataset to huggingFace.....
print("--------------------Pushing the dataset to huggingFaceHub............")
generated_questions = pd.read_csv(file_path)
dataset = Dataset.from_pandas(generated_questions)
dataset.push_to_hub(datasetName)