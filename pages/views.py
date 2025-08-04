from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from .models import Product

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Sobre Nosotros - Plug&Ad",
            "subtitle": "Sobre Nosotros",
            "description": "Automatizamos campañas publicitarias con tecnología y diseño.",
            "author": "Desarrollado por: Jose Alejandro Jiménez Vásquez",
        })
        return context

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contacto - Plug&Ad",
            "subtitle": "Contáctanos",
            "email": "jose@plugandad.com",
            "address": "Carrera 69 West, Medellín",
            "phone": "+57 3000000000",
        })
        return context

class ProductIndexView(View):
    template_name = 'products/index.html'
    
    def get(self, request):
        viewData = {}
        viewData["title"] = "Paquetes de Anuncios - Plug&Ad"
        viewData["subtitle"] = "Lista de Paquetes de Anuncios"
        viewData["products"] = Product.objects.all()
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        # Check if product id is valid
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("El ID del paquete de anuncios debe ser 1 o mayor")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            # If the product id is not valid, redirect to the home page
            return HttpResponseRedirect(reverse('home'))
        
        viewData = {}
        viewData["title"] = product.name + " - Plug&Ad"
        viewData["subtitle"] = product.name + " - Información del Paquete de Anuncios"
        viewData["product"] = product
        return render(request, self.template_name, viewData)

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products' # This will allow you to loop through 'products' in your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Paquetes de Anuncios - Plug&Ad'
        context['subtitle'] = 'Lista de Paquetes de Anuncios'
        return context

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price is not None and price <= 0:
            raise ValidationError('El precio debe ser mayor que cero.')
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'
    
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Crear Paquete de Anuncios"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Paquete de anuncios creado exitosamente!')
            return redirect('index') # Redirige a la lista de productos
        else:
            viewData = {}
            viewData["title"] = "Crear Paquete de Anuncios"
            viewData["form"] = form
            return render(request, self.template_name, viewData)

class ProductDeleteView(View):
    def post(self, request, id):
        product = get_object_or_404(Product, pk=id)
        product.delete()
        messages.success(request, '¡Paquete de anuncios eliminado exitosamente!')
        return redirect('index')

class ProductUpdateView(View):
    template_name = 'products/update.html'

    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        form = ProductForm(instance=product)
        viewData = {}
        viewData["title"] = "Actualizar Paquete de Anuncios"
        viewData["form"] = form
        viewData["product"] = product
        return render(request, self.template_name, viewData)

    def post(self, request, id):
        product = get_object_or_404(Product, pk=id)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Paquete de anuncios actualizado exitosamente!')
            return redirect('show', id=product.id)
        else:
            viewData = {}
            viewData["title"] = "Actualizar Paquete de Anuncios"
            viewData["form"] = form
            viewData["product"] = product
            return render(request, self.template_name, viewData)