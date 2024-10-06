import mlflow
import mlflow.pyfunc
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import os
from dotenv import load_dotenv

load_dotenv()
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

# Set the MLflow tracking URI to Databricks
mlflow.set_tracking_uri(DATABRICKS_HOST)

# Set the Databricks token as an environment variable
os.environ["MLFLOW_TRACKING_TOKEN"] = DATABRICKS_TOKEN
mlflow.set_experiment("/Users/albonwu@umich.edu/distilbert-finetuning")

# Define a custom PythonModel wrapper for Hugging Face models
class HuggingFaceModelWrapper(mlflow.pyfunc.PythonModel):

    def __init__(self, model_name):
        self.model_name = model_name

    def load_context(self, context):
        # Load the pre-trained Hugging Face model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

    def predict(self, context, model_input):
        # Tokenize the input data
        inputs = self.tokenizer(model_input, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            # Perform inference
            outputs = self.model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=1)
        return predictions.numpy()

# Initialize the Hugging Face model wrapper
model_name = "distilbert-base-uncased"
huggingface_model = HuggingFaceModelWrapper(model_name=model_name)

# Start an MLflow run and log the custom model to MLflow
with mlflow.start_run():
    # Log the Hugging Face model with the custom wrapper
    mlflow.pyfunc.log_model(
        artifact_path="distilbert-model",
        python_model=huggingface_model
    )

    # Optionally register the model
    model_uri = f"runs:/{mlflow.active_run().info.run_id}/distilbert-model"
    registered_model = mlflow.register_model(model_uri=model_uri, name="catalog.distilbert_base_uncased")

    print(f"Model {model_name} registered successfully in Unity Catalog!")


