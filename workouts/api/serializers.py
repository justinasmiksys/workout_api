from rest_framework.serializers import ModelSerializer, SerializerMethodField
from workouts.models import Exercise, Muscle, Workout, Set, Event


class MuscleSerializer(ModelSerializer):
    class Meta:
        model = Muscle
        # fields = ["id", "name"]
        fields = "__all__"


class ExerciseSerializer(ModelSerializer):
    primary = MuscleSerializer(read_only=True, many=True)
    secondary = MuscleSerializer(read_only=True, many=True)

    class Meta:
        model = Exercise
        # fields = ["id", "name", "url_img"]
        fields = "__all__"


class SetSerializer(ModelSerializer):
    class Meta:
        model = Set
        fields = ["reps", "priority", "exercise"]


class WorkoutSerializer(ModelSerializer):
    sets = SerializerMethodField()

    def get_sets(self, obj):
        sets = Set.objects.filter(workout=obj.id)
        sets_serializer = SetSerializer(sets, many=True)
        return sets_serializer.data

    class Meta:
        model = Workout
        fields = "__all__"


class EventSerializer(ModelSerializer):
    title = SerializerMethodField()
    color = SerializerMethodField()

    def get_title(self, obj):
        return obj.workout.title

    def get_color(self, obj):
        return obj.workout.color

    class Meta:
        model = Event
        fields = "__all__"
