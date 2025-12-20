"""
Configuration Loader Utilities Module

Provides utilities for loading, validating, and managing configuration files
in various formats including YAML, JSON, and XML.
"""

import logging
import os
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ConfigLoader:
    """
    Configuration file loader and manager.

    Provides convenient methods for loading configuration files from various
    formats and validating them against schemas.

    Example:
        >>> from shared.utils import ConfigLoader
        >>> config = ConfigLoader.load_yaml("config.yaml")
        >>> print(config)
    """

    @staticmethod
    def load_yaml(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load YAML configuration file.

        Args:
            file_path: Path to YAML file

        Returns:
            Dictionary with configuration or None if load fails

        Raises:
            FileNotFoundError: If file does not exist
            ImportError: If PyYAML not installed

        Example:
            >>> config = ConfigLoader.load_yaml("robot_config.yaml")
            >>> print(f"Robot name: {config['name']}")
        """
        try:
            import yaml
        except ImportError:
            logger.error("PyYAML not installed. Install with: pip install PyYAML")
            raise ImportError("PyYAML is required for YAML loading")

        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        try:
            with open(file_path, 'r') as f:
                config = yaml.safe_load(f)

            logger.info(f"Loaded YAML configuration from: {file_path}")
            logger.debug(f"Configuration keys: {list(config.keys())}")
            return config
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {e}")
            raise ValueError(f"Invalid YAML file: {e}")
        except Exception as e:
            logger.error(f"Failed to load YAML: {e}")
            raise

    @staticmethod
    def load_json(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load JSON configuration file.

        Args:
            file_path: Path to JSON file

        Returns:
            Dictionary with configuration or None if load fails

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If JSON is invalid

        Example:
            >>> config = ConfigLoader.load_json("settings.json")
            >>> print(f"Debug mode: {config['debug']}")
        """
        import json

        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        try:
            with open(file_path, 'r') as f:
                config = json.load(f)

            logger.info(f"Loaded JSON configuration from: {file_path}")
            logger.debug(f"Configuration keys: {list(config.keys())}")
            return config
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            raise ValueError(f"Invalid JSON file: {e}")
        except Exception as e:
            logger.error(f"Failed to load JSON: {e}")
            raise

    @staticmethod
    def load_config(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load configuration file (auto-detect format).

        Args:
            file_path: Path to configuration file (.yaml, .json, etc.)

        Returns:
            Dictionary with configuration

        Raises:
            ValueError: If file format not supported

        Example:
            >>> config = ConfigLoader.load_config("config.yaml")
            >>> # or
            >>> config = ConfigLoader.load_config("settings.json")
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext in ['.yaml', '.yml']:
            return ConfigLoader.load_yaml(file_path)
        elif ext == '.json':
            return ConfigLoader.load_json(file_path)
        else:
            logger.error(f"Unsupported file format: {ext}")
            raise ValueError(f"Unsupported configuration file format: {ext}")

    @staticmethod
    def validate_config(
        config: Dict[str, Any],
        required_keys: list,
        type_schema: Optional[Dict[str, type]] = None
    ) -> bool:
        """
        Validate configuration against schema.

        Args:
            config: Configuration dictionary to validate
            required_keys: List of required keys
            type_schema: Optional dictionary mapping keys to expected types

        Returns:
            True if valid, False otherwise

        Example:
            >>> config = {"robot": "ur5", "speed": 0.5}
            >>> valid = ConfigLoader.validate_config(
            ...     config,
            ...     required_keys=["robot", "speed"],
            ...     type_schema={"robot": str, "speed": float})
            >>> print(f"Valid: {valid}")
        """
        try:
            # Check required keys
            missing_keys = set(required_keys) - set(config.keys())
            if missing_keys:
                logger.error(f"Missing required keys: {missing_keys}")
                return False

            # Check types if schema provided
            if type_schema:
                for key, expected_type in type_schema.items():
                    if key in config:
                        if not isinstance(config[key], expected_type):
                            logger.error(
                                f"Key '{key}' has type {type(config[key]).__name__}, "
                                f"expected {expected_type.__name__}"
                            )
                            return False

            logger.info("Configuration validation passed")
            return True
        except Exception as e:
            logger.error(f"Configuration validation error: {e}")
            return False

    @staticmethod
    def merge_configs(
        base_config: Dict[str, Any],
        override_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge two configuration dictionaries.

        Args:
            base_config: Base configuration dictionary
            override_config: Configuration to merge in (overrides base)

        Returns:
            Merged configuration dictionary

        Example:
            >>> base = {"speed": 0.5, "debug": False}
            >>> override = {"speed": 1.0}
            >>> merged = ConfigLoader.merge_configs(base, override)
            >>> print(merged)  # {"speed": 1.0, "debug": False}
        """
        try:
            merged = base_config.copy()
            merged.update(override_config)

            logger.info(f"Merged {len(override_config)} overrides into base config")
            return merged
        except Exception as e:
            logger.error(f"Failed to merge configs: {e}")
            return base_config

    @staticmethod
    def save_config(
        config: Dict[str, Any],
        file_path: str,
        format: str = "yaml"
    ) -> bool:
        """
        Save configuration to file.

        Args:
            config: Configuration dictionary to save
            file_path: Path to save to
            format: File format ('yaml' or 'json')

        Returns:
            True if save successful, False otherwise

        Example:
            >>> config = {"robot": "ur5", "speed": 1.0}
            >>> ConfigLoader.save_config(config, "my_config.yaml")
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if format == "yaml":
                import yaml
                with open(file_path, 'w') as f:
                    yaml.dump(config, f, default_flow_style=False)
            elif format == "json":
                import json
                with open(file_path, 'w') as f:
                    json.dump(config, f, indent=2)
            else:
                logger.error(f"Unsupported format: {format}")
                return False

            logger.info(f"Configuration saved to: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False

    @staticmethod
    def get_config_value(
        config: Dict[str, Any],
        key_path: str,
        default: Any = None
    ) -> Any:
        """
        Get nested configuration value using dot notation.

        Args:
            config: Configuration dictionary
            key_path: Dot-separated key path (e.g., "robot.speed")
            default: Default value if key not found

        Returns:
            Configuration value or default

        Example:
            >>> config = {"robot": {"speed": 1.0, "name": "ur5"}}
            >>> speed = ConfigLoader.get_config_value(config, "robot.speed")
            >>> print(speed)  # 1.0
        """
        try:
            keys = key_path.split('.')
            value = config

            for key in keys:
                if isinstance(value, dict):
                    value = value.get(key)
                    if value is None:
                        return default
                else:
                    return default

            return value
        except Exception as e:
            logger.debug(f"Error getting config value '{key_path}': {e}")
            return default
