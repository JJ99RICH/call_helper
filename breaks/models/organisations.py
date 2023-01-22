from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()  # Получили модель пользователя


class Organization(models.Model):
    name = models.CharField(verbose_name='Организация', max_length=255)
    director = models.ForeignKey(verbose_name='Директор', to=User, on_delete=models.RESTRICT,
                                 related_name='organisation_directors')
    employees = models.ManyToManyField(verbose_name='Сотрудники', to=User, related_name='organization_employees',
                                       blank=True)

    # related_name - для того чтобы можно было посмотреть все организации Директора
    # Теперь чтобы узнать все организации Директора - User.objects.organisations_directors.all()
    def __str__(self):
        return f'{self.name} ({self.pk})'

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ('name',)




