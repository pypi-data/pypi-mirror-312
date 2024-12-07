import importlib
import os
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type

import pkg_resources


class BasePlugin(ABC):
    """
    Abstract base class for all plugins to ensure consistent interface
    """

    @abstractmethod
    def validate(self) -> bool:
        """
        Validate plugin configuration and requirements
        """
        pass

    @abstractmethod
    def initialize(self, config: Dict[str, Any]):
        """
        Initialize plugin with specific configuration
        """
        pass


class PluginManager:
    def __init__(
        self, package_name: str = "mypackage", config_dir: Optional[str] = None
    ):
        """
        Comprehensive plugin management system

        :param package_name: Base package name for namespace
        :param config_dir: Optional configuration directory
        """
        self.package_name = package_name
        self.config_dir = config_dir or os.path.join(
            os.path.expanduser("~"), f".{package_name}"
        )

        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)

        # Plugin registries
        self._plugin_registry = {"experiments": {}, "behaviors": {}, "stimuli": {}}

    def discover_plugins(self) -> Dict[str, list]:
        """
        Discover plugins using multiple mechanisms:
        1. Entry points
        2. Local filesystem
        3. Installed packages
        """
        discovered_plugins = {"experiments": [], "behaviors": [], "stimuli": []}

        # Discover via setuptools entry points
        for entry_point_group in self._plugin_registry.keys():
            entry_point_name = f"{self.package_name}.{entry_point_group}"
            discovered_plugins[entry_point_group] = [
                ep.name for ep in pkg_resources.iter_entry_points(entry_point_name)
            ]

        # Discover via local filesystem
        for plugin_type in self._plugin_registry.keys():
            local_plugin_dir = os.path.join(self.config_dir, "plugins", plugin_type)
            if os.path.isdir(local_plugin_dir):
                local_plugins = [
                    f.replace(".py", "")
                    for f in os.listdir(local_plugin_dir)
                    if f.endswith(".py") and not f.startswith("__")
                ]
                discovered_plugins[plugin_type].extend(local_plugins)

        return discovered_plugins

    def load_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> BasePlugin:
        """
        Load a plugin with multiple discovery mechanisms

        :param plugin_type: Type of plugin (experiments, behaviors, stimuli)
        :param plugin_name: Name of the plugin
        :param config: Optional configuration dictionary
        :return: Instantiated plugin
        """
        # First, try entry points
        entry_point_name = f"{self.package_name}.{plugin_type}"
        for ep in pkg_resources.iter_entry_points(entry_point_name, plugin_name):
            try:
                plugin_class = ep.load()
                plugin_instance = plugin_class()
                if plugin_instance.validate():
                    plugin_instance.initialize(config or {})
                    return plugin_instance
            except Exception as e:
                print(f"Error loading entry point plugin {plugin_name}: {e}")

        # Then, try local filesystem
        local_plugin_dir = os.path.join(self.config_dir, "plugins", plugin_type)
        plugin_path = os.path.join(local_plugin_dir, f"{plugin_name}.py")

        if os.path.exists(plugin_path):
            try:
                spec = importlib.util.spec_from_file_location(
                    f"{self.package_name}.{plugin_type}.{plugin_name}", plugin_path
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Find plugin class
                plugin_classes = [
                    cls
                    for cls in module.__dict__.values()
                    if (
                        isinstance(cls, type)
                        and issubclass(cls, BasePlugin)
                        and cls is not BasePlugin
                    )
                ]

                if plugin_classes:
                    plugin_instance = plugin_classes[0]()
                    if plugin_instance.validate():
                        plugin_instance.initialize(config or {})
                        return plugin_instance
            except Exception as e:
                print(f"Error loading local plugin {plugin_name}: {e}")

        raise ImportError(f"Plugin {plugin_name} not found in {plugin_type}")


# Example Plugin Implementation
class ExperimentPlugin(BasePlugin):
    def __init__(self):
        self.config = {}
        self.name = None

    def validate(self) -> bool:
        """
        Validate plugin requirements
        """
        # Example validation logic
        return self.name is not None

    def initialize(self, config: Dict[str, Any]):
        """
        Initialize plugin with configuration
        """
        self.config = config


# Example setup.py for entry point registration
"""
from setuptools import setup

setup(
    name='mypackage',
    # ... other setup parameters
    entry_points={
        'mypackage.experiments': [
            'myexp = mypackage.plugins.experiments:MyExperiment'
        ],
        'mypackage.behaviors': [
            'mybehavior = mypackage.plugins.behaviors:MyBehavior'
        ]
    }
)
"""


# Usage Example
def main():
    # Initialize plugin manager
    plugin_manager = PluginManager()

    # Discover available plugins
    print("Available Plugins:", plugin_manager.discover_plugins())

    # Load a specific plugin
    try:
        experiment = plugin_manager.load_plugin(
            "experiments", "myexp", config={"param1": "value1"}
        )
        # Use the plugin
    except ImportError as e:
        print(f"Plugin loading failed: {e}")


# Recommended Project Structure
"""
mypackage/
├── setup.py
├── mypackage/
│   ├── __init__.py
│   ├── plugin_manager.py
│   └── plugins/
│       ├── __init__.py
│       ├── experiments/
│       ├── behaviors/
│       └── stimuli/
└── README.md
"""
