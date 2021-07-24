from core.cache.base import BaseCacheManager
from .models import User


class UserCacheManager(BaseCacheManager[User]):
    """ User Cache Manager """
    
    cached_related_objects = ["section", "role", "work_group", "bank"]
    cached_prefetch_related_objects = ["permissions"]


user_cache_manager = UserCacheManager(model=User)