from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.reverse import reverse_lazy

from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate  # NOQA
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

from .models import PoolOwner, Pool, PoolReading
from .serializers import (
    PoolOwnerSerializer,
    PoolSerializer,
    PostPoolReadingSerializer,
    PoolReadingSerializer,
    LoginCredentialSerializer
)


HTMLFormParsers = [FormParser, MultiPartParser]


def finalize_response(request, response, **kwargs):
    logout = reverse_lazy('logout',
                          kwargs=kwargs,
                          request=request)
    response['Link'] = ('<{}>; rel="logout"; '
                        'title="Logout"'
                        ).format(logout)
    return response


class RegisterPoolOwner(generics.CreateAPIView):
    serializer_class = PoolOwnerSerializer
    parser_classes = HTMLFormParsers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        password = payload.pop('password')
        password2 = payload.pop('password2')
        if password != password2:
            return Response(
                {'result': 'error', 'detail': 'password mismatch'},
                status=400)

        username = payload.pop('username')
        email = payload.pop('email')
        user = User.objects.create_user(
            username, email=email, password=password,
            **{'first_name': payload.pop('first_name'),
               'last_name': payload.pop('last_name')})

        PoolOwner.objects.create(user=user, **payload)
        user = authenticate(username=username, password=password)
        login(request, user)

        return finalize_response(
            request, redirect('add-pool'), **kwargs)


class Login(generics.CreateAPIView):
    serializer_class = LoginCredentialSerializer
    parser_classes = HTMLFormParsers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        print('{}'.format(request.query_params))
        user = authenticate(username=payload['username'],
                            password=payload['password'])
        if user is None:
            return finalize_response(
                request, Response({'result': 'login failed'}), **kwargs)

        login(request, user)

        if 'next' in request.query_params:
            print('redirect to {}'.format(request.query_params['next']))
            return finalize_response(
                request, redirect(request.query_params['next']), **kwargs)

        return finalize_response(request, redirect('add-pool'), **kwargs)


class AddPool(generics.CreateAPIView):
    serializer_class = PoolSerializer
    parser_classes = HTMLFormParsers

    @method_decorator(login_required(login_url='login/'))
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    @method_decorator(login_required(login_url='login/'))
    def post(self, request, *args, **kwargs):
        if request.method == 'GET':
            return finalize_response(request, Response({}), **kwargs)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        pool = Pool.objects.create(user_id=request.user.id, **payload)

        return finalize_response(
            request, Response({'result': 'created', 'id': pool.id}), **kwargs)


class ListPools(generics.ListAPIView):
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer

    def get_queryset(self):
        return Pool.objects.filter(
            user__id=self.request.user.id)

    @method_decorator(login_required(login_url='login/'))
    def get(self, request, *args, **kwargs):
        return finalize_response(
            request,
            super(ListPools, self).get(request, *args, **kwargs),
            **kwargs)


class PostPoolReading(generics.CreateAPIView):
    serializer_class = PostPoolReadingSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.method == 'GET':
            return finalize_response(request, Response({}), **kwargs)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        pool = Pool.objects.get(
            id=payload['pool_name'],
            user__id=request.user.id)

        reading = PoolReading.objects.create(
            pool=pool,
            when=payload['when'],
            level=payload['level'])

        return finalize_response(
            request, Response({'result': 'created', 'id': reading.id}),
            **kwargs)


class ListPoolReading(generics.ListAPIView):
    serializer_class = PoolReadingSerializer

    def get_queryset(self):
        return PoolReading.objects.filter(
            pool__user_id=self.request.user.id).order_by('pool__id',
                                                         '-when')
    @method_decorator(login_required(login_url='login/'))
    def get(self, request, *args, **kwargs):
        response = super(ListPoolReading, self).get(request, *args, **kwargs)
        return finalize_response(request, response, **kwargs)
