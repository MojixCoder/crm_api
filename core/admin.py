from django.contrib import admin
from .models import Bank, BankBranch, Branch, City, Month, Permission, Province, Role, Section, WorkGroup, Year

# Register your models here.

admin.site.register(Bank)
admin.site.register(BankBranch)
admin.site.register(Branch)
admin.site.register(City)
admin.site.register(Month)
admin.site.register(Permission)
admin.site.register(Province)

class SectionAdmin(admin.ModelAdmin):
    search_fields = ["title"]

admin.site.register(Section, SectionAdmin)

class RoleAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    autocomplete_fields = ["section"]
    
admin.site.register(Role, RoleAdmin)
admin.site.register(WorkGroup)
admin.site.register(Year)
