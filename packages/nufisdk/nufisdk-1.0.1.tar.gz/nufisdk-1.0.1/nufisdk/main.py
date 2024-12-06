import json
import requests
from typing import Optional, List
from nufisdk.version import __version__
from nufisdk.config_manager import ConfigManager
from nufisdk.model import DeployDetail
from nufisdk.stream_tester import StreamApiTester, StreamerCommands
from nufisdk.sapeon_x330 import SapeonX330


class NufiSdk:
    def __init__(self):
        self.config: ConfigManager = ConfigManager()
        self.streamer: StreamApiTester = StreamApiTester()
        self.x330: SapeonX330 = SapeonX330()
        self.base_url = self.config.config_data.get(
            self.config.current_context,
            self.config.config_data["default"],
        )

    def version(self) -> str:
        return f"NufiSdk version: {__version__}"

    def list_deployments(self) -> List[DeployDetail]:
        """
        List all deployments.

        Returns:
            List[DeployDetail]: A list of deployments.
        """
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            data = response.json()

            items = data.get("items", [])
            deployments = []
            for item in items:
                name = item["metadata"]["name"]
                namespace = item["metadata"]["namespace"]
                creation_timestamp = item["metadata"]["creationTimestamp"]
                replicas = item["spec"]["replicas"]
                image = item["spec"]["template"]["spec"]["containers"][0]["image"]
                cpu = item["spec"]["template"]["spec"]["containers"][0]["resources"][
                    "requests"
                ]["cpu"]
                memory = item["spec"]["template"]["spec"]["containers"][0]["resources"][
                    "requests"
                ]["memory"]
                resources = item["spec"]["template"]["spec"]["containers"][0][
                    "resources"
                ]["limits"]
                accelerator_type = next(
                    (key for key in resources if key not in ["cpu", "memory"]), "none"
                )
                accelerator_count = resources.get(accelerator_type, "1")
                endpoint = item.get("endpoint", "N/A")
                available_replicas = item["status"].get("availableReplicas", 0)

                deployment = DeployDetail(
                    name=name,
                    namespace=namespace,
                    image=image,
                    cpu=cpu,
                    memory=memory,
                    creation_timestamp=creation_timestamp,
                    replicas=replicas,
                    accelerator_type=accelerator_type,
                    accelerator_count=accelerator_count,
                    available_replicas=available_replicas,
                    endpoint=endpoint,
                )
                deployments.append(deployment)

            return deployments
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to list deployments: {e}")

    def create_deployment(
        self,
        name: str,
        image: str,
        cpu: str = "1",
        memory: str = "1",
        replicas: int = 1,
        accelerator_type: Optional[str] = None,
        accelerator_count: Optional[int] = 1,
    ) -> str:
        """
        Create a new deployment.

        Args:
            name (str): Name of the deployment.
            image (str): Docker image to use.
            cpu (str): Requested CPU resources.
            memory (str): Requested memory resources.
            replicas (int): Number of replicas.
            accelerator_type (str, optional): Type of accelerator.
            accelerator_count (int, optional): Number of accelerators.

        Returns:
            str: Success message.
        """
        payload = {
            "name": name,
            "image": image,
            "cpu": cpu,
            "memory": memory,
            "replicas": replicas,
        }
        if accelerator_type:
            payload["acceleratorType"] = accelerator_type
        if accelerator_count:
            payload["acceleratorCount"] = accelerator_count

        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(
                self.base_url, headers=headers, data=json.dumps(payload)
            )
            response.raise_for_status()
            return f"Successfully created deployment: {name}"
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to create deployment: {e}")

    def delete_deployment(self, name: str) -> str:
        """
        Delete a deployment by name.

        Args:
            name (str): Name of the deployment to delete.

        Returns:
            str: Success message.
        """
        try:
            response = requests.delete(f"{self.base_url}/{name}")
            response.raise_for_status()
            return f"Successfully deleted deployment: {name}"
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to delete deployment: {e}")

    def get_logs(self, name: str) -> List[str]:
        """
        Retrieve logs for a specific deployment.

        Args:
            name (str): Name of the deployment.

        Returns:
            List[str]: Deployment logs.
        """
        try:
            response = requests.get(f"{self.base_url}/{name}/log", stream=True)
            response.raise_for_status()
            return [line.decode("utf-8") for line in response.iter_lines() if line]
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to retrieve logs: {e}")


def main():
    # This can serve as an example or an entry point for testing the SDK
    sdk = NufiSdk()
    print(sdk.version())
    deployments = sdk.list_deployments()
    print(f"Found {len(deployments)} deployments")


if __name__ == "__main__":
    main()
