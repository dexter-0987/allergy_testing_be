from django.db.models import Q
from datetime import date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics

from api.models import AuthorizationEntry, Patient, Vial, AllergyTemplate, AllergenTest
from api.serializers import (
    VialSerializer,
    AllergyTemplateSerializer,
    AllergenTestSerializer,
    AuthorizationEntrySerializer,
    PatientSerializer,
)


class PatienSearchView(APIView):
    """
    API view to handle patient search.
    """

    def get(self, request):
        name_query = request.query_params.get("name", "")
        patients = Patient.objects.filter(
            Q(first_name__icontains=name_query)
            | Q(middle_name__icontains=name_query)
            | Q(last_name__icontains=name_query)
        )

        if not name_query:
            return Response(
                {"message": "Please provide a name to search."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not patients.exists():
            return Response(
                {"message": "No patients found."}, status=status.HTTP_404_NOT_FOUND
            )

        data = []
        for patient in patients:
            patient_data = {
                "Patient Id": patient.id,
                "Patient Name": f"{patient.first_name} {patient.middle_name} {patient.last_name}",
                "Date of birth": patient.birth_date,
                "Last Test Date": "NA",
                "Insurance": patient.insurance_type,
                "Referral": "Yes" if patient.referral else "No",
                "Visits/Exp": "NA",
                "Billout Date": "NA",
            }

            data.append(patient_data)

        return Response(
            data,
            status=status.HTTP_200_OK,
        )


class VialCreateView(APIView):
    """
    API view to handle vial creation.
    """

    def post(self, request):
        serializer = VialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VialListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list vials.
    """

    # queryset = Vial.objects.all()
    serializer_class = VialSerializer

    def get_queryset(self):
        patient_id = self.request.query_params.get("patient")
        if patient_id:
            return Vial.objects.filter(patient_id=patient_id)
        return Vial.objects.all()


class AllergyTemplateView(APIView):
    """
    API view to create and list allergy templates.
    """

    def get(self, request):
        patient_id = request.query_params.get("patient", None)

        if patient_id:
            templates = AllergyTemplate.objects.filter(vial__patient__id=patient_id)
        else:
            templates = AllergyTemplate.objects.all()

        serializer = AllergyTemplateSerializer(templates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AllergyTemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MissedInjectionsView(APIView):
    """
    API View to handle missed injections.
    """

    def get(self, request):
        weeks = int(request.query_params.get("weeks", 4))
        print("!!!!!!!!!!!!!!!", timedelta(weeks=weeks))
        threshold_date = date.today() - timedelta(weeks=weeks)

        patients = Patient.objects.filter(
            vial__templates__date__lt=threshold_date
        ).distinct()
        data = []

        print("***********", patients)

        for patient in patients:
            # Get the most recent injection date
            latest_template = (
                AllergyTemplate.objects.filter(vial__patient=patient)
                .order_by("-date")
                .first()
            )

            print("latest_template date", latest_template.date)
            print("threshold_date", threshold_date)

            if latest_template and latest_template.date < threshold_date:
                data.append(
                    {
                        "patient_id": patient.id,
                        "patient_name": f"{patient.first_name} {patient.middle_name} {patient.last_name}",
                        "phone": patient.phone,
                        "last_injection_date": latest_template.date,
                        "weeks_since_last_injection": (
                            date.today() - latest_template.date
                        ).days
                        // 7,
                    }
                )

        return Response(data, status=status.HTTP_200_OK)


class AllergenTestListCreateView(generics.ListCreateAPIView):
    queryset = AllergenTest.objects.all()
    serializer_class = AllergenTestSerializer

    def get_queryset(self):
        patient_id = self.request.query_params.get("patientId")
        if patient_id:
            return self.queryset.filter(patient_id=patient_id).order_by("-test_date")
        return self.queryset.none()


class AllergenTestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AllergenTest.objects.all()
    serializer_class = AllergenTestSerializer
    lookup_field = "pk"


class AuthorizationEntryView(APIView):
    """
    API view to handle authorization entries with file upload.
    """

    def get(self, request):
        patient_id = request.query_params.get("patient_id")
        if not patient_id:
            return Response(
                {"message": "patient_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        entries = AuthorizationEntry.objects.filter(
            patient_id=patient_id
        ).prefetch_related("procedures")
        serializer = AuthorizationEntrySerializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        patient_id = request.data.get("patientId")

        if not patient_id:
            return Response(
                {"message": "Patient ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        entries = []
        index = 0

        # Loop through flattened form data: entries[0].field, entries[1].procedures[0].field, etc.
        while f"entries[{index}].drug_name" in request.data:
            # Extract flat fields
            entry = {
                "patient": patient_id,
                "drug_name": request.data.get(f"entries[{index}].drug_name"),
                "dose": request.data.get(f"entries[{index}].dose"),
                "frequency": request.data.get(f"entries[{index}].frequency"),
                "insurance": request.data.get(f"entries[{index}].insurance"),
                "auth_number": request.data.get(f"entries[{index}].auth_number"),
                "expiration_date": request.data.get(
                    f"entries[{index}].expiration_date"
                ),
                "at_home": request.data.get(f"entries[{index}].at_home")
                in ["true", "True", "1"],
                "cost_estimate": request.data.get(f"entries[{index}].cost_estimate"),
                "visit_history": request.data.get(f"entries[{index}].visit_history"),
                "uploaded_doc": request.FILES.get(f"entries[{index}].docs"),
                "icd10_codes": request.data.get(f"entries[{index}].icd10_codes", ""),
                "procedure_codes": request.data.get(
                    f"entries[{index}].procedure_codes", ""
                ),
            }

            # Gather nested procedures
            procedures = []
            p_index = 0
            while f"entries[{index}].procedures[{p_index}].code" in request.data:
                procedures.append(
                    {
                        "code": request.data.get(
                            f"entries[{index}].procedures[{p_index}].code"
                        ),
                        "units": request.data.get(
                            f"entries[{index}].procedures[{p_index}].units"
                        ),
                        "start_date": request.data.get(
                            f"entries[{index}].procedures[{p_index}].start_date"
                        ),
                        "end_date": request.data.get(
                            f"entries[{index}].procedures[{p_index}].end_date"
                        ),
                        "frequency": request.data.get(
                            f"entries[{index}].procedures[{p_index}].frequency"
                        ),
                        "description": request.data.get(
                            f"entries[{index}].procedures[{p_index}].description"
                        ),
                    }
                )
                p_index += 1

            entry["procedures"] = procedures
            entries.append(entry)
            index += 1

        serializer = AuthorizationEntrySerializer(data=entries, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Authorization entries created successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPatientView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Patient added successfully", "patient": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
