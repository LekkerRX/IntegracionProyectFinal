from django import forms
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from .models import Credencial, Oficio

# Validador para limitar el tipo de archivo
def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5 MB
    if value.size > limit:
        raise ValidationError("El archivo es demasiado grande. El límite es de 5 MB.")
    return value

# Formulario para subir credenciales
class CredencialForm(forms.ModelForm):
    class Meta:
        model = Credencial
        fields = ['oficio', 'documento']
        widgets = {
            'oficio': forms.Select(attrs={'class': 'form-select'}),
            'documento': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }

    # Agregar el validador para el archivo
    documento = forms.FileField(
        validators=[validate_file_size],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    # Validar si se sube un tipo de archivo permitido (por ejemplo, PDF y JPEG)
    def clean_documento(self):
        file = self.cleaned_data.get('documento')
        if file:
            if not file.name.endswith(('pdf', 'jpg', 'jpeg', 'png')):
                raise ValidationError('El archivo debe ser un PDF o una imagen JPG/PNG.')
        return file
