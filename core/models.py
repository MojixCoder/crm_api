from django.db import models

# Create your models here.

class DateModel(models.Model):
    """ Date Model """
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")
    
    
    class Meta:
        abstract = True


class Section(DateModel):
    """ Section Model """
    
    # Section Information
    title = models.CharField(max_length=255, unique=True, verbose_name="Title")

    def __str__(self):
        return self.title

    
    class Meta:
        ordering = "-pk",
        verbose_name = "Section"
        verbose_name_plural = "Sections"


class Role(DateModel):
    """ Role Model """
    
    # Foreign Keys
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="roles", verbose_name="Section")

    # Role Information
    title   = models.CharField(max_length=255, verbose_name="Title")

    def __str__(self):
        return f"{self.section.title}-{self.title}"

    
    class Meta:
        ordering = "-pk",
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        
        
class Permission(DateModel):
    """
    Permission of Users
    """
    # Foreign Key
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="permissions", verbose_name="Section")
    
    # Permission Information
    title   = models.CharField(max_length=255, verbose_name="Title")

    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"


class WorkGroup(DateModel):
    """ Work Group Model """
    
    # Work Group Information
    title       = models.CharField(max_length=255, verbose_name="Title")
    daily       = models.IntegerField(verbose_name="Daily")
    overtime    = models.IntegerField(verbose_name="Overtime")
    has_payslip = models.BooleanField(default=False, verbose_name="Has payslip")

    def __str__(self):
        return self.title

    
    class Meta:
        ordering = "-pk",
        verbose_name = "Work Group"
        verbose_name_plural = "Work Groups"


class Bank(DateModel):
    """ Bank Model """
    # Bank Information
    icon    = models.ImageField(upload_to="bank/", verbose_name="Icon")
    name    = models.CharField(max_length=255, unique=True, verbose_name="Name")

    def __str__(self):
        return self.name


    class Meta:
        ordering = "-pk",
        verbose_name = "Bank"
        verbose_name_plural = "Banks"


class Year(DateModel):
    """ Year Model """
    
    # Year Information
    year = models.IntegerField(unique=True, verbose_name="Year")

    def __str__(self):
        return f"{self.year}"

    
    class Meta:
        ordering = "pk",
        verbose_name = "Year"
        verbose_name_plural = "Years"


class Month(DateModel):
    """ Month Model """
    
    # Foreign Keys
    year         = models.ForeignKey(Year, on_delete=models.CASCADE, related_name="months", verbose_name="Year")
    
    # Month Information
    title        = models.CharField(max_length=255, verbose_name="title")
    month_number = models.IntegerField(verbose_name="Month number")
    days         = models.IntegerField(verbose_name="Number of days")

    def __str__(self):
        return f"{self.title} {self.year.year}"
    

    class Meta:
        ordering = "pk",
        verbose_name = "Month"
        verbose_name_plural = "Months"
        constraints = [
            models.UniqueConstraint(fields=["year", "month_number"], name='year_month_unique')
        ]


class Province(DateModel):
    """ Province Model """
    
    # Province Information
    name = models.CharField(max_length=100, unique=True, verbose_name="Province name")
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        ordering = "name",
        verbose_name = "Province"
        verbose_name_plural = "Provinces"
        
        
class City(DateModel):
    """ City Model """
    
    # Foreign Keys
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cities", verbose_name="Province")
    
    # City Information
    name     = models.CharField(max_length=100, verbose_name="City name")
    
    def __str__(self):
        return self.city
    
    
    class Meta:
        ordering = "province", "name",
        verbose_name = "City"
        verbose_name_plural = "Cities"


class BankBranch(DateModel):
    """ Branch of banks """
    
    # Foreign Keys
    bank            = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="bank_branchs", verbose_name="Bank")
    city            = models.ForeignKey(City, on_delete=models.CASCADE, related_name="bank_branchs", verbose_name="City")
    
    # Bank Branch Information
    name            = models.CharField(max_length=255, verbose_name="Branch name")
    branch_code     = models.CharField(max_length=10, verbose_name="Branch code")
    address         = models.TextField(verbose_name="Address")
    tel             = models.CharField(max_length=30, blank=True, verbose_name="Telephone")
    description     = models.TextField(blank=True, verbose_name="Description")
    manager_name    = models.CharField(max_length=255, blank=True, verbose_name="Manager name")
    fax_number      = models.CharField(max_length=255, blank=True, verbose_name="Fax number")
    manager_number  = models.CharField(max_length=255, blank=True, verbose_name="Manager phone number")
    
    def __str__(self):
        return f"{self.bank.name}-{self.name}-{self.branch_code}"


    class Meta:
        ordering = "bank", "-pk",
        verbose_name = "Bank Branch"
        verbose_name_plural = "Bank Branchs"
        constraints = [
            models.UniqueConstraint(fields=['branch_code', 'bank'], name='unique_branch_code_bank')
        ]


class Branch(DateModel):
    """ Branch Model """
    
    TYPE_CHOICES = (
        (1, "Branch"),
        (2, "Sales Agent"),
    )
    # Foreign Keys
    city        = models.ForeignKey(City, on_delete=models.CASCADE, related_name="branchs", verbose_name="City")
    
    # Branch Information
    name        = models.CharField(max_length=255, blank=True, verbose_name="Branch name")
    first_name  = models.CharField(max_length=255, verbose_name="Manager first name")
    last_name   = models.CharField(max_length=255, verbose_name="Manager last name")
    what_type   = models.IntegerField(choices=TYPE_CHOICES, default=1, verbose_name="Branch type")
    tel1        = models.CharField(max_length=100, verbose_name="Tel1")
    tel2        = models.CharField(max_length=100, blank=True, verbose_name="Tel2")
    address     = models.TextField(verbose_name="Address")
    
    def __str__(self):
        return self.title or ""
    
    
    class Meta:
        ordering = "-pk",
        verbose_name = "Branch"
        verbose_name_plural = "Branchs"
