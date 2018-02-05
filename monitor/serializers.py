from rest_framework import serializers
from django.contrib.auth.models import User

from .models import PoolOwner, Pool, PoolReading, PoolLevel


class LoginCredentialSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=User._meta.get_field('username').max_length)
    password = serializers.CharField(
        max_length=User._meta.get_field('password').max_length,
        style={'input_type': 'password'})

    class Meta:
        fields = ['username', 'password']


class PoolOwnerSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=User._meta.get_field('username').max_length)
    password = serializers.CharField(
        max_length=User._meta.get_field('password').max_length,
        style={'input_type': 'password'})
    password2 = serializers.CharField(
        max_length=User._meta.get_field('password').max_length,
        style={'input_type': 'password'},
        label='Verify password')
    first_name = serializers.CharField(
        max_length=User._meta.get_field('first_name').max_length)
    last_name = serializers.CharField(
        max_length=User._meta.get_field('last_name').max_length)
    email = serializers.CharField(
        max_length=User._meta.get_field('email').max_length)

    class Meta:
        fields = ['username', 'password', 'password2',
                  'first_name', 'last_name', 'email']
        fields.extend([f.name for f in PoolOwner._meta.get_fields()])
        fields.remove('user')


class PoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pool
        exclude = ('user',)


class PostPoolReadingSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(PostPoolReadingSerializer, self).__init__(*args, **kwargs)
        self.fields['pool_name'] = serializers.ChoiceField(
            choices=[(p.id, p.name)
                     for p in Pool.objects.filter(
                        user__id=self.context['view'].request.user.id)])

    pool_name = serializers.ChoiceField(choices=[])

    class Meta:
        model = PoolReading
        fields = ('pool_name', 'when', 'level')


class PoolNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pool
        fields = ('name',)

    def to_representation(self, obj):
        return obj.name


class PoolReadingSerializer(serializers.ModelSerializer):
    pool = PoolNameSerializer()

    def to_representation(self, instance):
        ret = super(PoolReadingSerializer, self).to_representation(instance)
        ret['level'] = PoolLevel(ret['level']).name
        return ret

    class Meta:
        model = PoolReading
        fields = ('pool', 'when', 'level')
