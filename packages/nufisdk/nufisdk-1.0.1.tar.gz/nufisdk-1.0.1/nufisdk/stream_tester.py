import requests
import websockets
import asyncio
import base64
import yaml
import os
from PIL import Image
from typing import Dict, List
from io import BytesIO
from tqdm import tqdm


class StreamApiTester:
    CONFIG_FILE = ".nufi/config.yaml"

    def __init__(self):
        self.config_data = self._load_config()
        self.server_config = self.config_data.get("server", {})
        self.server_url = self.server_config.get("server_url", "http://localhost:8000")
        self.pipeline_name = self.server_config.get("pipeline_name", None)
        self.websocket_url = self.server_config.get("websocket_url", None)

    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        if not os.path.exists(self.CONFIG_FILE):
            default_config = {
                "config": {
                    "current_context": "default",
                    "default": "http://localhost/api/deployments",
                },
                "server": {
                    "pipeline_name": None,
                    "server_url": "http://localhost:8000",
                    "websocket_url": None,
                },
            }
            with open(self.CONFIG_FILE, "w") as f:
                yaml.dump(default_config, f, default_flow_style=False)
            return default_config
        else:
            with open(self.CONFIG_FILE, "r") as f:
                return yaml.safe_load(f)

    def _save_config(self):
        """Save the current configuration to YAML file."""
        self.config_data["server"] = self.server_config
        with open(self.CONFIG_FILE, "w") as f:
            yaml.dump(self.config_data, f)

    def set_url(self, url: str) -> str:
        """Set the server URL."""
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"http://{url}"
        self.server_url = url
        self.server_config["server_url"] = self.server_url
        self._save_config()
        return f"Server URL set to: {url}"

    def get_url(self) -> str:
        """Get the current server URL."""
        return self.server_url

    def list_pipelines(self) -> List[Dict[str, str]]:
        """List available pipelines."""
        try:
            response = requests.get(f"{self.server_url}/pipelines")
            response.raise_for_status()
            pipelines = response.json()

            return [
                {"pipeline_name": name, "steps": command.split("!")}
                for name, command in pipelines.items()
            ]
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to get pipelines: {e}")

    def select_pipeline(self, pipeline_name: str) -> str:
        """Select a pipeline by name."""
        try:
            response = requests.post(
                f"{self.server_url}/pipelines/select",
                json={"pipeline_id": pipeline_name},
            )
            response.raise_for_status()
            result = response.json()

            clean_server_url = self.server_url.replace("http://", "").replace(
                "https://", ""
            )
            websocket_url = f"ws://{clean_server_url}/ws"

            self.server_config["pipeline_name"] = pipeline_name
            self.server_config["websocket_url"] = websocket_url
            self._save_config()

            return f"Pipeline '{pipeline_name}' selected. WebSocket URL set to: {websocket_url}"
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to select pipeline: {e}")

    async def _send_video_stream(self, websocket_url: str, video_path: str):
        """Send video frames to the server via WebSocket."""
        output_dir = "output_frames"
        os.makedirs(output_dir, exist_ok=True)

        async with websockets.connect(websocket_url) as websocket:
            cap = Image.open(video_path)
            frame_number = 0
            total_frames = cap.n_frames

            with tqdm(total=total_frames, desc="Streaming Video", unit="frame") as pbar:
                while True:
                    try:
                        cap.seek(frame_number)
                        frame = cap.convert("RGB")
                        buffer = BytesIO()
                        frame.save(buffer, format="JPEG")
                        frame_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
                        await websocket.send(frame_data)
                        response = await websocket.recv()

                        # Save the processed frame
                        output_path = os.path.join(
                            output_dir, f"output_{frame_number}.jpg"
                        )
                        with open(output_path, "wb") as f:
                            f.write(base64.b64decode(response))

                        frame_number += 1
                        pbar.update(1)
                    except EOFError:
                        break

    def stream_video(self, video_path: str):
        """Stream a video file to the server."""
        if not self.pipeline_name or not self.websocket_url:
            raise ValueError(
                "Pipeline name or WebSocket URL is not set. Please select a pipeline first."
            )

        try:
            asyncio.run(self._send_video_stream(self.websocket_url, video_path))
            return "Video streaming completed."
        except Exception as e:
            raise RuntimeError(f"An error occurred during video streaming: {e}")


class StreamerCommands:
    def __init__(self):
        self.api_tester = StreamApiTester()

    def set_url(self, url: str) -> str:
        """Set the server URL."""
        return self.api_tester.set_url(url)

    def get_url(self) -> str:
        """Get the server URL."""
        return self.api_tester.get_url()

    def list_pipelines(self) -> List[Dict[str, str]]:
        """List available pipelines."""
        return self.api_tester.list_pipelines()

    def select_pipeline(self, pipeline_name: str) -> str:
        """Select a pipeline by name."""
        return self.api_tester.select_pipeline(pipeline_name)

    def stream_video(self, video_path: str) -> str:
        """Stream a video to the selected pipeline."""
        return self.api_tester.stream_video(video_path)
