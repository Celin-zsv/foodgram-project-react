from api_foodgram import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api_foodgram'

router = DefaultRouter()
router.register('tag', views.TagViewSet)
router.register('ingredient', views.IngredientViewSet)
router.register('recipes', views.RecipesWriteViewSet)
router.register('users', views.CustomUserViewSet)  # Работа с пользователями

urlpatterns = [
    path('', include(router.urls)),
    path('zsv2/', views.zsv_page, name='zsv_page'),
    path('auth/', include('djoser.urls.authtoken')),  # Работа с токенами
]
