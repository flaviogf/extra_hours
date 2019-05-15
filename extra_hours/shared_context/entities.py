import uuid

from pyflunt.notifications import Notifiable


class Entity(Notifiable):
    def __init__(self, uid=None):
        super().__init__()
        self.uid = uid or uuid.uuid4()

    def __eq__(self, other):
        return self.uid == other.uid
