from django.contrib.auth import get_user_model
from django.db import models

from breaks.constants1 import BREAK_CREATED_STATUS, BREAK_CREATED_DEFAULT
from breaks.models.dicts import BreakStatus
from breaks.models.groups import Group
from breaks.models.replacements import Replacement

User = get_user_model()


class Break(models.Model):
    replacement = models.ForeignKey(to=Replacement, on_delete=models.CASCADE, related_name='breaks',
                                    verbose_name='Смена')
    employee = models.ForeignKey(verbose_name='Сотрудник', to=User, related_name='breaks',
                                 blank=True, on_delete=models.CASCADE)
    break_start = models.TimeField(verbose_name='Начало обеда', null=True, blank=True)
    break_end = models.TimeField(verbose_name='Конец обеда', null=True, blank=True)
    status = models.ForeignKey(to=BreakStatus, on_delete=models.RESTRICT, verbose_name='Статус', blank=True)

    break_max_duration = models.PositiveSmallIntegerField(verbose_name='Максимальная длительность обеда', null=True,
                                                          blank=True)

    def __str__(self):
        return f'Обед пользователя ({self.employee}) для {self.pk}'

    class Meta:
        verbose_name = 'Обеденные перерыв'
        verbose_name_plural = 'Обеденные перерывы'
        ordering = ('-replacement__date', 'break_start')   # Благодаря такой записи переходим в модель replacement.date

    def save(self, *args, **kwargs):
        if not self.pk:
            status, created = BreakStatus.objects.get_or_create(   # если у нас такого статуса не было, он будет создан
                code=BREAK_CREATED_STATUS, defaults=BREAK_CREATED_DEFAULT)
            self.status = status
        return super(Break, self).save(*args, **kwargs)


