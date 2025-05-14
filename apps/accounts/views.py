
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from datetime import timedelta
from rest_framework.views import APIView
from django.utils.html import strip_tags
from django.utils.timezone import now
from .models import VerificationCode
from .utils import send_sms_twilio 
from django.utils import timezone
from drf_yasg import openapi
from .serializers import *
import secrets
import hashlib
from django.shortcuts import get_object_or_404

from apps.users.models import UserResetPassword
from apps.users.models import CustomUser
from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    PasswordResetConfirmSerializer,
    PhoneNumberSerializer,
    VerificationCodeSerializer
)


class TokenObtainPairViewCustom(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TokenObtainPairSerializerCustom


class TokenRefreshViewCustom(TokenRefreshView):
    pass


class BlackListRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(data={'message': 'Refresh token revoked'}, status=status.HTTP_204_NO_CONTENT)
        except TokenError:
            return Response(data={'detail': 'Invalid or expired refresh token'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(request_body=ChangePasswordSerializer,
                         responses={status.HTTP_200_OK: ChangePasswordResponseSerializer})
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=self.request.user,
                          validated_data=serializer.validated_data)

        return Response(serializer.data)


class SendVerificationCodeView(APIView):
    """Endpoint para enviar um código de verificação via SMS."""

    @swagger_auto_schema(
        request_body=PhoneNumberSerializer,
        responses={
            200: openapi.Response(
                description="Código enviado com sucesso.",
                examples={"application/json": {"message": "Código enviado com sucesso."}}
            ),
            400: openapi.Response(
                description="Erro de validação",
                examples={"application/json": {"error": "Número de telefone inválido."}}
            )
        }
    )
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']    
            code = VerificationCode.generate_verification_code()
            VerificationCode.objects.create(phone_number=phone_number, code=code)

            try:
                response_sid = send_sms_twilio(phone_number, code)
                return Response({'message': 'Código enviado com sucesso.', 'twilio_sid': response_sid}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'Falha ao enviar SMS: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateVerificationCodeView(APIView):
    """Endpoint para validar um código de verificação enviado por SMS."""

    @swagger_auto_schema(
        request_body=VerificationCodeSerializer,
        responses={
            200: openapi.Response(
                description="Código validado com sucesso!",
                examples={"application/json": {"message": "Código validado com sucesso!"}}
            ),
            400: openapi.Response(
                description="Código inválido ou expirado",
                examples={"application/json": {"error": "Código inválido ou expirado."}}
            )
        }
    )
    def post(self, request):
        serializer = VerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']

            verification_code = VerificationCode.objects.filter(
                phone_number=phone_number,
                is_valid=True,
                code=code
            ).first()

            if verification_code is None:
                return Response({'error': 'Nenhum código válido encontrado para este número.'}, status=status.HTTP_400_BAD_REQUEST)

            if not verification_code.check_code(code):
                return Response({'error': 'Código incorreto.'}, status=status.HTTP_400_BAD_REQUEST)

            if not verification_code.is_valid_code():
                return Response({'error': 'Código expirado.'}, status=status.HTTP_400_BAD_REQUEST)

            VerificationCode.invalidate_all_codes(phone_number)

            return Response({'message': 'Código validado com sucesso!'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetRequestView(APIView):

    @swagger_auto_schema(
        operation_description="Solicita o envio de um código de redefinição de senha para o e-mail fornecido. O código será válido por 20 minutos.",
        request_body=PasswordResetRequestSerializer,
        responses={200: "Código enviado por e-mail.", 404: "Usuário não encontrado."}
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)

                # Gerando código de redefinição de senha
                reset_code = get_random_string(6, allowed_chars='0123456789')
                reset_code_expiration = timezone.now() + timedelta(minutes=20)

                # Salvando ou atualizando o código no banco
                UserResetPassword.objects.update_or_create(
                    user=user,
                    defaults={
                        'reset_code': reset_code,
                        'reset_code_expiration': reset_code_expiration
                    }
                )

                context = {
                    "user": user,
                    "reset_code": reset_code
                }
                html_message = render_to_string("password_reset.html", context)
                plain_message = strip_tags(html_message)  # Gerando versão texto do e-mail

                # Criando e enviando o e-mail
                subject = "Redefinição de Senha - Ecomonitor"
                from_email = "daviteixeira077@gmail.com"
                recipient_list = [user.email]

                email_message = EmailMultiAlternatives(
                    subject=subject,
                    body=plain_message,
                    from_email=from_email,
                    to=recipient_list
                )
                email_message.attach_alternative(html_message, "text/html")
                email_message.send()

                return Response({"message": "Código enviado por e-mail."}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerifyView(APIView):

    @swagger_auto_schema(
        operation_description="Verifica o código de redefinição de senha enviado para o e-mail. O código deve ser válido e não expirado.",
        request_body=PasswordResetVerifySerializer,
        responses={200: "Código verificado com sucesso.", 400: "Código inválido ou expirado.", 404: "Usuário não encontrado."}
    )
    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)
        if serializer.is_valid():       
            email = serializer.validated_data['email']
            reset_code = serializer.validated_data['reset_code']
            try:
                user = CustomUser.objects.get(email=email)
                user_reset = UserResetPassword.objects.get(user=user)
                
                if user_reset.reset_code == reset_code and timezone.now() < user_reset.reset_code_expiration:
                    return Response({"message": "Código verificado com sucesso."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Código inválido ou expirado."}, status=status.HTTP_400_BAD_REQUEST)
            except CustomUser.DoesNotExist:
                return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
            except UserResetPassword.DoesNotExist:
                return Response({"error": "Nenhum código encontrado para este usuário."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):

    @swagger_auto_schema(
        operation_description="Redefine a senha do usuário com base no e-mail. A nova senha deve ser fornecida e será aplicada imediatamente.",
        request_body=PasswordResetConfirmSerializer,
        responses={200: "Senha redefinida com sucesso.", 400: "Erro na requisição."}
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
           
            try:
                user = CustomUser.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                
                return Response({"message": "Senha redefinida com sucesso."}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
