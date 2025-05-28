from django.contrib import admin
from api.models import (
    Physician,
    Patient,
    ServiceType,
    Vial,
    AllergyTemplate,
    AllergenTest,
    AuthorizationEntry,
)

admin.site.register(
    [
        Physician,
        Patient,
        ServiceType,
        Vial,
        AllergyTemplate,
        AllergenTest,
        AuthorizationEntry,
    ]
)
