from django.db import models
from apps.users.models import Monitor
from apps.consortia.models import Consortium
from apps.municipalities.models import Municipality


class Form1(models.Model):
    FINAL_DESTINATION_CHOICES = [
        ('landfill', 'Aterro'),
        ('dump', 'Lixão'),
        ('none', 'Sem destinação'),
    ]

    user = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name="recyclable_compositions", verbose_name="User")
    consortium = models.ForeignKey(Consortium, on_delete=models.CASCADE, related_name="recyclable_compositions", verbose_name="Consortium")
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name="recyclable_compositions", verbose_name="Municipality")
    # 1 - Data (Data)
    start_date = models.DateField()  # Data de início
    end_date = models.DateField()    # Data de término

    # 2 - Informe o CEP (CEP)
    zip_code = models.CharField(max_length=10)  # CEP

    # 3 - Sua cidade possui destinação final dos resíduos sólidos (Landfill, Dump, No destination)
    final_destination = models.CharField(
        max_length=10,
        choices=FINAL_DESTINATION_CHOICES,
        default='none',
        verbose_name="Final Destination"
    )

    # 4 - A cidade possui coleta seletiva? (Sim/Não)
    selective_collection = models.BooleanField()  # Coleta seletiva

    # 5 - Qual a média per capita de geração de resíduos por habitante (ton/habitante/dia)
    average_waste_per_capita = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)  # Média per capita (ton/habitante/dia)

    # 6 - Média per capita em toneladas de resíduos secos, orgânicos e rejeitos
    dry_waste_per_capita = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)      # Secos
    organic_waste_per_capita = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)   # Orgânico
    reject_waste_per_capita = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)    # Rejeito

    # 7 - Valor médio pago por tonelada de resíduos sólidos urbanos
    average_payment_per_ton = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Valor médio pago por tonelada
    dont_know_payment = models.BooleanField(default=False)  # Não sei informar

    # 8 - Sua cidade possui algum programa de reciclagem? (Sim/Não)
    has_recycling_program = models.BooleanField()  # Programa de reciclagem

    # 9 - Informe qual programa de reciclagem
    recycling_program_info = models.CharField(max_length=255, null=True, blank=True)  # Nome do programa de reciclagem

    # 10 - Qual associação de catadores
    scavenger_association = models.CharField(max_length=255, null=True, blank=True)  # Associação de catadores

    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação

    def __str__(self):
        return f"Survey {self.zip_code} ({self.start_date} - {self.end_date})"

    class Meta:
        verbose_name = "Recyclable Composition"
        verbose_name_plural = "Recyclable Compositions"