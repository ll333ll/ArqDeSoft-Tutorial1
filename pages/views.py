from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views import View
from django import forms
from .models import AdPackage

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Sobre Plug&Ad",
            "subtitle": "Nuestra Misión",
            "description": "Automatizamos campañas publicitarias con tecnología y diseño.",
            "author": "Jose Alejandro Jiménez Vásquez",
        })
        return context

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

class ProductForm(forms.ModelForm):
    class Meta:
        model = AdPackage
        fields = ['name', 'description', 'price']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return price

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        products = AdPackage.objects.all()
        return render(request, self.template_name, {
            "title": "Servicios Publicitarios – Plug&Ad",
            "subtitle": "Paquetes disponibles",
            "products": products
        })

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product = AdPackage.objects.get(id=id)
        except AdPackage.DoesNotExist:
            return HttpResponseRedirect(reverse('home'))

        return render(request, self.template_name, {
            "title": f"{product.name} – Plug&Ad",
            "subtitle": f"Información del paquete {product.name}",
            "product": product
        })

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        return render(request, self.template_name, {
            "title": "Registrar nuevo paquete",
            "form": ProductForm()
        })

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'products/product_created.html', {"title": "Paquete registrado exitosamente"})
        return render(request, self.template_name, {"title": "Registrar nuevo paquete", "form": form})
