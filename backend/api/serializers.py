from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Dataset
from backend.serializer import get_list_response_dict

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user
    
class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ["id", "title", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}


def dataset_to_dict(dataset: Dataset) -> dict:
    return {
        'id': dataset.id,
        'title': dataset.title,
        'created_at': dataset.created_at,
        'clusters': [v.cluster_data[1:-1] for v in dataset.clusters.all()],
    }
