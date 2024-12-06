from djing.core.Filters.Filter import Filter

class BooleanFilter(Filter):
    component: str
    def default(self): ...
