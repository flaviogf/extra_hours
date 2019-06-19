import uuid

from pyflunt.notifications import Notifiable


class Entity(Notifiable):
    def __init__(self, uid=None):
        super().__init__()

        self._uid = uid or str(uuid.uuid4())

    @property
    def uid(self):
        return str(self._uid)

    def __eq__(self, other):
        return self.uid == other.uid
