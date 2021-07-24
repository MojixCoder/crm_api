from typing import Any, List,  Dict, Optional, TypeVar, Type, Generic, Union

from django.core.cache import cache
from django.db.models import QuerySet, Model


ModelType = TypeVar("ModelType", bound=Model)

class BaseCacheManager(Generic[ModelType]):
    
    cache_key: Optional[str] = None
    cached_related_objects: Optional[List[str]] = None
    cached_prefetch_related_objects: Optional[List[str]] = None
    list_timeout: Optional[int] = 86400 # Equals to 1 day
    detail_timeout: Optional[int] = 60
    
    
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model
    
    
    def _get_lower_model_name(self) -> str:
        return self.model.__name__.lower()
    
    
    def get_list_cache_key(self) -> str:
        if self.cache_key:
            return self.cache_key
        self.cache_key = self._get_lower_model_name()
        return self.cache_key
    
    
    def get_detail_cache_key(self, unique_identifier: Union[int, str]) -> str:
        return f"{self._get_lower_model_name()}_{unique_identifier}"
    
    
    def get_all(self) -> QuerySet[ModelType]:
        """
        Returns all instances stored in memory
        """
        cache_key = self.get_list_cache_key()
        
        if self.cached_related_objects:
            queryset = cache.get_or_set(
                cache_key,
                self.model.objects.select_related(*self.cached_related_objects).all(),
                timeout=self.list_timeout,
            )
        else:
            queryset = cache.get_or_set(
                cache_key,
                self.model.objects.all(),
                timeout=self.list_timeout,
            )
        
        return queryset
    
    
    def filter_queryset(self, options: Dict[str, Any]) -> QuerySet[ModelType]:
        """
        Returns filtered instances stored in memory
        """
        queryset = self.get_all()
        queryset = queryset.filter(**options)
        return queryset
    
    
    def get(self, key: str, value: Union[str, int]) -> ModelType:
        """
        Returns object instance stored in memory
        """
        try:
            dict_ = {key: value}
            obj = cache.get(self.get_detail_cache_key(value))
            if obj:
                return obj
            else:
                obj = self.model.objects.get(**dict_)
                if self.cached_related_objects and self.cached_prefetch_related_objects:
                    obj = self.model.objects.select_related(
                        *self.cached_related_objects
                    ).prefetch_related(*self.cached_prefetch_related_objects).get(**dict_)
                elif self.cached_related_objects:
                    obj = self.model.objects.select_related(*self.cached_related_objects).get(**dict_)
                elif self.cached_prefetch_related_objects:
                    obj = self.model.objects.prefetch_related(*self.cached_prefetch_related_objects).get(**dict_)
                cache.set(
                    self.get_detail_cache_key(value),
                    obj,
                    timeout=self.detail_timeout,
                )
        except self.model.DoesNotExist:
            obj = None
        return obj
        