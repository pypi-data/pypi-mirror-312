from django.forms import DateTimeField

from core.models.contenttypes import ObjectType
from utilities.forms.fields import CommentField, DynamicModelMultipleChoiceField
from utilities.forms.widgets import DateTimePicker
from utilities.forms.widgets.apiselect import APISelectMultiple
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm

from sop_migration.models import SopMigration


__all__ = ("SopMigrationForm", "SopMigrationFilterSetForm")


class SopMigrationForm(NetBoxModelForm):

    date = DateTimeField(label="Migration date", widget=DateTimePicker())
    comments = CommentField()

    class Meta:
        model = SopMigration
        fields = [
            "object_type",
            "object_id",
            "date",
            "cut",
            "impact",
            "state",
            "description",
            "comments",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "tags" in self.fields:
            del self.fields["tags"]


class SopMigrationFilterSetForm(NetBoxModelFilterSetForm):

    # all object_type ids
    object_type_ids = SopMigration.objects.values_list("object_type__id", flat=True)

    model = SopMigration
    object_type = DynamicModelMultipleChoiceField(
        queryset=ObjectType.objects.filter(pk__in=object_type_ids),
        required=False,
        label="Object (Type)",
        # only get existing object types
        widget=APISelectMultiple(
            api_url=f"/api/extras/object-types/?id="
            + "&id".join(map(str, object_type_ids))
        ),
    )
