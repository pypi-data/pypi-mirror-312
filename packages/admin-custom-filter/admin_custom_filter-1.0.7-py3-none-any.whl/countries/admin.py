from django.contrib import admin
from admin_custom_filter.admin_filter import AdminCustomFilter
from .models import Country, City, Street
# Register your models here.

class CountryAdmin(AdminCustomFilter):
    list_display = ["country_name"]

class CityAdmin(AdminCustomFilter):
    list_display = ["city_name"]

class StreetAdmin(AdminCustomFilter):
    list_display = ["street_name"]



admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Street, StreetAdmin)