from users.models import Users

from repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = Users
