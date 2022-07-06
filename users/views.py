
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import FormParser,MultiPartParser,JSONParser,FileUploadParser
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from .import serializers
from .import permissions
from . import models
# Create your views here.




class UserProfileViewSet(viewsets.ModelViewSet):
     
    serializer_class=serializers.UserProfileSerializer
    queryset=models.UserProfile.objects.all()
    
    authentication_classes=(TokenAuthentication,) #tuple
    permission_classes=(permissions.UpdateOwnProfile,)
    parser_classes=(JSONParser,FileUploadParser,FormParser,MultiPartParser)
    filter_backends=(filters.SearchFilter,)
    search_fields=('name','email',)
    
    @action(detail=True,methods=['PUT'])
    def profile(self,request,pk=None):
        
        user=self.get_object()
        UserProfile=user.UserProfile
        serializer = serializers.UserProfileSerializer(UserProfile,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UploadView(APIView):
    parser_classes=(FileUploadParser,)

    def post(self,request):
        file=request.data.get('file',None)
        import pdb;pdb.set_trace()
        print(file)
        if file:
            return Response({'message':'File is received'},status=200)
        else:
            return Response({'message':'No file here'},status=status.HTTP_400_BAD_REQUEST)

class LoginViewSet(viewsets.ViewSet):

    serializer_class=AuthTokenSerializer

    def create(self,request):

        return ObtainAuthToken().as_view()(request=request._request)

class UserProfileFeedViewSet(viewsets.ModelViewSet):

    authentication_classes =(TokenAuthentication,)
    serializer_class=serializers.ProfileFeedItemSerializer
    queryset=models.ProfileFeedItem.objects.all()
    permission_classes=(permissions.PostOwnStatus,IsAuthenticated)

    def perform_create(self,serializer):
        '''Sets the user profile to the logged in user'''

        serializer.save(user_profile=self.request.user)


