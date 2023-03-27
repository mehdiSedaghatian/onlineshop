from django.db.models import Count, Q
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from product_module.models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery
from site_module.models import SiteBanner
from utils.convertors import group_list
from utils.http_service import get_client_ip


# Create your views here.


class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 100
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.SiteBannerPosition.product_list)
        # context['form'] = SearchForm()
        # if 'search' in self.request.GET:
        #     form = SearchForm(self.request.GET)
        #     cd = form.cleaned_data['search']
        #     products = Product.objects.filter(Q(title__icontains=cd) | Q(description__icontains=cd))
        #     context['form'] = form
        #     context['products'] = products
        #
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)
        if end_price is not None:
            query = query.filter(price__lte=end_price)
        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)
        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context['banners'] = SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.SiteBannerPosition.product_detail)
        product = self.object
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=product.id)
            new_visit.save()
        context['galleries'] = group_list(ProductGallery.objects.filter(product_id=product.id)[:6], 3)
        context['related_products'] = group_list(Product.objects.filter(brand_id=product.brand_id).exclude(pk=product.id).all()[:12])
        return context


class AddProductFavorite(View):
    def post(self, request):
        product_id = request.POST["product_id"]
        product = Product.objects.get(pk=product_id)
        request.session["product-favorite"] = product_id
        return redirect(product.get_absolute_url())


def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': product_categories
    }
    return render(request, 'product_module/components/product_categories_component.html', context)


def product_brand_component(request: HttpRequest):
    product_brand = ProductBrand.objects.annotate(product_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brand
    }
    return render(request, 'product_module/components/product_brand_component.html', context)

# def search(request):
#     form = SearchForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'product_module/product_list.html', context)
