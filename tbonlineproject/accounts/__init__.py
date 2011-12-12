from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

content_type, created = ContentType.objects.get_or_create(model='basicpost')

permission, created = Permission.objects.get_or_create(codename='can_submit', name='Can Submit Posts', content_type=content_type)
permission.save()

group, created = Group.objects.get_or_create(name='Contributors')
group.save()

group.permissions.add(permission)
group.save()
