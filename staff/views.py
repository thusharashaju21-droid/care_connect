from django.shortcuts import render
from staff.models import Doctor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

# Create your views here.
class DoctorCreateListView(APIView):

    def get(self,request):

        qs=Doctor.objects.all().values()

        doctors_list=list(qs)

        return Response(data=doctors_list)

    def post(self,request):

        form_data = request.data

        specialization = form_data.get("specialization")

        flat=[tp[0] for tp in Doctor.SPECIALIZATION_OPTIONS]

        if specialization not in Doctor.flat:

            raise serializers.ValidationError(specialization+ "is not a valid choice")

        Doctor.objects.create(**form_data)

        return Response(data={"message":"doctor Created "})

class DoctorRetrieveUpdateDeleteView(APIView):

    def get(self,request,pk=None):

        qs = Doctor.objects.filter(id=pk).values()

        doctor_list= list(qs)

        return Response(data=doctor_list)

    def put(self,request,pk=None):

        form_data = request.data

        Doctor.objects.filter(id=pk).update(**form_data)

        return Response (data={"message" : "updated"})

    def delete(self,request,pk=None):

        Doctor.objects.get(id=pk).delete()

        return Response(data={"message" : "deleted successfully"})
    

