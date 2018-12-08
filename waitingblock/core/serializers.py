from rest_framework import serializers
from core.models import Table, BOOL_CHOICES
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    tables = serializers.HyperlinkedRelatedField(many=True, view_name='table-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'tables')

class TableSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='table-highlight', format='html')

    class Meta:
        model = Table
        fields = ('url', 'highlight', 'owner', 'id','name', 'partysize', 'arrival_time', 'contact', 'status', 'wait')
        owner = serializers.ReadOnlyField(source='owner.username')
