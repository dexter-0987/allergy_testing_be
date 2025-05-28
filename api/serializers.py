from rest_framework import serializers
from django.utils import timezone

from api.models import (
    Vial,
    Patient,
    AllergyTemplate,
    AllergenTest,
    AuthorizationEntry,
    ProcedureDetail,
)


class PatientSerializer(serializers.ModelSerializer):
    referral = serializers.SerializerMethodField()
    visits_exp = serializers.SerializerMethodField()
    last_test_date = serializers.SerializerMethodField()
    billout_date = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "birth_date",
            "insurance_type",
            "referral",
            "visits_exp",
            "last_test_date",
            "billout_date",
        ]

    def get_referral(self, obj):
        return "Yes" if obj.referral else "No"

    def get_visits_exp(self, obj):
        return "NA"

    def get_last_test_date(self, obj):
        return "NA"

    def get_billout_date(self, obj):
        return "NA"


class VialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vial
        fields = "__all__"

    # def validate(self, attrs):
    #     patient = attrs.get("patient")

    # # Count existing vials for this patient
    # existing_vials = Vial.objects.filter(patient=patient).count()

    # # Exclude current instance from count if updating
    # if self.instance:
    #     existing_vials -= 1

    # if existing_vials >= 3:
    #     raise serializers.ValidationError("A patient can have a maximum of 3 vials.")

    # return attrs


class AllergyTemplateSerializer(serializers.ModelSerializer):
    vial_name = serializers.SerializerMethodField()

    class Meta:
        model = AllergyTemplate

        fields = [
            "id",
            "vial_name",
            "vial_color",
            "vial",
            "dose",
            "date",
            "arm",
            "peak_flow",
            "tech_id",
            "hcrm_applied",
            "reaction",
            "notes",
        ]

    def get_vial_name(self, obj):
        return obj.vial.name if obj.vial else None


class AllergenTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllergenTest
        fields = "__all__"

    def create(self, validated_data):
        instance, created = AllergenTest.objects.update_or_create(
            patient=validated_data["patient"],
            allergen_name=validated_data["allergen_name"],
            defaults={
                "category": validated_data.get("category"),
                "reaction_level": validated_data.get("reaction_level"),
                "custom_size": validated_data.get("custom_size"),
                "test_date": validated_data.get("test_date", timezone.now()),
            },
        )
        return instance


class ProcedureDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureDetail
        exclude = ["authorization_entry"]


class AuthorizationEntrySerializer(serializers.ModelSerializer):
    procedures = ProcedureDetailSerializer(many=True)

    class Meta:
        model = AuthorizationEntry
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        procedures_data = validated_data.pop("procedures", [])
        entry = AuthorizationEntry.objects.create(**validated_data)
        for proc_data in procedures_data:
            ProcedureDetail.objects.create(authorization_entry=entry, **proc_data)
        return entry

    def update(self, instance, validated_data):
        procedures_data = validated_data.pop("procedures", [])

        # Update fields on the main instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Optional: clear and recreate all procedures
        instance.procedures.all().delete()
        for proc_data in procedures_data:
            ProcedureDetail.objects.create(authorization_entry=instance, **proc_data)

        return instance


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"
