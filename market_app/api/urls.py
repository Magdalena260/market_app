from django.contrib import admin
from .views import markets_view, market_single_view

urlpatterns = [
    
    path('', markets_view)
    path('<int:pk>/', markets_single_view),
]
