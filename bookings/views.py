from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from bookings.models import Appointment
from bookings.serializers import AppointmentSerializer
from staff.models import Doctor

# Create your views here.
class AppointmentListCreateView(APIView):

    def get(self,request):

        qs = Appointment.objects.all()

        serial_instance = AppointmentSerializer(qs,many=True)

        return Response(data=serial_instance.data)
    

    def post(self,request):

        form_data = request.data

        serializer_instannce = AppointmentSerializer(data=form_data)

        if serializer_instannce.is_valid():

            cleaned_data = serializer_instannce.validated_data

            """
            cleaned_data =
        
            {
                "patient_name": "Syam",
                "phone": "9876543214",
                "doctor": 4,
                "appointment_date": "2026-10-09",
                "problem": "Back pain"
            }
              
            """

            doctor = cleaned_data.get("doctor") # DOCTOR_ID not diect save convert object

            appointment_date = cleaned_data.get("appointment_date")

            new_token = 0

            last_appoinment_object = Appointment.objects.filter(doctor = doctor,appointment_date = appointment_date).last()

            if last_appoinment_object:

                new_token = last_appoinment_object.token_number+1

            else:

                new_token = 1

            doctor_object = Doctor.objects.get(id = doctor) # dr object retrieve

            cleaned_data["doctor"] = doctor_object

            Appointment.objects.create(**cleaned_data,token_number = new_token)

            response_data = {

            "status" : "booked",
            "token" : new_token

            }

            return Response(data=response_data)

        else:

            return Response(data=serializer_instannce.errors)

