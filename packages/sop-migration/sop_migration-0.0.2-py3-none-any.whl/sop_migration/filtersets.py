from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from sop_migration.models import SopMigration


__all__ = ("SopMigrationFilterSet",)


class SopMigrationFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = SopMigration
        fields = ("id", "object_type", "object_id", "date", "state", "impact")

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(object_type__icontains=value)
            | Q(object_id__icontains=value)
            | Q(date__icontains=value)
            | Q(state__icontains=value)
            | Q(impact__icontains=value)
        )
