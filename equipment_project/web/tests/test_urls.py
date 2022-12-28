from http import (
    HTTPStatus,
)

from django.contrib.auth import (
    get_user_model,
)
from django.test import (
    Client,
    TestCase,
)
from equipments.models import (
    Equipment,
)
from web.tests.const import (
    DOCUMENT_PATH_FIRST,
    EQUIPMENT_MODEL_FIRST,
    EQUIPMENT_NAME_FIRST,
    INVENTORY_NUM_FIRST,
    NOMENCLATURE_KEY_FIRST,
    USER_NAME_NON_STAFF,
    USER_NAME_STAFF,
)

User = get_user_model()


class EquipmentURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.staff_user = User.objects.create_user(
            username=USER_NAME_STAFF,
            email='first@mail.ru',
            first_name='staff_name',
            last_name='staff_last_name',
            is_staff=True
        )
        cls.non_staff_user = User.objects.create_user(
            username=USER_NAME_NON_STAFF,
            email='last@mail.ru',
            first_name='non_staff_name',
            last_name='non_staff_last_name',
            is_staff=False
        )
        cls.equipment = Equipment.objects.create(
            inventory=INVENTORY_NUM_FIRST,
            name=EQUIPMENT_NAME_FIRST,
            model=EQUIPMENT_MODEL_FIRST,
            nomenclature_key=NOMENCLATURE_KEY_FIRST,
            document_path=DOCUMENT_PATH_FIRST,
            creator=EquipmentURLTests.staff_user
        )
        cls.pages = (
            '/',
            '/equipment_create/',
            f'/equipment_edit/{EquipmentURLTests.equipment.id}/',
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
            '/equipment_create/':
                'equipments/create_form.html',
            f'/equipment_edit/{self.equipment.id}/':
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
