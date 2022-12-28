from django.contrib.auth import (
    get_user_model,
)
from django.test import (
    Client,
    TestCase,
)
from django.urls import (
    reverse,
)
from equipments.models import (
    Destination,
    Equipment,
    Movement,
)
from web.tests.const import (
    DATE_AUGUST,
    DATE_MAY,
    DESTINATION_ADDRESS_FIRST,
    DESTINATION_ADDRESS_SECOND,
    DOCUMENT_PATH_FIRST,
    DOCUMENT_PATH_SECOND,
    EQUIPMENT_MODEL_FIRST,
    EQUIPMENT_MODEL_SECOND,
    EQUIPMENT_NAME_FIRST,
    EQUIPMENT_NAME_SECOND,
    INVENTORY_NUM_FIRST,
    INVENTORY_NUM_SECOND,
    NOMENCLATURE_KEY_FIRST,
    NOMENCLATURE_KEY_SECOND,
    USER_NAME_STAFF,
)

User = get_user_model()


class EquipmentCreateEditFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.staff_user = User.objects.create_user(
            username=USER_NAME_STAFF,
            is_staff=True
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

        self.movement_first = Movement.objects.create(
            date=DATE_MAY,
            destination=self.destination_first,
            equipment=self.equipment,
            creator=self.staff_user
        )
        self.movement_second = Movement.objects.create(
            date=DATE_AUGUST,
            destination=self.destination_second,
            equipment=self.equipment,
            creator=self.staff_user
        )

        self.authorized_staff_user = Client()
        self.authorized_staff_user.force_login(self.staff_user)
        self.equipment_count = Equipment.objects.count()
        self.movement_count = Movement.objects.count()

    def test_create_equipment(self):
        """Валидная форма создает запись Equipment."""
        equipment_form_data = {
            'inventory': INVENTORY_NUM_SECOND,
            'name': EQUIPMENT_NAME_SECOND,
            'model': EQUIPMENT_MODEL_SECOND,
            'nomenclature_key': NOMENCLATURE_KEY_SECOND,
            'document_path': DOCUMENT_PATH_SECOND,
        }
        self.assertEqual(Equipment.objects.count(), self.equipment_count + 1)
        self.assertTrue(
            Equipment.objects.filter(**equipment_form_data).exists()
        )

    def test_create_movement(self):
        movement_form_data = {
            'date': DATE_MAY,
            'destination': self.destination_first.pk,
        }
        response = self.authorized_staff_user.post(
            reverse(
                'web:movement_create',
                kwargs={'equipment_id': self.equipment.pk}
            ),
            data=movement_form_data
        )
        self.assertEqual(
            Movement.objects.count(),
            self.movement_count + 1
        )
        self.assertTrue(
            Movement.objects.filter(
                **movement_form_data,
                equipment=self.equipment,
                creator=self.staff_user.id
            ).exists()
        )

    def test_edit_equipment(self):
        """Валидная форма меняет запись equipment_id в Equipment."""
        equipment_form_data = {
            'inventory': INVENTORY_NUM_SECOND,
            'name': EQUIPMENT_NAME_SECOND,
            'model': EQUIPMENT_MODEL_SECOND,
            'nomenclature_key': NOMENCLATURE_KEY_SECOND,
            'document_path': DOCUMENT_PATH_SECOND,
        }

        response = self.authorized_staff_user.post(
            reverse(
                'web:equipment_edit',
                kwargs={'equipment_id': self.equipment.pk}
            ),
            data=equipment_form_data
        )
        self.assertEqual(Equipment.objects.count(), self.equipment_count)
        self.assertTrue(
            Equipment.objects.filter(
                **equipment_form_data,
                id=self.equipment.pk
            ).exists()
        )
