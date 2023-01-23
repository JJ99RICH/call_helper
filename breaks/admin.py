from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from breaks.models import groups
from breaks.models.breaks import Break
from breaks.models.dicts import ReplacementStatus, BreakStatus
from breaks.models.organisations import Organization
from breaks.models.groups import Group
from breaks.models.replacements import Replacement, ReplacementEmployee


# Inlines
class ReplacementEmployeeInline(admin.TabularInline):
    model = ReplacementEmployee
    fields = ('employee', 'status',)


# Models
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director',)
    filter_horizontal = ('employees', )   # Удобное отображение сотрудников, также есть filter_vertical


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'manager', 'min_active', 'replacement_count')
    search_fields = ('name',)

    def replacement_count(self, obj):   # Возвращаем атрибут obj.replacement_count и имя функции нужно писать в поле
        return obj.replacement_count    # отображения

    replacement_count.short_description = 'Количество смен'   # Присвоили имя вычисляемой колонке

    def get_queryset(self, request):                        # Берем queryset назначаем новый атрибут replacement_count
        queryset = groups.Group.objects.annotate(           # В нем же функция которая считает кол-во replacements__id
            replacement_count=Count('replacements__id')
        )
        return queryset


@admin.register(Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'date', 'break_start', 'break_end', 'break_max_duration')
    inlines = (ReplacementEmployeeInline,)
    autocomplete_fields = ('group',)


@admin.register(ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active')


@admin.register(BreakStatus)
class BreakStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active')


@admin.register(Break)
class BreakAdmin(admin.ModelAdmin):
    list_display = ('id', 'replacement_link', 'break_start', 'break_end', 'status')
    list_filter = ('status',)   # Фильтрация по списку
    radio_fields = {'status': admin.HORIZONTAL}   # для того чтобы ветикально отображать статцсы и их можно отметить нажав

    def replacement_link(self, obj):
        link = reverse('admin:breaks_replacement_change', args=[obj.replacement.id])
        return format_html('<a href="{}> {} </a>', link, obj.replacement)
    # Сделали ссылку для replacement при нажатии на нее в админке переносит именно на объект Replacement
