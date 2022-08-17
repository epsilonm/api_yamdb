from rest_framework import serializers


class UserNameValidator:
    """Валидатор для проверки, что пользователь не может выбрать имя 'me'."""
    def __init__(self, username='username'):
        self.username = username

    def __call__(self, attrs):
        if attrs[self.username] == 'me':
            raise serializers.ValidationError(
                f'{attrs[self.username]} - служебное имя. Выберите другое'
            )
        return True
