from rest_framework import viewsets, filters, views, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Destination
from .serializers import DestinationSerializer, UserSerializer
from .ml_model import predict_tourists
from datetime import datetime

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username
        })

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out."}, status=200)

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'location']

@api_view(['GET'])
def forecast_tourists(request):
    try:
        year_str = request.GET.get('year')
        month_str = request.GET.get('month')
        
        if year_str and month_str:
            year = int(year_str)
            month = int(month_str)
        else:
            now = datetime.now()
            year = now.year
            month = now.month
            
        prediction = predict_tourists(year, month)
        
        # Add some mock variations for different regions for the dashboard
        regions = {
            "North India": int(prediction * 0.4),
            "South India": int(prediction * 0.3),
            "West India": int(prediction * 0.2),
            "East India": int(prediction * 0.1)
        }
        
        return Response({
            'year': year,
            'month': month,
            'forecasted_tourists': prediction,
            'regional_breakdown': regions
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)
