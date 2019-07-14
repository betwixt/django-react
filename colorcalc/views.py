from .calcsubject import CalcSubject
from .serializers import CalcSubjectSerializer
from rest_framework import generics


class SubjectList(generics.ListCreateAPIView):
    queryset = CalcSubject.objects.all()
    serializer_class = CalcSubjectSerializer


class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CalcSubject.objects.all()
    serializer_class = CalcSubjectSerializer

