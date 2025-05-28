from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from localflavor.us.us_states import US_STATES

DEGREE_CHOICES = [
    ("MD", "Doctor of Medicine (M.D.)"),
    ("DO", "Doctor of Osteopathic Medicine (D.O.)"),
    ("NP", "Nurse Practitioner (N.P.)"),
    ("PA", "Physician Assistant (P.A.)"),
    ("DC", "Doctor of Chiropractic (D.C.)"),
    ("DDS", "Doctor of Dental Surgery (D.D.S.)"),
    ("DMD", "Doctor of Medicine in Dentistry (D.M.D.)"),
    ("PhD", "Doctor of Philosophy (Ph.D.)"),
    ("Other", "Other"),
]
RELATIONSHIP_CHOICES = [
    ("Self", "Self"),
    ("Spouse", "Spouse"),
    ("Child", "Child"),
    ("Mother", "Mother"),
    ("Father", "Father"),
    ("Grandparent", "Grandparent"),
    ("Grandchild", "Grandchild"),
    ("Niece/Nephew", "Niece/Nephew"),
    ("Stepchild", "Stepchild"),
    ("Fosterchild", "Fosterchild"),
    ("Ward", "Ward"),
    ("Employee", "Employee"),
    ("Life Partner", "Life Partner"),
    ("Significant Other", "Significant Other"),
    ("Handicapped Dependent", "Handicapped Dependent"),
    ("Other", "Other"),
    ("Unknown", "Unknown"),
]
MARITAL_CHOICES = [
    ("Single", "Single"),
    ("Married", "Married"),
    ("Separated", "Separated"),
    ("Divorced", "Divorced"),
    ("Widowed", "Widowed"),
    ("Prefer not to answer", "Prefer not to answer"),
    ("Other", "Other"),
]
LANGUAGE_CHOICES = [
    ("Brazilian Portuguese", "Brazilian Portuguese"),
    ("French", "French"),
    ("German", "German"),
    ("Italian", "Italian"),
    ("Japanese", "Japanese"),
    ("Korean", "Korean"),
    ("Portuguese", "Portuguese"),
    ("Russian", "Russian"),
    ("Simplified Chinese", "Simplified Chinese"),
    ("Spanish", "Spanish"),
    ("Traditional Chinese", "Traditional Chinese"),
    ("United States English", "United States English"),
]
ETHNICITY_CHOICES = [
    ("Hispanic and Latino", "Hispanic and Latino"),
    ("Not Hispanic and Latino", "Not Hispanic and Latino"),
]
INSURANCE_CHOICES = [
    ("Primary", "Primary"),
    ("Secondary", "Secondary"),
    ("Tertiary", "Tertiary"),
    ("Other", "Other"),
]
REACTION_CHOICES = [
    ("MR", "MR"),
    ("NR", "NR"),
    ("3mm", "3mm"),
    ("4mm", "4mm"),
    ("5mm", "5mm"),
    ("6mm", "6mm"),
    ("7mm", "7mm"),
    ("8mm", "8mm"),
    ("9mm", "9mm"),
    ("10mm", "10mm"),
    (">10mm", ">10mm"),
]


class BaseModel(models.Model):
    """
    Abstract base model that includes common fields for all models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Physician(BaseModel):
    """
    Description: Model representing a physician.
    Fields:
        - name: The name of the physician.
        - degree: The degree of the physician (e.g., MD, DO).
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="physician_profile"
    )
    name = models.CharField(max_length=255)
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES)

    def __str__(self):
        return f"{self.name}, {self.degree}"


class ServiceType(BaseModel):
    """
    Description: Model representing a service type.
    Fields:
        - code: The code of the service type.
        - description: A description of the service type.
    """

    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.description}"


class Patient(BaseModel):
    """
    Description: Model representing a patient.
    Fields:
        - first_name: The first name of the patient.
        - middle_name: The middle name of the patient.
        - last_name: The last name of the patient.
        - birth_date: The birth date of the patient.
        - gender: The gender of the patient.
        - email: The email address of the patient.
        - marital_status: The marital status of the patient.
        - ssn: The social security number of the patient.
        - address: The address of the patient.
        - address_2: The second address line of the patient.
        - city: The city of the patient.
        - state: The state of the patient.
        - zip_code: The zip code of the patient.
        - county: The county of the patient.
        - phone: The phone number of the patient.
        - pcp: The primary care physician of the patient.
        - ref_physician: The referring physician of the patient.
        - language: The preferred language of the patient.
        - ethnicity: The ethnicity of the patient.
        - patient_consent: The consent status of the patient.
        - insurance_type: The type of insurance of the patient.
        - insurance_id: The insurance ID of the patient.
        - group_number: The group number of the insurance.
        - service_type: The type of service the patient is receiving.
        - date_of_service: The date of service for the patient.
        - plan_number: The plan number of the insurance.
        - co_pay: The copay amount for the patient.
        - eligibility_date: The eligibility date of the insurance.
        - termination_date: The termination date of the insurance.
        - payer_phone: The phone number of the insurance payer.
        - payer_fax: The fax number of the insurance payer.
        - relationship: The relationship of the patient to the insured.
        - comments: Additional comments about the patient.
    """

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(
        max_length=10, choices=[("Male", "Male"), ("Female", "Female")]
    )
    email = models.EmailField(null=True, blank=True)
    marital_status = models.CharField(max_length=30, choices=MARITAL_CHOICES)
    ssn = models.CharField(max_length=11, unique=True)
    address = models.TextField()
    address_2 = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50, choices=US_STATES)
    zip_code = models.CharField(max_length=10)
    county = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20)
    pcp = models.CharField(max_length=255, null=True, blank=True)
    ref_physician = models.ForeignKey(
        Physician, on_delete=models.SET_NULL, null=True, related_name="patients"
    )
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    ethnicity = models.CharField(max_length=50, choices=ETHNICITY_CHOICES)
    patient_consent = models.BooleanField(default=True)
    insurance_type = models.CharField(max_length=50, choices=INSURANCE_CHOICES)
    insurance_id = models.CharField(max_length=100, unique=True)
    group_number = models.CharField(max_length=100)
    service_type = models.ForeignKey(
        ServiceType, null=True, on_delete=models.SET_NULL, related_name="patients"
    )
    date_of_service = models.DateField()
    plan_number = models.CharField(max_length=255, unique=True)
    co_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    eligibility_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    payer_phone = models.CharField(max_length=20)
    payer_fax = models.CharField(max_length=20)
    relationship = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES)
    referral = models.BooleanField(default=False)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Vial(BaseModel):
    """
    Description: Model representing a vial used for testing.
    Fields:
        - patient: The patient to whom the vial belongs.
        - name: The name of the vial.
        - allergens: A JSON field for storing allergen information.
        - diagnosis_codes: A JSON field for storing diagnosis codes.
        - expiration_date: The expiration date of the vial.
    """

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    expiration_date = models.DateField(null=True, blank=True)
    allergens = models.JSONField(default=list)
    diagnosis_codes = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name} - {self.patient.first_name} {self.patient.last_name}"

    class Meta:
        unique_together = ("patient", "name")
        ordering = ["-expiration_date"]
        verbose_name_plural = "Vials"


class AllergyTemplate(BaseModel):
    """
    Description: Model representing an allergy template.
    Fields:
        - name: The name of the allergy template.
        - allergens: A JSON field for storing allergen information.
        - diagnosis_codes: A JSON field for storing diagnosis codes.
    """

    vial = models.ForeignKey(Vial, on_delete=models.CASCADE, related_name="templates")
    dose = models.CharField(max_length=50)
    date = models.DateField()
    arm = models.CharField(max_length=1, choices=[("L", "Left"), ("R", "Right")])
    peak_flow = models.CharField(max_length=50)
    tech_id = models.CharField(max_length=50)
    hcrm_applied = models.BooleanField(default=False)
    reaction = models.CharField(max_length=50, choices=REACTION_CHOICES)
    notes = models.TextField(null=True, blank=True)
    vial_color = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Template for {self.vial.name} - {self.dose} on {self.date}"


class AllergenTest(models.Model):
    """
    Description: Model representing an allergen test for a patient.
    Fields:
        - patient: The patient who is being tested.
        - allergen_name: The name of the allergen being tested.
        - category: The category of the allergen (e.g., food, environmental).
        - reaction_level: The level of reaction to the allergen.
        - custom_size: A custom size for the allergen test.
        - test_date: The date of the allergen test.
    """

    CATEGORY_CHOICES = [
        ("food", "Food"),
        ("environmental", "Environmental"),
    ]

    REACTION_CHOICES = [
        ("None", "None"),
        ("1+", "1+"),
        ("2+", "2+"),
        ("3+", "3+"),
    ]

    patient = models.ForeignKey(
        "Patient", on_delete=models.CASCADE, related_name="allergen_tests"
    )
    allergen_name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    reaction_level = models.CharField(max_length=10, blank=True, null=True)
    custom_size = models.CharField(max_length=10, blank=True, null=True)
    test_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("patient", "allergen_name", "test_date")

    def __str__(self):
        return f"{self.patient} - {self.allergen_name} - {self.reaction_level or self.custom_size}"


class AuthorizationEntry(BaseModel):
    """
    Represents an authorization entry for a patient, including drug and insurance info,
    ICD-10 codes, procedure codes, and related uploaded documents.
    """

    patient = models.ForeignKey(
        "Patient", on_delete=models.CASCADE, related_name="authorization_entries"
    )

    # Drug & Insurance Info
    drug_name = models.CharField(max_length=255)
    dose = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    insurance = models.CharField(max_length=255)
    auth_number = models.CharField(max_length=100)
    expiration_date = models.DateField()
    at_home = models.BooleanField(default=False)
    cost_estimate = models.CharField(max_length=100, blank=True)
    visit_history = models.TextField(blank=True)

    # New Fields for Allergy Testing Flow
    icd10_codes = models.TextField(blank=True)  # Editable textarea with default values
    procedure_codes = models.TextField(blank=True)  # From small textarea next to radio

    uploaded_doc = models.FileField(
        upload_to="authorization_docs/", null=True, blank=True
    )

    def __str__(self):
        return f"{self.patient} - {self.drug_name} ({self.auth_number})"


class ProcedureDetail(BaseModel):
    """
    Represents a single procedure line item linked to an authorization entry.
    """

    authorization_entry = models.ForeignKey(
        AuthorizationEntry, on_delete=models.CASCADE, related_name="procedures"
    )

    code = models.CharField(max_length=100)
    units = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    frequency = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} ({self.units} units)"
