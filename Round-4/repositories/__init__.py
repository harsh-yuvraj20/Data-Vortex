"""Repositories package initialization."""
try:
    from repositories.sqlite_repository import SQLiteRepository, get_sqlite_repo, run_cached_query
    from repositories.dataset_repository import DatasetRepository, get_dataset_repo
    from repositories.model_repository import ModelRepository, get_model_repo
except ImportError:
    from .sqlite_repository import SQLiteRepository, get_sqlite_repo, run_cached_query
    from .dataset_repository import DatasetRepository, get_dataset_repo
    from .model_repository import ModelRepository, get_model_repo
