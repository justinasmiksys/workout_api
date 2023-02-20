from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("", views.getRoutes),
    # auth
    path("signup/", views.signup),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # general data
    path("exercises/", views.getExercises),
    path("exercises/<int:id>/", views.getExercise),
    path("muscles/", views.getMuscles),
    # workout
    path("workouts/", views.getWorkouts),
    path("workouts/<int:id>/", views.getWorkout),
    path("postworkout/", views.postWorkout),
    path("putworkout/", views.putWorkout),
    path("deleteworkout/<int:id>/", views.deleteWorkout),
    # event
    path("events/", views.getEvents),
    path("postevent/", views.postEvent),
    path("deleteevent/<int:id>/", views.deleteEvent),
]
