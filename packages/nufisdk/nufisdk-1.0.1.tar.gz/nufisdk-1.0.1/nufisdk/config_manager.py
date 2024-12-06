import yaml
import os
from typing import Optional, Dict
from tabulate import tabulate
from nufisdk.utils import generate_random_name

CONFIG_FILE = ".nufi/config.yaml"


class ConfigManager:
    def __init__(self):
        config = self.load_config()
        self.config_data = config.get("config", {})
        self.inference_data = config.get("inference", {"url": ""})
        self.default_url = self.config_data.get("default", "")
        self.current_context = self.config_data.get("current_context", "default")
        if "default" not in self.config_data:
            self.config_data["default"] = ""
        self.save_config()

    def save_config(self):
        """Save the configuration data to the YAML file."""
        all_data = self.load_config()
        all_data["config"] = self.config_data
        all_data["inference"] = self.inference_data
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(all_data, f)

    def load_config(self) -> Dict:
        """Load the configuration data from the YAML file."""
        config_dir = os.path.dirname(CONFIG_FILE)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        if not os.path.exists(CONFIG_FILE):
            default_config = {
                "config": {"default": "", "current_context": "default"},
                "inference": {"url": ""},
            }
            with open(CONFIG_FILE, "w") as f:
                yaml.dump(default_config, f, default_flow_style=False)
            return default_config
        else:
            with open(CONFIG_FILE, "r") as f:
                return yaml.safe_load(f)

    def set(self, name: Optional[str] = None, url: Optional[str] = None):
        """Set a new configuration or update an existing one."""
        if not url:
            raise ValueError("URL is required for setting configuration.")
        if not name:
            name = generate_random_name()
        self.config_data[name] = url
        self.save_config()
        return f"Configuration '{name}' set with URL '{url}'."

    def list_configs(self) -> str:
        """List all configurations."""
        headers = ["Context", "Config Name", "URL"]
        table = [
            [
                "*" if self.current_context == "default" else "",
                "default",
                self.default_url,
            ]
        ]
        for name, url in self.config_data.items():
            if name in ["current_context", "default"]:
                continue
            table.append(["*" if name == self.current_context else "", name, url])
        return tabulate(table, headers, tablefmt="pretty")

    def delete(self, name: str):
        """Delete a configuration by name."""
        if name == "default":
            raise ValueError("Cannot delete the default context.")
        if name in self.config_data:
            if name == self.current_context:
                self.current_context = "default"
            del self.config_data[name]
            self.save_config()
            return f"Configuration '{name}' deleted."
        else:
            raise ValueError(f"Configuration '{name}' does not exist.")

    def set_current_context(
        self, name: Optional[str] = None, url: Optional[str] = None
    ):
        """Set the current context by name or URL."""
        if name and name in self.config_data:
            self.current_context = name
        elif url and url in self.config_data.values():
            name = next(
                (key for key, value in self.config_data.items() if value == url), None
            )
            self.current_context = name
        else:
            raise ValueError("Configuration name or URL must exist.")
        self.config_data["current_context"] = self.current_context
        self.save_config()
        return f"Current context set to '{self.current_context}'."

    def get_current_context(self) -> Dict[str, str]:
        """Get the current context."""
        context_url = self.config_data.get(self.current_context, self.default_url)
        return {"current_context": self.current_context, "url": context_url}

    def reset(self):
        """Reset the configuration to default settings."""
        default_config = {
            "config": {"default": "", "current_context": "default"},
            "inference": {"url": ""},
        }
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(default_config, f, default_flow_style=False)
        self.config_data = default_config["config"]
        self.current_context = "default"
        self.save_config()
        return "Configuration reset to default."
