from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# custom manager for Tag model, so we can use it to filter tags by passing app_name and id
class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        """Retrieve tags for a given object type and object ID."""
        content_type = ContentType.objects.get_for_model(obj_type)
        return TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=obj_id)


# Create your models here.

class Tag(models.Model):
    label = models.CharField(max_length=64)

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # generic relationship
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
