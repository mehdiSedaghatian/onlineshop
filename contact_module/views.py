from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView

from site_module.models import SiteSetting
from .forms import ContactUsModelForm
from .models import ContactUs, UserProfile


# Create your views here.


class ContactUsView(CreateView):
    template_name = 'contact_module/contact_us_page.html'
    form_class = ContactUsModelForm
    success_url = '/contact-us/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting
        return context

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)

    # def get(self, request):
    #     contact_form = ContactUsModelForm()
    #     return render(request, 'contact_module/contact_us_page.html', {'contact_form': contact_form})
    #
    # def post(self, request):
    #     contact_form = ContactUsModelForm(request.POST)
    #     if contact_form.is_valid():
    #         contact_form.save()
    #         return redirect('home_page')
    #
    #     contact_form = ContactUsModelForm()
    #     return render(request, 'contact_module/contact_us_page.html', {'contact_form': contact_form})


# def contact_us_page(request):
#     if request.method == 'POST':
#         contact_form = ContactUsModelForm(request.POST)
#         if contact_form.is_valid():
#             contact_form.save()
#             return redirect('home_page')
#
#     else:
#         contact_form = ContactUsModelForm()
#     return render(request, 'contact_module/contact_us_page.html', {'contact_form': contact_form})


class CreateProfileView(CreateView):
    template_name = 'contact_module/create_profile_page.html'
    success_url = '/products/'
    model = UserProfile
    fields = ['image']

    # def get(self, request):
    #     form = ProfileForm()
    #     context = {
    #         'form': form
    #     }
    #     return render(request, 'contact_module/create_profile_page.html', context)
    #
    # def post(self, request):
    #     submitted_form = ProfileForm(request.POST, request.FILES)
    #     if submitted_form.is_valid():
    #         profile = UserProfile(image=request.FILES['user_image'])
    #         profile.save()
    #         return redirect('home_page')
    #
    #     context = {
    #         'form': submitted_form
    #     }
    #     return render(request, 'contact_module/create_profile_page.html', context)


class ProfilesView(ListView):
    template_name = 'contact_module/profiles_list_page.html'
    model = UserProfile
    context_object_name = 'profiles'
