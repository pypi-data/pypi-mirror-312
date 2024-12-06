from django.db import models

# Create your models here.


class Country(models.Model):
    country_name = models.CharField(verbose_name="Country name", max_length=152)

    def __str__(self):
        return self.country_name


class City(models.Model):
    city_name = models.CharField(verbose_name="City name", max_length=152)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.city_name 
    

class Street(models.Model):
    street_name = models.CharField(verbose_name="Street name", max_length=128)
    city = models.ManyToManyField(City)

    def __str__(self):
        return self.street_name