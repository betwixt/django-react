from rest_framework import serializers
from .calcsubject import CalcSubject

class CalcSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'birthMonth', 'birthNum', )
        model = CalcSubject
