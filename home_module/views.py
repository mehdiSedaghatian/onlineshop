from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from home_module.forms import SearchForm
from utils.convertors import group_list
from product_module.models import Product, ProductCategory
from site_module.models import SiteSetting, FooterLinkBox, FooterLink, Slider
from utils.http_service import get_client_ip


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sliders: Slider = Slider.objects.filter(is_active=True)
        context['sliders'] = sliders
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
        context['latest_products'] = group_list(latest_products)
        most_visit_products = Product.objects.filter(is_active=True, is_delete=False).annotate(visit_count=Count('productvisit')).order_by('-visit_count')
        context['most_visit_products'] = group_list(most_visit_products)
        categories = list(ProductCategory.objects.annotate(product_count=Count('product_categories')).filter(is_active=True, is_delete=False, product_count__gt=0)[:6])
        categories_products = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.product_categories.all()[:4])
            }
            categories_products.append(item)
        context['categories_products'] = categories_products
        most_bought_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum(
            'orderdetail__count'
        )).order_by('-order_count')[:12]
        context['most_bought_products'] = group_list(most_bought_products)
        return context


class AboutView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting
        return context


def site_header_component(request):
    site_setting = SiteSetting.objects.filter(is_main_setting=True).first()

    context = {
        'site_setting': site_setting,
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxes: FooterLinkBox = FooterLinkBox.objects.all()
    for item in footer_link_boxes:
        item.footerlink_set

    context = {
        'site_setting': site_setting,
        'footer_link_boxes': footer_link_boxes,

    }
    return render(request, 'shared/site_footer_component.html', context)


class Page404(TemplateView):
    template_name = 'home_module/not-yet-completed.html'


class SearchProductsView(View):
    def get(self, request):
        form = SearchForm()
        products = Product.objects.filter(is_active=True, is_delete=False)

        context = {
            'form': form,
            'products': products
        }
        return render(request, 'home_module/search_products.html', context)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            products=Product.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
            context = {
                'form': form,
                'products': products
            }
            return render(request,'home_module/search_products.html',context)
        form = SearchForm()
        products = Product.objects.filter(is_active=True, is_delete=False)

        context = {
            'form': form,
            'products': products
        }
        return render(request, 'home_module/search_products.html', context)
