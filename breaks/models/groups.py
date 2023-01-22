from django.contrib.auth import get_user_model
from django.db import models
from breaks.models.organisations import Organization


User = get_user_model()


class Group(models.Model):
    organisation = models.ForeignKey(to=Organization, on_delete=models.CASCADE, related_name='groups',
                                     verbose_name='Организация')
    name = models.CharField(verbose_name='Название', max_length=255)
    manager = models.ForeignKey(verbose_name='Менеджер', to=User, on_delete=models.RESTRICT,
                                related_name='group_managers')
    employees = models.ManyToManyField(verbose_name='Сотрудники', to=User, related_name='group_employees',
                                       blank=True)
    min_active = models.PositiveSmallIntegerField(verbose_name='Минимальное количество активных сотрудников', null=True,
                                                  blank=True)
    break_start = models.TimeField(verbose_name='Начало обеда', null=True, blank=True)
    break_end = models.TimeField(verbose_name='Конец обеда', null=True, blank=True)
    break_max_duration = models.PositiveSmallIntegerField(verbose_name='Максимальная длительность обеда', null=True,
                                                          blank=True)

    def __str__(self):
        return f'{self.name} ({self.pk}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('name',)

    # Organizations.objects.groups.all()

