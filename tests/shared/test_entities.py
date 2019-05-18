import unittest
import uuid

from extra_hours.shared.entities import Entity


class FakeEntity(Entity):
    pass


class EntityTest(unittest.TestCase):
    def test_should_contains_uid_when_entity_is_created(self):
        entity_one = Entity()

        self.assertIsInstance(entity_one.uid, uuid.UUID)

    def test_should_entity_are_equal_when_uid_are_equal(self):
        uid = uuid.uuid4()

        entity_one = Entity(uid=uid)

        entity_two = Entity(uid=uid)

        self.assertEqual(entity_one, entity_two)
