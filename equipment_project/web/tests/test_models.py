from django.contrib.auth import get_user_model
from django.test import TestCase
from equipments.models import (Attestation, Calibration, Destination, Document,
                               Equipment, Movement, Organization, Rent)
from web.tests.const import (ATTESTATION_NAME_FIRST, CALIBRATION_NAME_FIRST,
                             DATE_JANUARY, DATE_MARCH, DATE_MAY,
                             DESTINATION_ADDRESS_FIRST,
                             DESTINATION_ADDRESS_SECOND,
                             DOCUMENT_DESCRIPTION_NAME, DOCUMENT_MANUAL_NAME,
                             DOCUMENT_PATH_FIRST, EQUIPMENT_MODEL_FIRST,
                             EQUIPMENT_NAME_FIRST,
                             EQUIPMENT_SERIAL_NUMBER_FIRST,
                             FIRST_ORGANIZATION_NAME, INVENTORY_NUM_FIRST,
                             MANUFACTURER_FIRST, NOMENCLATURE_KEY_FIRST,
                             SECOND_ORGANIZATION_NAME, USER_NAME_STAFF)

User = get_user_model()


class EquipmentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.staff_user = User.objects.create_user(
            username=USER_NAME_STAFF,
            is_staff=True
        )
        cls.document_manual = Document.objects.create(
            name=DOCUMENT_MANUAL_NAME
        )
        cls.document_description = Document.objects.create(
            name=DOCUMENT_DESCRIPTION_NAME
        )
        cls.organization_first = Organization.objects.create(
            name=FIRST_ORGANIZATION_NAME
        )
        cls.organization_second = Organization.objects.create(
            name=SECOND_ORGANIZATION_NAME
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
            serial_number=EQUIPMENT_SERIAL_NUMBER_FIRST,
            model=EQUIPMENT_MODEL_FIRST,
            manufacturer=MANUFACTURER_FIRST,
            nomenclature_key=NOMENCLATURE_KEY_FIRST,
            document_path=DOCUMENT_PATH_FIRST,
            creator=self.staff_user
        )
        self.equipment.documents.set(
            (self.document_manual, self.document_description)
        )
        self.rent = Rent.objects.create(
            owner=self.organization_first,
            renter=self.organization_second,
            date=DATE_JANUARY,
            equipment=self.equipment,
            creator=self.staff_user
        )
        self.attestation = Attestation.objects.create(
            name=ATTESTATION_NAME_FIRST,
            date=DATE_JANUARY,
            validity_period=DATE_MAY,
            equipment=self.equipment,
            creator=self.staff_user
        )
        self.calibration = Calibration.objects.create(
            name=CALIBRATION_NAME_FIRST,
            date=DATE_JANUARY,
            validity_period=DATE_MARCH,
            equipment=self.equipment,
            creator=self.staff_user
        )
        self.movement = Movement.objects.create(
            date=DATE_MAY,
            destination=self.destination_first,
            equipment=self.equipment,
            creator=self.staff_user
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        field_values = {
            self.equipment: EQUIPMENT_NAME_FIRST,
            self.rent:
                f'В аренде у {SECOND_ORGANIZATION_NAME} с {DATE_JANUARY}, '
                f'владелец {FIRST_ORGANIZATION_NAME}',
            self.attestation: f'{ATTESTATION_NAME_FIRST} от {DATE_JANUARY}, '
                              f'действует до {DATE_MAY}',
            self.calibration: f'{CALIBRATION_NAME_FIRST} от {DATE_JANUARY}, '
                              f'действует до {DATE_MARCH}',
            self.movement:
                f'По адресу {DESTINATION_ADDRESS_FIRST} с {DATE_MAY}',
            self.document_manual: DOCUMENT_MANUAL_NAME,
            self.organization_first: FIRST_ORGANIZATION_NAME,
        }
        for field, expected_value in field_values.items():
            with self.subTest(field=field):
                self.assertEqual(
                    str(field), expected_value)
