from rest_framework import serializers
from ..models import Song
import urllib.parse

class SongSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = '__all__'

    def get_name(self, obj):
      return urllib.parse.unquote(obj.name)