from api_foodgram import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from .views import views

app_name = 'api_foodgram'

router = DefaultRouter()
router.register('tag', views.TagViewSet)
router.register('ingredient', views.IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('zsv2/', views.zsv_page, name='zsv_page'),
    # path('', views.get_token),
]
