from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    password: str = ...
    user: str = ...
    db_name: str = ...
    port: int = ...
    host: str = ...
    model_config: str = SettingsConfigDict(env_prefix='content_postgres_')

    @property
    def adsn(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'
    
    @property
    def dsn(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'


class RedisSettings(BaseSettings):
    host: str = ...
    port: int = ...
    model_config: str = SettingsConfigDict(env_prefix='redis_')

    @property
    def dsn(self):
        return f"redis://{self.host}:{self.port}"


class Hasher(BaseSettings):
    algorithm: str = ...
    rounds: int = ...

    model_config: str = SettingsConfigDict(env_prefix='hasher_')


class Auth(BaseSettings):
    secret_key: str = ...
    algorithm: str = ...
    private_key: str = ...
    model_config: str = SettingsConfigDict(env_prefix='auth_')


class PlayMobile(BaseSettings):
    url: str = ...
    username: str = ...
    password: str = ...
    originator: str = ...
    model_config: str = SettingsConfigDict(env_prefix='playmobile_')


class Settings(BaseSettings):
    project_name: str = "LMS API"
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
    auth: Auth = Auth()
    hasher: Hasher = Hasher()
    sms_broker: PlayMobile = PlayMobile()
