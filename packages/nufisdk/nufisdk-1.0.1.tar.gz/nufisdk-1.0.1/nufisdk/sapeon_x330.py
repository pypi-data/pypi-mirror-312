import json
import requests
from typing import List, Optional, Dict
from nufisdk.config_manager import ConfigManager


class SapeonX330:
    """
    SapeonX330 SDK for managing inference API and models.
    """

    CONFIG_FILE = ".nufi/config.yaml"

    def __init__(self):
        self.config_manager = ConfigManager()
        self.inference_url = self._load_inference_url()
        self.no_url_message = (
            "Inference URL is not set. Please configure it using `set_inference_url`."
        )

    def _load_inference_url(self) -> Optional[str]:
        """Load the inference URL from the configuration."""
        config = self.config_manager.load_config()
        return config.get("inference", {}).get("url", None)

    def set_inference_url(self, url: str) -> str:
        """
        Set the inference API server URL.

        Args:
            url (str): Inference API server URL.

        Returns:
            str: Confirmation message.
        """
        if not url:
            raise ValueError("Inference API server URL is required.")
        config = self.config_manager.load_config()
        config["inference"] = {"url": url}
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        self.inference_url = url
        return f"Inference API server URL set to: {url}"

    def get_inference_url(self) -> str:
        """
        Get the current inference API server URL.

        Returns:
            str: Inference API server URL.
        """
        if self.inference_url:
            return self.inference_url
        else:
            raise ValueError(self.no_url_message)

    def list_models(self) -> List[str]:
        """
        List uploaded models on the server.

        Returns:
            List[str]: A list of model names.
        """
        if not self.inference_url:
            raise ValueError(self.no_url_message)

        try:
            response = requests.get(f"{self.inference_url}/api/models")
            response.raise_for_status()
            models = response.json().get("models", [])
            return [model[:-4] for model in models]  # Remove file extension (.smp)
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to list uploaded models: {e}")

    def upload_model(self, name: str, model_path: str) -> str:
        """
        Upload a model to the server.

        Args:
            name (str): Model name.
            model_path (str): Path to the .smp model file.

        Returns:
            str: Confirmation message.
        """
        if not self.inference_url:
            raise ValueError(self.no_url_message)

        try:
            with open(model_path, "rb") as f:
                files = {"file": f}
                data = {"name": name}
                response = requests.post(
                    f"{self.inference_url}/api/models", files=files, data=data
                )
                response.raise_for_status()
            return f"Successfully uploaded model '{name}' from file '{model_path}'."
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to upload model: {e}")

    def delete_model(self, name: str) -> str:
        """
        Delete a model from the server.

        Args:
            name (str): Name of the model to delete.

        Returns:
            str: Confirmation message.
        """
        if not self.inference_url:
            raise ValueError(self.no_url_message)

        try:
            response = requests.delete(f"{self.inference_url}/api/models/{name}")
            response.raise_for_status()
            return f"Successfully deleted model '{name}'."
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to delete model: {e}")

    def run_inference(
        self, name: str, preprocessed_image_path: str, output_path: str
    ) -> Dict:
        """
        Run inference on a preprocessed image using a specific model.

        Args:
            name (str): Model name.
            preprocessed_image_path (str): Path to the preprocessed .npy image file.
            output_path (str): Path to save the inference result.

        Returns:
            Dict: Inference result as a dictionary.
        """
        if not self.inference_url:
            raise ValueError(self.no_url_message)

        try:
            with open(preprocessed_image_path, "rb") as f:
                files = {"file": f}
                response = requests.post(
                    f"{self.inference_url}/api/inference/{name}", files=files
                )
                response.raise_for_status()
                inference_result = response.json()

            with open(output_path, "w") as f:
                json.dump(inference_result, f, indent=2)

            return inference_result
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to run inference: {e}")
