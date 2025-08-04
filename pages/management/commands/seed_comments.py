from django.core.management.base import BaseCommand
from pages.models import Product, Comment

class Command(BaseCommand):
    help = 'Seed the database with comments'

    def handle(self, *args, **kwargs):
        product = Product.objects.first()
        if product:
            Comment.objects.create(product=product, description='¡Excelente paquete de anuncios!')
            Comment.objects.create(product=product, description='Muy buena opción para mi negocio.')
            Comment.objects.create(product=product, description='Lo recomiendo totalmente.')
            self.stdout.write(self.style.SUCCESS('Comentarios sembrados exitosamente.'))
        else:
            self.stdout.write(self.style.WARNING('No hay productos para asociar comentarios.'))
