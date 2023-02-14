from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

router = DefaultRouter()
router.register('tag', views.TagViewSet)
router.register('ingredient', views.IngredientViewSet)
router.register('recipes', views.RecipesWriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'users/<int:user_id>/subscribe/',
        views.APISubscribePostDelete.as_view()),
    path(
        'users/subscriptions/',
        views.APISubscriptionsList.as_view()),

    path('', include('djoser.urls')),  # Работа с пользователями
    path('auth/', include('djoser.urls.authtoken')),  # Работа с токенами

    path('zsv2/', views.zsv_page, name='zsv_page'),  # my
]
