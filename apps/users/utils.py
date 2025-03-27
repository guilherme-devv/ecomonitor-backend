# from rest_framework.exceptions import ValidationError
# import re

# def validate_cpf(value):
#     # Remove caracteres não numéricos
#     cpf = re.sub(r'[^0-9]', '', value)
    
#     # Verifica se o CPF contém exatamente 11 dígitos numéricos após a remoção dos caracteres não numéricos
#     if not re.match(r'^\d{11}$', cpf):
#         raise ValidationError('CPF deve conter exatamente 11 dígitos numéricos.')
    
#     # Verifica se todos os números do CPF são iguais (ex.: 111.111.111-11)
#     if cpf == cpf[0] * 11:
#         raise ValidationError('CPF inválido.')
    
#     # Validação dos dígitos verificadores
#     for i in range(9, 11):
#         value_sum = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
#         digit = ((value_sum * 10) % 11) % 10
#         if digit != int(cpf[i]):
#             raise ValidationError('CPF inválido.')

#     # Se passar por todas as validações, retorna o CPF formatado (opcional)
#     return value

# def validate_number_of_phone(value):
#     phone = re.sub(r'[^0-9]', '', value)  # Remove caracteres não numéricos
#     if not re.match(r'^\d{10,11}$', phone):  # Aceita telefones de 10 ou 11 dígitos
#         raise ValidationError('Número de telefone deve conter 10 ou 11 dígitos.')
#     return value
