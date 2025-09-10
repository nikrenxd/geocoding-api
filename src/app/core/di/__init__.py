from .providers import (
    ConfigProvider,
    DatabaseProvider,
    RepositoriesProvider,
    ServicesProvider,
)

providers = [
    DatabaseProvider(),
    ConfigProvider(),
    RepositoriesProvider(),
    ServicesProvider(),
]

__all__ = ["providers"]
