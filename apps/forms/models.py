from django.db import models
from apps.users.models import Monitor
from apps.consortia.models import Consortium
from apps.municipalities.models import Municipality


class RecyclableWasteComposition(models.Model):

    user = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name="recyclable_compositions", verbose_name="User")
    consortium = models.ForeignKey(Consortium, on_delete=models.CASCADE, related_name="recyclable_compositions", verbose_name="Consortium")
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name="recyclable_compositions", verbose_name="Municipality")
    created_at = models.DateTimeField(auto_now_add=True)
    quantity_tetrapak = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_aluminum = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_white_paper = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_colored_paper = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_cardboard = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_newspaper = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_general_plastic = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_film_plastic = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_pet = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_pvc = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.total} kg of recyclable waste collected by {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Recyclable Composition"
        verbose_name_plural = "Recyclable Compositions"