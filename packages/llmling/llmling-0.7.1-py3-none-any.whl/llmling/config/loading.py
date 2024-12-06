"""Configuration loading utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING

import logfire
import yamling

from llmling.core import exceptions
from llmling.core.log import get_logger


if TYPE_CHECKING:
    import os

    from llmling.config.models import Config


logger = get_logger(__name__)


@logfire.instrument("Loading configuration from {path}")
def load_config(path: str | os.PathLike[str]) -> Config:
    """Load configuration from YAML file.

    This function only handles the basic loading and model validation.
    For full validation and management, use ConfigManager.load() instead.

    Args:
        path: Path to configuration file

    Returns:
        Loaded configuration

    Raises:
        ConfigError: If loading fails

    Example:
        >>> try:
        ...     config = load_config("config.yml")
        ...     manager = ConfigManager(config)
        ...     manager.validate_or_raise()
        ... except ConfigError as e:
        ...     print(f"Error: {e}")
    """
    logger.debug("Loading configuration from %s", path)

    try:
        content = yamling.load_yaml_file(path)
    except Exception as exc:
        msg = f"Failed to load YAML from {path!r}"
        raise exceptions.ConfigError(msg) from exc

    # Validate basic structure
    if not isinstance(content, dict):
        msg = "Configuration must be a dictionary"
        raise exceptions.ConfigError(msg)

    try:
        from llmling.config.models import Config

        # Convert to model (only basic pydantic validation)
        config = Config.model_validate(content)
    except Exception as exc:
        msg = f"Failed to validate configuration from {path}"
        raise exceptions.ConfigError(msg) from exc
    else:
        msg = "Loaded raw configuration: version=%s, resources=%d"
        logger.debug(msg, config.version, len(config.resources))
        return config


if __name__ == "__main__":
    import sys

    from llmling.config.manager import ConfigManager

    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yml"
    manager: ConfigManager = ConfigManager.load(config_path)
