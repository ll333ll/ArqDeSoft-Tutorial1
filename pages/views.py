from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View
from django import forms

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Plug&Ad",
            "subtitle": "About us",
            "description": "Automatizamos campañas publicitarias con tecnología y diseño.",
            "author": "Developed by: Jose Alejandro Jiménez Vásquez",
        })
        return context

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact - Plug&Ad",
            "subtitle": "Contact us",
            "email": "jose@plugandad.com",
            "address": "Carrera 69 West, Medellín",
            "phone": "+57 3000000000",
        })
        return context

class Product:
    products = [
        {"id":"1", "name":"Campaña Express", "description":"Publicidad rápida para eventos urgentes", "price": 1200.0},
        {"id":"2", "name":"Meta Ads Pro", "description":"Campaña completa en Facebook e Instagram", "price": 2100.0},
        {"id":"3", "name":"Google Smart", "description":"Optimización automatizada en Google", "price": 980.0},
        {"id":"4", "name":"TikTok Viral", "description":"Viralización orgánica + pagos estratégicos", "price": 1300.0}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'
    
    def get(self, request):
        viewData = {}
        viewData["title"] = "Servicios - Plug&Ad"
        viewData["subtitle"] = "Lista de servicios"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'
    
    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1 or product_id > len(Product.products):
                return HttpResponseRedirect('/')
            
            viewData = {}
            product = Product.products[product_id-1]
            viewData["title"] = product["name"] + " - Plug&Ad"
            viewData["subtitle"] = product["name"] + " - Información del servicio"
            viewData["product"] = product
            return render(request, self.template_name, viewData)
        except (ValueError, IndexError):
            return HttpResponseRedirect('/')

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'
    
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create service"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            # Simular guardado exitoso
            viewData = {}
            viewData["title"] = "Service Created"
            viewData["message"] = "Service created successfully!"
            return render(request, 'products/create.html', viewData)
        else:
            viewData = {}
            viewData["title"] = "Create service"
            viewData["form"] = form
            return render(request, self.template_name, viewData)