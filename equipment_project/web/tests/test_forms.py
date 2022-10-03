from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from equipments.models import (Attestation, Calibration, Destination, Document,
                               Equipment, Movement, Organization, Rent)
from web.tests.core import (ATTESTATION_NAME_FIRST, ATTESTATION_NAME_SECOND,
                            CALIBRATION_NAME_FIRST, CALIBRATION_NAME_SECOND,
                            DATE_AUGUST, DATE_FEBRUARY, DATE_JANUARY,
                            DATE_JUNE, DATE_MARCH, DATE_MAY,
                            DESTINATION_ADDRESS_FIRST,
                            DESTINATION_ADDRESS_SECOND,
                            DOCUMENT_DESCRIPTION_NAME, DOCUMENT_MANUAL_NAME,
                            DOCUMENT_PATH_FIRST, DOCUMENT_PATH_SECOND,
                            EQUIPMENT_MODEL_FIRST, EQUIPMENT_MODEL_SECOND,
                            EQUIPMENT_NAME_FIRST, EQUIPMENT_NAME_SECOND,
                            EQUIPMENT_SERIAL_NUMBER_FIRST,
                            EQUIPMENT_SERIAL_NUMBER_SECOND,
                            FIRST_ORGANIZATION_NAME, INVENTORY_NUM_FIRST,
                            INVENTORY_NUM_SECOND, MANUFACTURER_FIRST,
                            MANUFACTURER_SECOND, NEW_NAME,
                            NOMENCLATURE_KEY_FIRST, NOMENCLATURE_KEY_SECOND,
                            SECOND_ORGANIZATION_NAME, USER_NAME_STAFF)

User = get_user_model()


class EquipmentCreateEditFormTests(TestCase):
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
        self.rent_first = Rent.objects.create(
            owner=self.organization_first,
            renter=self.organization_second,
            date=DATE_JANUARY,
            equipment=self.equipment,
            creator=self.staff_user
        )
        self.rent_second = Rent.objects.create(
            owner=self.organization_first,
            renter=self.organization_second,
            date=DATE_FEBRUARY,
            equipment=self.equipment,
            creator=self.staff_user
        )

        self.attestation_first = Attestation.objects.create(
            name=ATTESTATION_NAME_FIRST,
            date=DATE_JANUARY,
            validity_period=DATE_MARCH,
            equipment=self.equipment,
            creator=self.staff_user
        )
        self.attestation_second = Attestation.objects.create(
            name=ATTESTATION_NAME_SECOND,
            date=DATE_MARCH,
            validity_period=DATE_MAY,
            equipment=self.equipment,
            creator=self.staff_user
        )
        self.calibration_first = Calibration.objects.create(
            name=CALIBRATION_NAME_FIRST,
            date=DATE_JANUARY,
            validity_period=DATE_MARCH,
            equipment=self.equipment,
            creator=self.staff_user
        )
        self.calibration_second = Calibration.objects.create(
            name=CALIBRATION_NAME_SECOND,
            date=DATE_MAY,
            validity_period=DATE_JUNE,
            equipment=self.equipment,
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
        self.rent_count = Rent.objects.count()
        self.attestation_count = Attestation.objects.count()
        self.calibration_count = Calibration.objects.count()
        self.movement_count = Movement.objects.count()

    def test_create_equipment(self):
        """Валидная форма создает запись Equipment."""
        equipment_form_data = {
            'inventory': INVENTORY_NUM_SECOND,
            'name': EQUIPMENT_NAME_SECOND,
            'serial_number': EQUIPMENT_SERIAL_NUMBER_SECOND,
            'model': EQUIPMENT_MODEL_SECOND,
            'manufacturer': MANUFACTURER_SECOND,
            'nomenclature_key': NOMENCLATURE_KEY_SECOND,
            'documents': (
                self.document_manual.id,
                self.document_description.id
            ),
            'document_path': DOCUMENT_PATH_SECOND,
        }
        response = self.authorized_staff_user.post(
            reverse('web:equipment_create'),
            data=equipment_form_data
        )
        self.assertRedirects(
            response,
            reverse(
                'web:rent_create',
                kwargs={'equipment_id': self.equipment.pk + 1}
            )
        )
        self.assertEqual(Equipment.objects.count(), self.equipment_count + 1)
        self.assertTrue(
            Equipment.objects.filter(**equipment_form_data).exists()
        )

    def test_create_rent(self):
        """Валидная форма создает запись Rent."""
        rent_form_data = {
            'owner': self.organization_second.id,
            'renter': self.organization_first.id,
            'date': DATE_MAY
        }
        response = self.authorized_staff_user.post(
            reverse(
                'web:rent_create',
                kwargs={'equipment_id': self.equipment.pk}
            ),
            data=rent_form_data
        )
        self.assertRedirects(
            response,
            reverse(
                'web:attestation_create',
                kwargs={'equipment_id': self.equipment.pk}
            )
        )
        self.assertEqual(Rent.objects.count(), self.rent_count + 1)
        self.assertTrue(
            Rent.objects.filter(
                **rent_form_data,
                equipment=self.equipment,
                creator=self.staff_user.id
            ).exists()
        )

    def test_create_attestation(self):
        attestation_form_data = {
            'name': NEW_NAME,
            'date': DATE_MAY,
            'validity_period': DATE_JUNE,

        }
        response = self.authorized_staff_user.post(
            reverse(
                'web:attestation_create',
                kwargs={'equipment_id': self.equipment.pk}
            ),
            data=attestation_form_data
        )
        self.assertRedirects(
            response,
            reverse(
                'web:calibration_create',
                kwargs={'equipment_id': self.equipment.pk}
            )
        )
        self.assertEqual(
            Attestation.objects.count(),
            self.attestation_count + 1
        )
        self.assertTrue(
            Attestation.objects.filter(
                **attestation_form_data,
                equipment=self.equipment,
                creator=self.staff_user.id
            ).exists()
        )

    def test_create_calibration(self):
        calibration_form_data = {
            'name': NEW_NAME,
            'date': DATE_MAY,
            'validity_period': DATE_JUNE,

        }
        response = self.authorized_staff_user.post(
            reverse(
                'web:calibration_create',
                kwargs={'equipment_id': self.equipment.pk}
            ),
            data=calibration_form_data
        )
        self.assertRedirects(
            response,
            reverse(
                'web:movement_create',
                kwargs={'equipment_id': self.equipment.pk}
            )
        )
        self.assertEqual(
            Calibration.objects.count(),
            self.calibration_count + 1
        )
        self.assertTrue(
            Calibration.objects.filter(
                **calibration_form_data,
                equipment=self.equipment,
                creator=self.staff_user.id
            ).exists()
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
        self.assertRedirects(
            response,
            reverse(
                'web:equipment_get',
                kwargs={'equipment_id': self.equipment.pk}
            )
        )
        self.assertEqual(
            Movement.objects.count(),
            self.calibration_count + 1
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
            'serial_number': EQUIPMENT_SERIAL_NUMBER_SECOND,
            'model': EQUIPMENT_MODEL_SECOND,
            'manufacturer': MANUFACTURER_SECOND,
            'nomenclature_key': NOMENCLATURE_KEY_SECOND,
            'documents': (
                self.document_manual.id,
                self.document_description.id
            ),
            'document_path': DOCUMENT_PATH_SECOND,
        }

        response = self.authorized_staff_user.post(
            reverse(
                'web:equipment_edit',
                kwargs={'equipment_id': self.equipment.pk}
            ),
            data=equipment_form_data
        )
        self.assertRedirects(
            response,
            reverse(
                'web:rent_create',
                kwargs={'equipment_id': self.equipment.pk}
            )
        )
        self.assertEqual(Equipment.objects.count(), self.equipment_count)
        self.assertTrue(
            Equipment.objects.filter(
                **equipment_form_data,
                id=self.equipment.pk
            ).exists()
        )
