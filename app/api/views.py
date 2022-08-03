import operator

from flask_caching import Cache
from flask_resty import ColumnFilter, Filtering, GenericModelView, NoOpAuthentication, NoOpAuthorization, Sorting

from . import models, schemas
from .pagination import CustomCursorPagination

# Cache initialization
cache = Cache()


class UserViewBase(GenericModelView):
    """UserViewBase

    GenericModelView for User objects. Include
    pagination, sorting, filtering
    """

    model = models.User
    schema = schemas.UserSchema()

    authentication = NoOpAuthentication()
    authorization = NoOpAuthorization()

    pagination = CustomCursorPagination(max_limit=10000)
    sorting = Sorting("id", default="id")
    filtering = Filtering(
        id=ColumnFilter(operator.eq),
        email=ColumnFilter(operator.eq),
        first_name=ColumnFilter(operator.eq),
        last_name=ColumnFilter(operator.eq),
        created=ColumnFilter(operator.eq),
        updated=ColumnFilter(operator.eq),
    )


class UserListView(UserViewBase):
    """UserListView

    UserViewBase for a list of User objects.
    Include get()
    """

    @cache.cached(timeout=60, query_string=True)
    def get(self):
        """List of User objects.

        Returns:
            A 200 HTTP Response and a list of users
        """
        return self.list()
