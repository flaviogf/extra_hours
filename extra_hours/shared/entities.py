import uuid

from pyflunt.notifications import Notifiable


class Entity(Notifiable):
    def __init__(self, uid=None):
        super().__init__()

        self._uid = uid or str(uuid.uuid4())

    @property
    def uid(self):
        return self._uid
