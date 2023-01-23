from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseDictModelMixin(models.Model):
    code = models.CharField(max_length=16, verbose_name='Код', primary_key=True)
    name = models.CharField(verbose_name='Название', max_length=32)
    sort = models.PositiveSmallIntegerField(verbose_name='Сортировка', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активность', default=True)

    def __str__(self):
        return f'({self.code}) {self.name}'

    class Meta:
        abstract = True   # Так как мы создали этот класс для того чтобы наследоваться и переиспользовать код значит
        ordering = ('-sort',)   # этот класс не должен мигрировать в бд
