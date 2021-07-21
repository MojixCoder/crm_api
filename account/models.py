from django.core.validators import RegexValidator
from django.db import models
from core.models import Section, Role, WorkGroup, Bank, Permission, DateModel
from django.contrib.auth.models import AbstractUser
from .utils import image_upload_to
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    """
    User Model
        Note:
            Extending Django User Model
    """
    STATUS_CHOICES = (
        (1, "Is completed"),
        (2, "Is not completed"),
        (3, "Working"),
        (4, "End of contract"),
        (5, "Resignation"),
        (6, "Fired"),
        (7, "End of work"),
    )
    SEX_CHOICES = (
        (1, "Male"),
        (2, "Female"),
    )
    EDUCATION_CHOICES = (
        (1, "Dropout"),
        (2, "Middle school degree"),
        (3, "Diploma"),
        (4, "Associate’s degree"),
        (5, "Bachelor’s degree"),
        (6, "Master’s Degree"),
        (7, "Doctorate"),
        (8, "Student"),
        (9, "Unknown"),
    )
    MARRIAGE_CHOICES = (
        (1, "Married"),
        (2, "Single"),
        (3, "Divorced"),
        (4, "Widowed"),
        (5, "Unknown"),
    )
    MILITARY_CHOICES = (
        (1, "Exempted from military service"),
        (2, "End of  military service"),
        (3, "Subject to military service"),
        (4, "fugitive"),
        (5, "Exempted due to study"),
        (6, "Temporary Exempted"),
        (7, "Female"),
        (8, "Unknown"),
    )
    
    username = models.CharField(
        max_length=150, unique=True, db_index=True, verbose_name="Username",
        validators=[
            RegexValidator(
                regex="^(?=.{4,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$",
                message="Username is not valid.",
            ),
        ],
    )
    
    # Foreign Keys
    section             = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="users", verbose_name="Section")
    role                = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="users", verbose_name="Role")
    work_group          = models.ForeignKey(WorkGroup, on_delete=models.CASCADE, related_name="users", verbose_name="Work group")
    bank                = models.ForeignKey(Bank, null=True, blank=True, on_delete=models.SET_NULL, related_name="users", verbose_name="Bank")
    permissions         = models.ManyToManyField(Permission, blank=True, related_name="users", verbose_name="Permissions")

    # Personal Information
    father              = models.CharField(max_length=255, blank=True, verbose_name="Father name")
    father_job          = models.CharField(max_length=255, blank=True, verbose_name="Father job")
    father_mobile       = models.CharField(max_length=255, blank=True, verbose_name="Father phone number")
    child               = models.IntegerField(default=0, verbose_name="Number of children")

    # ID Cards Information
    meli                = models.CharField(max_length=10, unique=True, null=True, verbose_name="National ID number")
    id_number           = models.CharField(max_length=10, unique=True, null=True, verbose_name="ID card number")
    id_place            = models.CharField(max_length=255, blank=True, verbose_name="Issuance of identity card place")
    meli_image          = models.ImageField(upload_to=image_upload_to, blank=True, verbose_name="National ID image")
    id_image            = models.ImageField(upload_to=image_upload_to, blank=True, verbose_name="ID card image")

    # Bank and Insurance Information
    card_number         = models.CharField(max_length=30, unique=True, null=True, verbose_name="Card number")
    account_number      = models.CharField(max_length=30, unique=True, null=True, verbose_name="Account number")
    shaba_number        = models.CharField(max_length=30, unique=True, null=True, verbose_name="Shaba number")
    branch_code         = models.CharField(max_length=30, blank=True, verbose_name="Branch code")
    insurance_number    = models.CharField(max_length=30, blank=True, verbose_name="Insurance number")

    # Contact Information 
    phone_number        = models.CharField(max_length=255, unique=True, null=True, verbose_name="Phone number")
    tel                 = models.CharField(max_length=255, blank=True, verbose_name="Telephone")
    emergency_mobile    = models.CharField(max_length=255, blank=True, verbose_name="Emergency contact number")
    email               = models.EmailField(unique=True, null=True, verbose_name="Email")

    # Choice Fields
    marriage            = models.IntegerField(choices=MARRIAGE_CHOICES, default=5, verbose_name="Marriage status")
    education_level     = models.IntegerField(choices=EDUCATION_CHOICES, default=9, verbose_name="Education level")
    sex                 = models.IntegerField(choices=SEX_CHOICES, default=1, verbose_name="Sex")
    military_service    = models.IntegerField(choices=MILITARY_CHOICES, default=8, verbose_name="Military service status")
    status              = models.IntegerField(choices=STATUS_CHOICES, default=2, verbose_name="User status" )

    # Place Information
    postal_code         = models.CharField(max_length=30, blank=True, verbose_name="Postal code")
    birth_place         = models.CharField(max_length=255, blank=True, verbose_name="Birth place")
    address             = models.TextField(blank=True, verbose_name="Address")

    # Images
    personal_image      = models.ImageField(upload_to=image_upload_to, blank=True, verbose_name="Personal image")
    signature_image     = models.ImageField(upload_to=image_upload_to, blank=True, verbose_name="Signature image")
    
    # Date Information
    birth_date          = models.DateField(blank=True, null=True, verbose_name="Birth date")
    start_work          = models.DateField(verbose_name="Start of work date")
    end_work            = models.DateField(blank=True, null=True, verbose_name="End of work date")
    created_at          = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at          = models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")
    
    # Removed Fields
    user_permissions = None
    groups = None
    
    # Required Fields for createsuperuser command
    REQUIRED_FIELDS = [
        "section_id", "role_id", "email",
        "work_group_id", "start_work",
    ]

    def __str__(self):
        to_repr = self.username
        if self.first_name and self.last_name:
            to_repr = self.get_full_name()
            self.get_short_name
        return to_repr
    
    def get_absolute_url(self):
        return f"{settings.BASE_URL}/api/v1/accounts/@{self.username}/"
    
    class Meta:
        ordering = "-pk",
        verbose_name = "User"
        verbose_name_plural = "Users"


class Child(DateModel):
    """ Childern of Users """
    SEX_CHOICES = (
        (1, "Male"),
        (2, "Female"),
    )
    # Foreign Keys
    parent     = models.ForeignKey(User, on_delete=models.CASCADE, related_name="children", verbose_name="Parent")

    # Child Information
    name       = models.CharField(max_length=255, verbose_name="Child name")
    birth_date = models.DateField(verbose_name="Birth date")
    sex        = models.IntegerField(choices=SEX_CHOICES, default=1, verbose_name="Sex")
    has_impact = models.BooleanField(default=False, verbose_name="Has impact on payslip?")

    def __str__(self):
        return self.parent.get_full_name()
    
    
    class Meta:
        ordering = "-pk",
        verbose_name = "Child"
        verbose_name_plural = "Children"
