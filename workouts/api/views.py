from workouts.models import CustomUser, Exercise, Muscle, Workout, Set, Event

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import json
from django.db.utils import IntegrityError

from .serializers import (
    ExerciseSerializer,
    MuscleSerializer,
    WorkoutSerializer,
    EventSerializer,
)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "/api/token",
        "/api/token/refresh",
    ]

    return Response(routes)


# auth


@api_view(["POST"])
def signup(request):

    body = json.loads(request.body)
    username = body["username"]
    email = body["email"]
    password = body["password"]

    try:
        CustomUser.objects.create_user(
            username=username, email=email, password=password
        )
    except IntegrityError as e:
        message = str(e)
        failed_parameter_string = message.split(".")[-1]
        response_message = f"Such {failed_parameter_string} already exists!"

        return JsonResponse({"error": response_message}, status=409)

    return JsonResponse({"message": "Success"}, status=200)


# general


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getExercises(request):
    exercises = Exercise.objects.all()
    serializer = ExerciseSerializer(exercises, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getExercise(request, id):
    exercise = Exercise.objects.get(id=id)
    serializer = ExerciseSerializer(exercise)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMuscles(request):
    muscles = Muscle.objects.all()
    serializer = MuscleSerializer(muscles, many=True)

    return Response(serializer.data)


# workout


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getWorkouts(request):

    user = request.user
    workouts = Workout.objects.filter(user=user)
    serializer = WorkoutSerializer(workouts, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getWorkout(request, id):
    user = request.user
    workout = Workout.objects.get(user=user, id=id)
    serializer = WorkoutSerializer(workout)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postWorkout(request):
    body = json.loads(request.body)

    try:
        workout = Workout(title=body["title"], color=body["hex"], user=request.user)
        workout.save()

        for exercise_data in body["exercises"]:
            exercise = Exercise.objects.get(id=exercise_data["id"])

            for index, set_data in enumerate(exercise_data["sets"], start=1):
                set_object = Set(
                    exercise=exercise,
                    workout=workout,
                    reps=set_data["value"],
                    priority=index,
                )
                set_object.save()

    except IntegrityError as e:
        return JsonResponse(
            {"error": "Workout with such title already exists"}, status=409
        )

    return JsonResponse({"message": "Success"}, status=200)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putWorkout(request):
    body = json.loads(request.body)

    try:
        workout = Workout.objects.get(title=body["oldTitle"], user=request.user)

        workout.title = body["newTitle"]
        workout.color = body["hex"]
        workout.save()

        sets = Set.objects.filter(workout=workout)
        sets.delete()

        for exercise_data in body["exercises"]:
            exercise = Exercise.objects.get(id=exercise_data["id"])

            for index, set_data in enumerate(exercise_data["sets"], start=1):
                set_object = Set(
                    exercise=exercise,
                    workout=workout,
                    reps=set_data["value"],
                    priority=index,
                )
                set_object.save()

    except IntegrityError as e:
        return JsonResponse(
            {"error": "Workout with such title already exists"}, status=409
        )

    return JsonResponse({"message": "Success"}, status=200)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteWorkout(request, id):
    try:
        user = request.user
        workout = Workout.objects.filter(user=user, id=id)
        workout.delete()
    except:
        return JsonResponse({"error": "Something went wrong"}, status=409)

    return JsonResponse({"message": "Success"}, status=200)


# events


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postEvent(request):
    body = json.loads(request.body)
    workout = Workout.objects.get(id=body["workoutId"])

    event = Event(workout=workout, date=body["eventDate"], user=request.user)
    event.save()

    return JsonResponse({"message": "Success"}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getEvents(request):
    user = request.user
    events = Event.objects.filter(user=user)
    serializer = EventSerializer(events, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteEvent(request, id):
    try:
        user = request.user
        event = Event.objects.filter(user=user, id=id)
        event.delete()
    except:
        return JsonResponse({"error": "Something went wrong"}, status=409)

    return JsonResponse({"message": "Success"}, status=200)
