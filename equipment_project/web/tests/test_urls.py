from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from equipments.models import (
    Equipment,
    Document,
)
from web.tests.core import *

User = get_user_model()


class EquipmentURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.staff_user = User.objects.create_user(
            username=USER_NAME_STAFF,
            is_staff=True
        )
        cls.non_staff_user = User.objects.create_user(
            username=USER_NAME_NON_STAFF,
            is_staff=False
        )
        cls.document_manual = Document.objects.create(
            name=DOCUMENT_MANUAL_NAME
        )
        cls.equipment = Equipment.objects.create(
            inventory=INVENTORY_NUM_FIRST,
            name=EQUIPMENT_NAME_FIRST,
            type=EQUIPMENT_TYPE_FIRST,
            model=EQUIPMENT_MODEL_FIRST,
            manufacturer=MANUFACTURER_FIRST,
            nomenclature_key=NOMENCLATURE_KEY_FIRST,
            document_path=DOCUMENT_PATH_FIRST,
            creator=EquipmentURLTests.staff_user
        )
        EquipmentURLTests.equipment.documents.set(
            (EquipmentURLTests.document_manual,)
        )
        cls.pages = (
            '/',
            f'/rent_create/{EquipmentURLTests.equipment.id}/',
            f'/equipment_get/{EquipmentURLTests.equipment.id}/',
            '/equipment_create/',
            f'/equipment_edit/{EquipmentURLTests.equipment.id}/',
            f'/attestation_create/{EquipmentURLTests.equipment.id}/',
            f'/calibration_create/{EquipmentURLTests.equipment.id}/',
            f'/movement_create/{EquipmentURLTests.equipment.id}/',
        )

    def setUp(self):
        self.authorized_staff_user = Client()
        self.authorized_staff_user.force_login(self.staff_user)
        self.authorized_non_staff_user = Client()
        self.authorized_non_staff_user.force_login(self.non_staff_user)
        self.guest_client = Client()

    def test_page_guest_exists(self):
        """Проверяем статус код страниц от
        лица пользователя без права доступа сотрудника и с правами доступа."""
        for address in self.pages:
            with self.subTest(address=address):
                response = self.authorized_non_staff_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
                response = self.authorized_staff_user.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_staff_url_template_tests(self):
        """Проверяем соответствие адреса и шаблона страницы."""
        page_dict = {
            '/':
                'equipments/index.html',
            f'/rent_create/{self.equipment.id}/':
                'equipments/create_form.html',
            f'/equipment_get/{self.equipment.id}/':
                'equipments/index.html',
            '/equipment_create/':
                'equipments/create_form.html',
            f'/equipment_edit/{self.equipment.id}/':
                'equipments/create_form.html',
            f'/attestation_create/{self.equipment.id}/':
                'equipments/create_form.html',
            f'/calibration_create/{self.equipment.id}/':
                'equipments/create_form.html',
            f'/movement_create/{self.equipment.id}/':
                'equipments/create_form.html',
            '/unexisting_page/': 'core/404.html',
        }
        for address, template in page_dict.items():
            with self.subTest(address=address):
                response = self.authorized_staff_user.get(address)
                self.assertTemplateUsed(response, template)

    def test_not_staff_url_template_tests(self):
        """Проверяем шаблон страницы для авторазизованного пользователя
        не являющегося персоналом."""
        for address in self.pages:
            with self.subTest(address=address):
                response = self.authorized_non_staff_user.get(
                    address,
                    follow=True
                )
                self.assertTemplateUsed(response, 'core/403csrf.html')

    def test_page_guest_redirect(self):
        """Проверяем адрес переадресации при попытке от неавторизованного
        пользователя зайти на страницу сайта."""
        for address in self.pages:
            with self.subTest(address=address):
                response = self.guest_client.get(address, follow=True)
                self.assertRedirects(response, '/auth/login/?next=' + address)
