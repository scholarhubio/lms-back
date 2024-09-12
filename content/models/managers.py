from sqlalchemy.orm import Query


class SoftDeleteQuery(Query):
    """Custom query class to automatically exclude soft-deleted records."""

    def __new__(cls, *args, **kwargs):
        obj = super(SoftDeleteQuery, cls).__new__(cls)
        obj._with_deleted = False
        return obj

    def __init__(self, entities, session=None):
        super().__init__(entities, session)

    def with_deleted(self):
        """Include deleted records in the query results."""
        self._with_deleted = True
        return self

    def __iter__(self):
        print('#####')
        if self._with_deleted == True:
            self._add_is_deleted_filter()
        return super().__iter__()

    def _add_is_deleted_filter(self):
        """Add filter to exclude deleted records."""
        mapper = self._only_full_mapper_zero('get')
        if hasattr(mapper.class_, 'is_deleted'):
            print(mapper.class_)
            self._criterion = self._criterion & (mapper.class_.is_deleted == True)
