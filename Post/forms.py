from django import forms
from .models import Publicacion  # Asegúrate de que el modelo Localidad esté importado
from Oficio.models import Oficio
# Definir las comunas de Santiago como opciones para el campo localidad
COMUNAS_SANTIAGO = [
    ('Cerrillos', 'Cerrillos'),
    ('Cerro Navia', 'Cerro Navia'),
    ('Conchalí', 'Conchalí'),
    ('El Bosque', 'El Bosque'),
    ('Estación Central', 'Estación Central'),
    ('Huechuraba', 'Huechuraba'),
    ('Independencia', 'Independencia'),
    ('La Cisterna', 'La Cisterna'),
    ('La Florida', 'La Florida'),
    ('La Granja', 'La Granja'),
    ('La Pintana', 'La Pintana'),
    ('La Reina', 'La Reina'),
    ('Las Condes', 'Las Condes'),
    ('Lo Barnechea', 'Lo Barnechea'),
    ('Lo Espejo', 'Lo Espejo'),
    ('Lo Prado', 'Lo Prado'),
    ('Macul', 'Macul'),
    ('Maipú', 'Maipú'),
    ('Ñuñoa', 'Ñuñoa'),
    ('Pedro Aguirre Cerda', 'Pedro Aguirre Cerda'),
    ('Peñalolén', 'Peñalolén'),
    ('Providencia', 'Providencia'),
    ('Pudahuel', 'Pudahuel'),
    ('Quilicura', 'Quilicura'),
    ('Quinta Normal', 'Quinta Normal'),
    ('Recoleta', 'Recoleta'),
    ('Renca', 'Renca'),
    ('San Joaquín', 'San Joaquín'),
    ('San Miguel', 'San Miguel'),
    ('San Ramón', 'San Ramón'),
    ('Santiago', 'Santiago'),
    ('Vitacura', 'Vitacura'),
    ('Santiago Centro','Santiago Centro'),
    ('San Bernardo','San Bernardo'),
    ('Puente Alto','Puente Alto'),
    
]

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'descripcion', 'limite_monto', 'imagen', 'ubicacion','oficios']  # No incluimos 'cliente'

    # Campo de localidades con opciones de las comunas de Santiago
    ubicacion = forms.ChoiceField(
        choices=COMUNAS_SANTIAGO,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Comuna de Ubicación',
        error_messages={'required': 'El campo ubicación es obligatorio.'}
    )
    limite_monto = forms.FloatField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Límite de Monto',
        error_messages={'required': 'El campo limite de monto es obligatorio.'}
    )
    
    oficios = forms.ModelMultipleChoiceField(queryset=Oficio.objects.all(), required=True, widget=forms.CheckboxSelectMultiple(attrs={'id': 'oficios'}), error_messages={'required': 'El campo oficio es obligatorio.'})
    
    def __init__(self, *args, **kwargs):
        # Asegúrate de que el usuario se pase cuando se instancie el formulario
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Agregar clases de Bootstrap a los campos
        self.fields['titulo'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'style': 'max-height: 150px; overflow-y: scroll;', 'placeholder': 'Escribe una descripción aquí...'})
        self.fields['limite_monto'].widget.attrs.update({'class': 'form-control'})
        self.fields['imagen'].widget.attrs.update({'class': 'form-control'})
        
        
    def clean_limite_monto(self):
        # Obtener el valor ingresado para limite_monto
        monto = self.cleaned_data.get('limite_monto')
        
        # Validación: Si el monto es menor a 5000, lanzar un error
        if monto and monto < 5000:
            raise forms.ValidationError('El monto mínimo es 5.000 pesos chilenos.')
        
        return monto

    def save(self, commit=True):
        publicacion = super().save(commit=False)
        # Asocia el usuario al campo 'cliente'
        if self.user:
            publicacion.cliente = self.user
        if commit:
            publicacion.save()
        return publicacion

