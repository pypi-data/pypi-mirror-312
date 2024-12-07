# ethopy/core/schema_manager.py
import json
from pathlib import Path
from typing import Dict, Optional

import datajoint as dj


class SchemaManager:
    """Manages DataJoint schema creation and access based on local_conf.json configuration"""

    def __init__(self):
        """Initialize the schema manager with configuration from local_conf.json"""
        self.schemas = {}
        self.config = self._load_config()
        self.initialize_schemas()

    def _load_config(self) -> dict:
        """Load schema configuration from local_conf.json"""
        config_path = Path("local_conf.json")
        if not config_path.exists():
            raise FileNotFoundError("local_conf.json not found!")

        with open(config_path) as f:
            config = json.load(f)

        # Configure DataJoint
        dj.config.update(config["dj_local_conf"])
        dj.logger.setLevel(dj.config["loglevel"])

        return config["SCHEMATA"]

    def initialize_schemas(
        self, connection: Optional[dj.Connection] = None
    ) -> Dict[str, dj.VirtualModule]:
        """Initialize all schemas as virtual modules"""
        try:
            self.schemas = {
                name: dj.create_virtual_module(
                    name,
                    schema,
                    connection=connection,
                    create_tables=True,
                    create_schema=True,
                )
                for name, schema in self.config.items()
            }
            # Make schemas accessible as module attributes
            for name, schema in self.schemas.items():
                setattr(self, name, schema)

            return self.schemas

        except Exception as e:
            raise Exception(f"Failed to create virtual modules: {str(e)}")

    def get_schema(self, name: str) -> dj.VirtualModule:
        """Get a specific schema by name"""
        if name not in self.schemas:
            raise KeyError(f"Schema {name} not initialized")
        return self.schemas[name]

    @property
    def available_schemas(self) -> list:
        """List available schema names"""
        return list(self.schemas.keys())


# # Create singleton instance
# _schema_manager = SchemaManager()

# # Export schemas directly
# experiment = _schema_manager.experiment
# stimulus = _schema_manager.stimulus
# behavior = _schema_manager.behavior
# recording = _schema_manager.recording
# mice = _schema_manager.mice
