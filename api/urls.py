from django.urls import path
from api.views import (
    PatienSearchView,
    VialListCreateAPIView,
    AllergyTemplateView,
    MissedInjectionsView,
    AllergenTestListCreateView,
    AllergenTestRetrieveUpdateDestroyView,
    AuthorizationEntryView,
    AddPatientView,
)

urlpatterns = [
    path("search/", PatienSearchView.as_view(), name="test"),
    path("vials/", VialListCreateAPIView.as_view(), name="vial_list_create"),
    path(
        "allergy-templates/",
        AllergyTemplateView.as_view(),
        name="allergy_template_create",
    ),
    path(
        "missed-injections/", MissedInjectionsView.as_view(), name="missed_injections"
    ),
    path(
        "allergen-tests/", AllergenTestListCreateView.as_view(), name="allergen-tests"
    ),
    path(
        "allergen-tests/<int:pk>/",
        AllergenTestRetrieveUpdateDestroyView.as_view(),
        name="allergen-test-detail",
    ),
    path(
        "authorization-entries/",
        AuthorizationEntryView.as_view(),
        name="authorization-entries",
    ),
    path(
        "authorization/", AuthorizationEntryView.as_view(), name="authorization_entry"
    ),
    path("patients/add/", AddPatientView.as_view(), name="add_patient"),
]
