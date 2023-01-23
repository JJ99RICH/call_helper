from django.contrib.auth import get_user_model
from django.db import models

from breaks.models.dicts import ReplacementStatus
from breaks.models.groups import Group

User = get_user_model()


class Replacement(models.Model):
    group = models.ForeignKey(verbose_name='Группа', to=Group, on_delete=models.CASCADE, related_name='replacements')
    date = models.DateField(verbose_name='Дата смены')
    break_start = models.TimeField(verbose_name='Начало смены')
    break_end = models.TimeField(verbose_name='Конец смены')
    break_max_duration = models.PositiveSmallIntegerField(verbose_name='Макс. продолжительность обеда')

    def __str__(self):
        return f'Смена №({self.pk}) для {self.group}'

    class Meta:
        verbose_name = 'Смена'
        verbose_name_plural = 'Смены'
        ordering = ('-date',)


class ReplacementEmployee(models.Model):
    employee = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='replacements',
                                 verbose_name='Сотрудник')
    replacement = models.ForeignKey(to=Replacement, on_delete=models.CASCADE, related_name='employees',
                                    verbose_name='Смена')
    status = models.ForeignKey(to=ReplacementStatus, on_delete=models.RESTRICT, related_name='replacement_employees',
                               verbose_name='Статус')

    def __str__(self):
        return f'({self.replacement}) {self.employee}'

    class Meta:
        verbose_name = 'Смена - Работник'
        verbose_name_plural = 'Смены Работники'
