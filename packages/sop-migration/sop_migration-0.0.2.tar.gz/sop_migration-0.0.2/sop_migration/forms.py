from django.forms import DateTimeField

from netbox.forms import NetBoxModelForm
from utilities.forms.fields import CommentField
from utilities.forms.widgets import DateTimePicker

from sop_migration.models import SopMigration


__all__ = ("SopMigrationForm",)


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
