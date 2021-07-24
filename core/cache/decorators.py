from django.core.cache import cache
from typing import TypeVar, Type
from .base import BaseCacheManager


ManagerType = TypeVar("ManagerType", bound=BaseCacheManager)


def post_create_clear_cache(key: str):
    """ 
    removes the cache after object creation 
    """
    def post_save(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            cache.delete(key)
        return wrapper
    return post_save


def post_update_clear_cache(manager: Type[ManagerType]):
    """ 
    removes the cache after object creation 
    """
    def post_save(func):
        def wrapper(*args, **kwargs):
            output = func(*args, **kwargs)
            list_key = manager.get_list_cache_key()
            detail_key = manager.get_detail_cache_key(output.id)
            cache.delete_many([list_key, detail_key])
        return wrapper
    return post_save
