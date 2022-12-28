from django import (
    forms,
)
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
    EQUIPMENT_MODEL_FIRST,
    EQUIPMENT_NAME_FIRST,
    INVENTORY_NUM_FIRST,
    MASS_EQUIPMENT_DOCUMENT_PATH,
    MASS_EQUIPMENT_MODEL,
    MASS_EQUIPMENT_NAME,
    MASS_EQUIPMENT_NOMENCLATURE_KEY,
    NOMENCLATURE_KEY_FIRST,
    USER_NAME_STAFF,
)
from web.utils import (
    COUNT_OF_EQUIPMENT,
)

User = get_user_model()


class EquipmentPagesTests(TestCase):
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
        cls.mass_equipments = [
            Equipment(
                inventory=count,
                name=MASS_EQUIPMENT_NAME + str(count),
                model=MASS_EQUIPMENT_MODEL,
                nomenclature_key=MASS_EQUIPMENT_NOMENCLATURE_KEY,
                document_path=MASS_EQUIPMENT_DOCUMENT_PATH,
                creator=EquipmentPagesTests.staff_user
            ) for count in range(COUNT_OF_EQUIPMENT)
        ]
        Equipment.objects.bulk_create(EquipmentPagesTests.mass_equipments)
        cls.first_mass_equipment = Equipment.objects.all().first()
        cls.equipment = Equipment.objects.create(
            inventory=INVENTORY_NUM_FIRST,
            name=EQUIPMENT_NAME_FIRST,
            model=EQUIPMENT_MODEL_FIRST,
            nomenclature_key=NOMENCLATURE_KEY_FIRST,
            document_path=DOCUMENT_PATH_FIRST,
            creator=EquipmentPagesTests.staff_user
        )
        cls.pages = (
            '/',
            f'/equipment_get/{EquipmentPagesTests.equipment.id}/',
            '/equipment_create/',
            f'/equipment_edit/{EquipmentPagesTests.equipment.id}/',
            f'/movement_create/{EquipmentPagesTests.equipment.id}/',
        )
        cls.movement_first = Movement.objects.create(
            date=DATE_MAY,
            destination=EquipmentPagesTests.destination_first,
            equipment=EquipmentPagesTests.equipment,
            creator=EquipmentPagesTests.staff_user
        )
        cls.movement_second = Movement.objects.create(
            date=DATE_AUGUST,
            destination=EquipmentPagesTests.destination_second,
            equipment=EquipmentPagesTests.equipment,
            creator=EquipmentPagesTests.staff_user
        )

    def setUp(self):
        self.authorized_staff_user = Client()
        self.authorized_staff_user.force_login(self.staff_user)
        self.equipment_count = Equipment.objects.count()
        self.movement_count = Movement.objects.count()

    def test_pre_filled_data_count(self):
        """Проверяем количество созданных объектов"""
        counter = {
            self.equipment_count: 101,
            self.movement_count: 2
        }
        for fact_count, expected_count in counter.items():
            with self.subTest(fact_count=fact_count):
                self.assertEqual(fact_count, expected_count)

    def test_pages_used_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        page_dict = {
            reverse('web:index'): 'equipments/index.html',

            reverse(
                'web:equipment_create'
            ): 'equipments/create_form.html',
            reverse(
                'web:equipment_edit',
                kwargs={'equipment_id': EquipmentPagesTests.equipment.id}
            ): 'equipments/create_form.html',
            reverse(
                'web:movement_create',
                kwargs={'equipment_id': EquipmentPagesTests.equipment.id}
            ): 'equipments/create_form.html',
        }
        for reverse_name, template in page_dict.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_staff_user.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_paginator_pages_contains_count_records(self):
        """Тест на проверку искомого количества постов на
        первой и второй страницах пагинатора."""
        equipment_count_on_second_page = 1
        page_dict = {
            reverse('web:index'): COUNT_OF_EQUIPMENT,
            reverse('web:index') + '?page=2': equipment_count_on_second_page,
        }
        for reverse_name, count in page_dict.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_staff_user.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), count)

    def test_pages_on_equipment_contains_context(self):
        """Шаблон index сформирован из контекста, являющегося списком,
        первый элемент которого - Equipment."""
        form_fields_list = [
            reverse('web:index'),
        ]
        for value in form_fields_list:
            with self.subTest(value=value):
                response = self.authorized_staff_user.get(
                    value)
                form_field = response.context.get('page_obj')[0]
                self.assertIsInstance(form_field, Equipment)

    def test_index_page_show_correct_context(self):
        """Страница index сформирована с правильным контекстом и
         сортировкой."""
        response = self.authorized_staff_user.get(reverse('web:index'))
        first_object, second_object, *_ = response.context.get('page_obj')
        post_dict = {
            first_object: EquipmentPagesTests.equipment,
            second_object: EquipmentPagesTests.first_mass_equipment
        }
        for equipment_obj, expected_value in post_dict.items():
            with self.subTest(equipment_obj=equipment_obj):
                self.assertEqual(equipment_obj, expected_value)

    def test_index_page_show_correct_context_filter(self):
        """Страница index сформированы с правильным контекстом c фильтром."""
        response = self.authorized_staff_user.get(
            reverse('web:index') + "/?inventory=1&name=mass_equipment_name"
        )
        equipments = Equipment.objects.filter(
            inventory__icontains='1',
            name__icontains='mass_equipment_name'
        ).all()
        self.assertEqual(
            tuple(equipments),
            tuple(response.context.get('page_obj'))
        )

    def test_equipment_edit_page_contains_correct_fields(self):
        """Шаблон equipment_edit сформирован с правильными полями."""
        response = (
            self.authorized_staff_user.get(
                reverse(
                    'web:equipment_edit',
                    kwargs={'equipment_id': EquipmentPagesTests.equipment.id}
                )
            )
        )
        fields_dict = {
            'inventory': forms.fields.CharField,
            'name': forms.fields.CharField,
            'model': forms.fields.CharField,
            'nomenclature_key': forms.fields.IntegerField,
            'document_path': forms.fields.CharField,
        }
        for field, class_name in fields_dict.items():
            with self.subTest(reverse_name=field):
                self.assertIsInstance(
                    response.context.get(
                        'form'
                    ).fields.get(field),
                    class_name
                )

    def test_equipment_edit_page_is_edit_true(self):
        """Шаблон equipment_edit сформирован с параметром is_edit == True."""
        context_dict = {
            reverse(
                'web:equipment_edit',
                kwargs={'equipment_id': EquipmentPagesTests.equipment.id}
            ): True,
            reverse('web:equipment_create'): None,
        }
        for reverse_name, value in context_dict.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_staff_user.get(reverse_name)
                self.assertIs(response.context.get('is_edit'), value)

    def test_equipment_id_is_true(self):
        """Шаблон equipment_edit сформирован с правильным id."""
        response = (
            self.authorized_staff_user.get(
                reverse(
                    'web:equipment_edit',
                    kwargs={'equipment_id': EquipmentPagesTests.equipment.id}
                )
            ).context.get('form').instance
        )
        self.assertEqual(response, EquipmentPagesTests.equipment)

    def test_comment_post_page(self):
        """Страница equipment_get отображает внесенные связанные данные по
         оборудованию (rents, attestations, calibrations)."""
        response = (
            self.authorized_staff_user.get(
                reverse(
                    'web:equipment_get',
                    kwargs={'equipment_id': EquipmentPagesTests.equipment.id}
                )
            )
        )
        self.assertEqual(
            len(response.context.get('page_obj')),
            1,
        )
