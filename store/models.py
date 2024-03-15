"""
    Module name :- models
"""

import random
from datetime import date, timedelta, datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


# Create your models here.
class EquipmentType(models.Model):
    """
    Equipment Type Model.
    """

    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=3, unique=True)
    threshold = models.IntegerField(default=10)
    slug = models.SlugField(blank=True, unique=True)

    @property
    def get_remaining_equipments(self):
        """
        Get total equipments.
        """
        return len(Equipment.get_non_assigned_equipments(self))

    @classmethod
    def create_random_equipment_types(cls):
        """
        Create random equipment types.
        """
        equipment_types = [
            "Laptop",
            "Monitor",
            "Keyboard",
            "Mouse",
            "Speaker",
            "CPU",
            "Headphones",
            "Support Stand",
            "Adapters",
            "Power Bank",
            "Memory",
        ]

        equipment_type_list = []

        for equipment_type in equipment_types:
            print(equipment_type)
            instance = cls(name=equipment_type, abbreviation=equipment_type[:3])
            instance.slug = slugify(instance.name)
            equipment_type_list.append(instance)

        cls.objects.bulk_create(equipment_type_list)

    def save(self, *args, **kwargs):
        """
        save method
        """
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String Representation.
        """
        return f"{self.name}"


class Equipment(models.Model):
    """
    Equipment Model.
    """

    label = models.CharField(max_length=10)
    serial_number = models.CharField(max_length=20)
    model_number = models.CharField(max_length=20)
    brand = models.CharField(max_length=30)
    price = models.FloatField()
    buy_date = models.DateField()
    equipment_type = models.ForeignKey(
        EquipmentType, on_delete=models.CASCADE, related_name="equipment"
    )
    under_repair = models.BooleanField(default=False)
    functional = models.BooleanField(default=True)
    slug = models.SlugField(blank=True, unique=True)

    @property
    def set_label(self):
        """
        Automatically set label.
        """
        try:
            temp_id = list(self.equipment_type.equipment.all())[-1]
            count = int(temp_id.label[4:]) + 1
        except IndexError:
            count = 1
        return f"{self.equipment_type.abbreviation}-{count:0>6}"

    @property
    def get_current_user(self):
        """
        Get current user for equipment.
        """
        allocations = list(self.allocation.all())
        if allocations:
            return allocations[-1].user if not allocations[-1].returned else "No User"
        return "No User"

    @property
    def get_all_users(self):
        """
        Get all users used the equipment.
        """
        return [allocation.user for allocation in self.allocation.all()][::-1]

    @classmethod
    def get_all_functional_equipments(cls, equipment_type):
        """
        Get Functional Equipments.
        """
        return cls.objects.filter(
            equipment_type=equipment_type, functional=True, under_repair=False
        )

    @classmethod
    def get_under_repair_equipments(cls, equipment_type):
        """
        Get under repaired equipments.
        """
        return cls.objects.filter(
            equipment_type=equipment_type, functional=True, under_repair=True
        )

    @classmethod
    def get_assigned_equipments(cls, equipment_type):
        """
        Get assigned equipments.
        """
        equipments = cls.objects.filter(
            equipment_type=equipment_type, functional=True, under_repair=False
        )
        assigned_equipments = []

        for equipment in equipments:
            allocations = equipment.allocation.all()
            if not allocations:
                continue

            last_allocation = list(allocations)[-1]
            if not last_allocation.returned:
                assigned_equipments.append(equipment)

        return assigned_equipments

    @classmethod
    def get_non_assigned_equipments(cls, equipment_type):
        """
        Get non-assigned equipments.
        """
        equipments = cls.objects.filter(
            equipment_type=equipment_type, functional=True, under_repair=False
        )
        non_assigned_equipments = []

        for equipment in equipments:
            allocations = equipment.allocation.all()
            if not allocations:
                non_assigned_equipments.append(equipment)
                continue

            last_allocation = list(allocations)[-1]
            if last_allocation.returned:
                non_assigned_equipments.append(equipment)

        return non_assigned_equipments

    @classmethod
    def get_ids(cls, equipment_type):
        """
        Get equipment ids.
        """
        return [
            (equipment.pk, equipment.label)
            for equipment in cls.get_non_assigned_equipments(equipment_type)
        ]

    @classmethod
    def create_random_equipments(cls):
        """
        Create random equipments.
        """
        equipment_types = list(EquipmentType.objects.all())
        functionality = [True, False]
        serial_numbers = [
            f"{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
            for _ in range(1000)
        ]
        model_numbers = [f"Model-{number}" for number in serial_numbers]
        buy_dates = [date.today() - timedelta(days=x) for x in range(40)]
        brands = [
            "Samsung",
            "Nokia",
            "Microsoft",
            "Apple",
            "Logitech",
            "Dell",
            "Asus",
            "Xiaomi",
            "Nothing",
            "HP",
        ]

        for _ in range(10000):
            instance = cls(
                buy_date=random.choice(buy_dates),
                price=random.randint(1000, 10000),
                serial_number=random.choice(serial_numbers),
                model_number=random.choice(model_numbers),
                equipment_type=random.choice(equipment_types),
                functional=random.choice(functionality),
                brand=random.choice(brands),
            )
            instance.label = instance.set_label
            instance.slug = slugify(instance.label)
            instance.save()

    def save(self, *args, **kwargs):
        """
        save method.
        """
        if not self.label:
            self.label = self.set_label
        self.slug = slugify(self.label)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String Representation.
        """
        return self.label


class Allocation(models.Model):
    """
    Allocation data model.
    """

    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name="allocation"
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    allocated_date = models.DateField(auto_now_add=True)
    release_date = models.DateField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    returned = models.BooleanField(default=False)

    @classmethod
    def get_non_returned_allocations(cls):
        """
        Get non-returned euipments.
        """
        return cls.objects.filter(returned=False)

    @classmethod
    def create_random_allocations(cls):
        """
        Create fake allocation.
        """
        users = list(get_user_model().objects.all())
        equipments = list(Equipment.objects.all())
        returned = [True, False]

        allocation_list = []

        for _ in range(10000):
            allocation = cls(
                user=random.choice(users),
                equipment=random.choice(equipments),
                returned=random.choice(returned),
            )
            allocation.slug = slugify(
                f"{allocation.user}-{allocation.equipment}-{datetime.now()}"
            )

            allocation_list.append(allocation)

        cls.objects.bulk_create(allocation_list)

    def save(self, *args, **kwargs):
        """
        save method.
        """
        if self.returned:
            self.release_date = date.today()

        self.slug = slugify(f"{self.user}-{self.equipment}-{datetime.now()}")

        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation.
        """
        return f"{self.equipment} - {self.user}"
