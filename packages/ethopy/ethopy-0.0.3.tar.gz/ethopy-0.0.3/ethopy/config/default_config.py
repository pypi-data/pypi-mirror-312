from dataclasses import dataclass
from typing import Optional, Dict, Any
from pathlib import Path
import os
import json

@dataclass
class DatabaseConfig:
    host: str = "127.0.0.1"
    user: str = "root"
    password: str = ""
    port: int = 3306
    reconnect: bool = True
    use_tls: bool = False
    loglevel: str = "WARNING"

@dataclass
class SchemaConfig:
    experiment: str = "lab_experiments"
    stimulus: str = "lab_stimuli"
    behavior: str = "lab_behavior"
    recording: str = "lab_recordings"
    mice: str = "lab_mice"

@dataclass
class PathConfig:
    source_path: Path = Path.home() / "EthoPy_Files"
    target_path: Optional[Path] = None
    protocol_path: Optional[Path] = None

class Config:
    def __init__(self):
        self.db = DatabaseConfig()
        self.schema = SchemaConfig()
        self.paths = PathConfig()
        self._load_config()

    def _load_config(self):
        self._load_from_env()
        if os.path.exists("local_conf.json"):
            self._load_from_json("local_conf.json")
        self._validate_config()

    def _load_from_env(self):
        if db_host := os.getenv("ETHOPY_DB_HOST"):
            self.db.host = db_host
        if db_user := os.getenv("ETHOPY_DB_USER"):
            self.db.user = db_user
        if db_pass := os.getenv("ETHOPY_DB_PASSWORD"):
            self.db.password = db_pass
        if db_port := os.getenv("ETHOPY_DB_PORT"):
            self.db.port = int(db_port)
        if source_path := os.getenv("ETHOPY_SOURCE_PATH"):
            self.paths.source_path = Path(source_path)

    def _load_from_json(self, config_path: str):
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        if 'dj_local_conf' in config:
            for key, value in config['dj_local_conf'].items():
                key = key.split('.')[-1]
                if hasattr(self.db, key):
                    setattr(self.db, key, value)
                    
        if 'SCHEMATA' in config:
            for key, value in config['SCHEMATA'].items():
                if hasattr(self.schema, key):
                    setattr(self.schema, key, value)

    def _validate_config(self):
        if not self.db.password:
            raise ConfigurationError("Database password not set")
        self.paths.source_path.mkdir(parents=True, exist_ok=True)
        if self.paths.target_path:
            self.paths.target_path.mkdir(parents=True, exist_ok=True)

    @property
    def datajoint_config(self) -> Dict[str, Any]:
        return {
            "database.host": self.db.host,
            "database.user": self.db.user,
            "database.password": self.db.password,
            "database.port": self.db.port,
            "database.reconnect": self.db.reconnect,
            "database.use_tls": self.db.use_tls,
            "loglevel": self.db.loglevel
        }