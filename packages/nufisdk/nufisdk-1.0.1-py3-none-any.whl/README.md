### Python CLI (name : nufictl) for CRD npudeploy 

```bash
poetry shell
poetry install
```

* example usage
```python

from nufisdk import NufiSdk
from img_utils import preprocess_image, postprocess_results, create_output_path

# Config Constants
CONTAINER_IMAGE_NAME = "[Your NPU Deploy Image]"
NUFI_SERVER_URL = "[Your NuFi Server URL]"
NPU_SERVER_URL = "[Your NPU Deployment URL]"
MODEL_NAME = "yolov7"
MODEL_PATH = "./x330_yolo/models/yolov7.smp"
IMAGE_PATH = "./x330_yolo/datasets/imgs/kite.jpg"
OUTPUT_PATH = create_output_path(IMAGE_PATH)

nfk = NufiSdk()


# simple example
def simple():
    nfk.config.set("x330_server", NUFI_SERVER_URL)
    nfk.config.set_current_context("x330_server")
    preprocessed_img = preprocess_image(IMAGE_PATH)
    nfk.x330.set_inference_url(NPU_SERVER_URL)
    nfk.x330.upload_model(MODEL_NAME, MODEL_PATH)
    nfk.x330.run_inference(MODEL_NAME, preprocessed_img, OUTPUT_PATH)
    postprocess_results(IMAGE_PATH, OUTPUT_PATH)


# detailed example
def detail():
    nfk.config.set("x330_server", NUFI_SERVER_URL)
    nfk.config.set_current_context("x330_server")

    deployments = nfk.list_deployments()
    print(f"Found {len(deployments)} deployments.")
    for deploy in deployments:
        print(f" - {deploy.name}: {deploy.endpoint}")

    preprocessed_img = preprocess_image(IMAGE_PATH)

    print("Configuring X330 inference server...")
    nfk.x330.set_inference_url(NPU_SERVER_URL)
    print(nfk.x330.get_inference_url())

    # # List models on the server
    models = nfk.x330.list_models()
    print(f"Found {len(models)} models on the server.")
    for model in models:
        print(f" - {model}")

    # Upload the model to the X330 server
    print(f"Uploading model '{MODEL_NAME}' to the server...")
    upload_message = nfk.x330.upload_model(MODEL_NAME, MODEL_PATH)
    print(upload_message)

    # # Run inference
    print(f"Running inference on image '{IMAGE_PATH}' using model '{MODEL_NAME}'...")
    inference_result = nfk.x330.run_inference(MODEL_NAME, preprocessed_img, OUTPUT_PATH)
    print("Inference result saved to:", OUTPUT_PATH)

    # # Postprocess results
    print("Postprocessing inference results...")
    postprocess_results(IMAGE_PATH, OUTPUT_PATH)
    print("Postprocessing completed. Check the output image.")


if __name__ == "__main__":
    simple()
    # detail()


```