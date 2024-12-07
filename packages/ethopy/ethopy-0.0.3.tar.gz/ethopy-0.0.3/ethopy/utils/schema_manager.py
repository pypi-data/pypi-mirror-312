import json
from pathlib import Path
from typing import Dict, Optional

import datajoint as dj


class SchemaManager:
    """Manages DataJoint schema creation and access"""

    def __init__(self):
        """Initialize the schema manager with empty schemas"""
        self.schemas = {}
        self._initialize_empty_schemas()
        # Try to load config and update schemas if possible
        try:
            self.config = self._load_config()
            self.initialize_virtual_schemas()
        except FileNotFoundError:
            pass

    def _initialize_empty_schemas(self):
        """Initialize empty schemas"""
        schema_names = ["experiment", "stimulus", "behavior", "recording", "mice"]
        for name in schema_names:
            schema = dj.Schema()
            self.schemas[name] = schema
            setattr(self, name, schema)

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

    def initialize_virtual_schemas(
        self, connection: Optional[dj.Connection] = None
    ) -> Dict[str, dj.VirtualModule]:
        """Initialize schemas as virtual modules if config exists"""
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
            # Update schema attributes
            for name, schema in self.schemas.items():
                setattr(self, name, schema)

            return self.schemas

        except Exception as e:
            raise Exception(f"Failed to create virtual modules: {str(e)}")


_schema_manager = SchemaManager()

# Export schemas directly - these will be empty dj.Schema() on install
# and get upgraded to virtual modules when local_conf.json is present
experiment = _schema_manager.experiment
stimulus = _schema_manager.stimulus
behavior = _schema_manager.behavior
recording = _schema_manager.recording
mice = _schema_manager.mice
