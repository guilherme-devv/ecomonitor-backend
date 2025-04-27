from django.db import models
from ..consortia.models import Consortium


class Municipality(models.Model):
    name = models.CharField(max_length=255, verbose_name="Municipality Name")
    consortium = models.ForeignKey(Consortium, on_delete=models.SET_NULL, null=True, blank=True, related_name='municipalities')
    population = models.PositiveIntegerField(null=True, blank=True, help_text="Total population")
    per_capita = models.FloatField(null=True, blank=True, help_text="Per capita value")
    solid_waste_generation_rate = models.FloatField(null=True, blank=True, help_text="Rate of solid waste generation")
    service_coverage_rate = models.FloatField(null=True, blank=True, help_text="Service coverage rate")
    total_generated_waste_tpd = models.FloatField(null=True, blank=True, help_text="Total generated waste (tons/day)")
    collection_coverage_rate_total_population = models.FloatField(null=True, blank=True, help_text="Collection coverage rate relative to total population")
    collection_coverage_rate_urban_population = models.FloatField(null=True, blank=True, help_text="Collection coverage rate relative to urban population")
    per_capita_rsu_expenses_per_inhabitant = models.FloatField(null=True, blank=True, help_text="RSU expenses per inhabitant")
    per_capita_rsu_expenses_total_population = models.FloatField(null=True, blank=True, help_text="RSU expenses per total population")
    collection_unit_cost = models.FloatField(null=True, blank=True, help_text="Unit cost of waste collection")
    tons_per_km_collected = models.FloatField(null=True, blank=True, help_text="Tons collected per kilometer")
    tons_per_collection_sector = models.FloatField(null=True, blank=True, help_text="Tons collected per collection sector")
    per_capita_recovered_mass = models.FloatField(null=True, blank=True, help_text="Recovered mass per capita")
    apparent_density = models.FloatField(null=True, blank=True, help_text="Apparent specific weight or density")
    waste_disposed_in_landfill_or_dump = models.FloatField(null=True, blank=True, help_text="Waste disposed in landfill or dump (tons)")
    waste_to_gdp_per_capita_ratio = models.FloatField(null=True, blank=True, help_text="Ratio between waste and GDP per capita")
    total_generated_waste = models.FloatField(null=True, blank=True, help_text="Total solid waste generated (tons)")

    class Meta:
        verbose_name = "Municipality"
        verbose_name_plural = "Municipalities"

    def __str__(self):
        return self.name
