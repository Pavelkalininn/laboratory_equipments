import shutil
import tempfile

from django.contrib.auth import (
    get_user_model,
)
from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)
from django.test import (
    Client,
    TestCase,
    override_settings,
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
    EMAIL_NON_STAFF,
    EMAIL_STAFF,
    EQUIPMENT_MODEL_FIRST,
    EQUIPMENT_MODEL_SECOND,
    EQUIPMENT_NAME_FIRST,
    EQUIPMENT_NAME_SECOND,
    INVENTORY_NUM_FIRST,
    INVENTORY_NUM_SECOND,
    NOMENCLATURE_KEY_FIRST,
    NOMENCLATURE_KEY_SECOND,
    USER_NAME_NON_STAFF,
    USER_NAME_STAFF,
)

from equipment_project import (
    settings,
)

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class EquipmentCreateEditFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.staff_user = User.objects.create_user(
            username=USER_NAME_STAFF,
            email=EMAIL_STAFF,
            is_staff=True
        )
        cls.non_staff_user = User.objects.create_user(
            username=USER_NAME_NON_STAFF,
            email=EMAIL_NON_STAFF,
            is_staff=False
        )
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.destination_first = Destination.objects.create(
            address=DESTINATION_ADDRESS_FIRST
        )
        cls.destination_second = Destination.objects.create(
            address=DESTINATION_ADDRESS_SECOND
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.equipment = Equipment.objects.create(
            inventory=INVENTORY_NUM_FIRST,
            name=EQUIPMENT_NAME_FIRST,
            model=EQUIPMENT_MODEL_FIRST,
            manual=EquipmentCreateEditFormTests.uploaded,
            nomenclature_key=NOMENCLATURE_KEY_FIRST,
            document_path=DOCUMENT_PATH_FIRST,
            creator=self.staff_user
        )

        self.movement_first = Movement.objects.create(
            date=DATE_MAY,
            early=False,
            late=False,
            recipient=EquipmentCreateEditFormTests.non_staff_user,
            destination=self.destination_first,
            equipment=self.equipment,
            creator=self.staff_user
        )
        self.movement_second = Movement.objects.create(
            date=DATE_AUGUST,
            early=False,
            late=False,
            recipient=EquipmentCreateEditFormTests.non_staff_user,
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
            'manual': EquipmentCreateEditFormTests.uploaded,
            'nomenclature_key': NOMENCLATURE_KEY_SECOND,
            'document_path': DOCUMENT_PATH_SECOND,
        }
        response = self.authorized_staff_user.post(
            reverse('web:equipment_create'),
            data=equipment_form_data
        )
        self.assertRedirects(
            response,
            reverse(
                'web:movement_create',
                kwargs={'equipment_id': self.equipment.pk + 1}
            )
        )
        self.assertEqual(Equipment.objects.count(), self.equipment_count + 1)
        self.assertTrue(
            Equipment.objects.filter(**equipment_form_data).exists()
        )

    def test_create_movement(self):
        movement_form_data = {
            'destination': self.destination_first.pk,
        }
        self.authorized_staff_user.post(
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
            'manual': EquipmentCreateEditFormTests.uploaded,
            'nomenclature_key': NOMENCLATURE_KEY_SECOND,
            'document_path': DOCUMENT_PATH_SECOND,
        }

        self.authorized_staff_user.post(
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
