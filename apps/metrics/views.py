from django.contrib.auth.models import User
from oauth2_provider.models import AccessToken
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from ..accounts.models import UserProfile
from ..dot_ext.models import Application


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class AppMetricsSerializer(ModelSerializer):

    beneficiaries = SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ('id', 'name', 'active', 'user', 'beneficiaries')

    def get_beneficiaries(self, obj):
        return({'count': AccessToken.objects.filter(application=obj.id).distinct('user').count()})


class AppMetricsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class BeneMetricsView(APIView):
    """
    View to provide beneficiary metrics.

    * Only admin users are able to access this view.
    * Default returns count info
    """
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )

    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        content = {
            'count': UserProfile.objects.filter(user_type='BEN').count()
        }
        return Response(content)


class AppMetricsView(ListAPIView):
    """
    View to provide application metrics.


    * Only admin users are able to access this view
    * Default returns count info and application list data with unique bene counts
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    serializer_class = AppMetricsSerializer
    pagination_class = AppMetricsPagination

    def get_queryset(self):

        queryset = Application.objects.all().order_by('name')

        return queryset


class AppMetricsDetailView(APIView):
    """
    View to provide application metrics detail.


    * Only admin users are able to access this view
    * Default returns count info and application list data with unique bene count
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    def get(self, request, pk, format=None):

        queryset = Application.objects.get(pk=pk)

        return Response(AppMetricsSerializer(queryset).data)


class TokenMetricsView(APIView):
    """
    View to provide access token metrics.

    * Only admin users are able to access this view.
    * Default returns count info
    """
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )

    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        content = {
            'count': AccessToken.objects.count()
        }
        return Response(content)
