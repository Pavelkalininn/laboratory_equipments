from django.contrib.auth import (
    get_user_model,
)
from django.test import (
    TestCase,
)
from equipments.models import (
    Destination,
    Equipment,
    Movement,
)
from web.tests.const import (
    DATE_MAY,
    DESTINATION_ADDRESS_FIRST,
    DESTINATION_ADDRESS_SECOND,
    DOCUMENT_PATH_FIRST,
    EMAIL_NON_STAFF,
    EQUIPMENT_MODEL_FIRST,
    EQUIPMENT_NAME_FIRST,
    INVENTORY_NUM_FIRST,
    NOMENCLATURE_KEY_FIRST,
    USER_NAME_NON_STAFF,
    USER_NAME_STAFF,
)

User = get_user_model()


class EquipmentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.staff_user = User.objects.create_user(
            username=USER_NAME_STAFF,
            is_staff=True
        )
        cls.non_staff_user = User.objects.create_user(
            username=USER_NAME_NON_STAFF,
            email=EMAIL_NON_STAFF,
            is_staff=False
        )
        cls.destination_first = Destination.objects.create(
            address=DESTINATION_ADDRESS_FIRST
        )
        cls.destination_second = Destination.objects.create(
            address=DESTINATION_ADDRESS_SECOND
        )

    def setUp(self):
        self.equipment = Equipment.objects.create(
            inventory=INVENTORY_NUM_FIRST,
            name=EQUIPMENT_NAME_FIRST,
            model=EQUIPMENT_MODEL_FIRST,
            nomenclature_key=NOMENCLATURE_KEY_FIRST,
            document_path=DOCUMENT_PATH_FIRST,
            creator=self.staff_user
        )
        self.movement = Movement.objects.create(
            date=DATE_MAY,
            early=False,
            late=False,
            recipient=EquipmentModelTest.non_staff_user,
            destination=self.destination_first,
            equipment=self.equipment,
            creator=self.staff_user
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        field_values = {
            self.equipment: EQUIPMENT_NAME_FIRST,
            self.movement:
                f'По адресу {DESTINATION_ADDRESS_FIRST} с {DATE_MAY}',
        }
        for field, expected_value in field_values.items():
            with self.subTest(field=field):
                self.assertEqual(
                    str(field), expected_value)
