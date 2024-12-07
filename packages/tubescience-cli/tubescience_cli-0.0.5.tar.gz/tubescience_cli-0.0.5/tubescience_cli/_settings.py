
from app_paths import get_paths
from typing import Tuple, Type
from importlib.metadata import entry_points

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)
from pydantic import create_model

from pathlib import Path

paths = get_paths('tubescience_cli', 'TubeScience')
paths.env_paths = ( Path.cwd() / '.env', )
paths.secrets_paths = ( Path('/var/run'), Path('/run/secrets') )
paths.settings_paths = ( paths.site_config_path / "settings.toml", paths.user_config_path / "settings.toml" )


class LoggingSettings(BaseSettings):
        log_level: str = 'INFO'
        log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        log_date_format: str = '%Y-%m-%d %H:%M:%S'


class BaseCLISettings(BaseSettings):

    model_config = SettingsConfigDict(env_prefix='TS_', 
                                      case_sensitive=False,
                                      env_nested_delimiter='__',
                                      env_file=(str(p) for p in paths.env_paths if p.exists()),
                                      secrets_dir=(str(p) for p in paths.secrets_paths if p.exists()),
                                      toml_file=(str(p) for p in paths.settings_paths if p.exists()),
                                      extra='allow'
                                      )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls),
            )

    debug: bool = False
    testing: bool = False
    logging: LoggingSettings = LoggingSettings()

extra_settings = {}

for plugin in entry_points(group='tubescience.settings'):
    setting = plugin.load()
    if isinstance(setting, dict):
         extra_settings.update(setting)
    elif isinstance(setting, tuple):
        extra_settings[plugin.name] = setting

Settings = create_model(
     'Settings',
     __base__=BaseCLISettings, 
     **extra_settings,
     )
