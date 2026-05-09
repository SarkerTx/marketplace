from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import CustomerSignUpForm, VendorSignUpForm
from .models import User

class CustomerRegisterView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')   # or show a success message

class VendorRegisterView(CreateView):
    model = User
    form_class = VendorSignUpForm
    template_name = 'accounts/vendor_register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')