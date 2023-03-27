from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView
from account_module.models import User
from order_module.models import Order, OrderDetail
from .forms import EditProfileModelForm, ChangePasswordForm


# Create your views here.
@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'


@login_required
def user_panel_menu_component(request: HttpRequest):
    return render(request, 'user_panel_module/components/user_panel_menu_component.html')


@method_decorator(login_required, name='dispatch')
class EditUserProfilePage(View):
    def get(self, request: HttpRequest):
        current = User.objects.filter(id=request.user.id).first()
        edit_profile = EditProfileModelForm(instance=current)
        context = {
            'edit_profile': edit_profile,
            'current_user': current
        }

        return render(request, 'user_panel_module/edit_profile_page.html', context)

    def post(self, request: HttpRequest):
        current = User.objects.filter(id=request.user.id).first()
        edit_profile = EditProfileModelForm(request.POST, request.FILES, instance=current)
        if edit_profile.is_valid():
            edit_profile.save(commit=True)
        context = {
            'edit_profile': edit_profile
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)


@method_decorator(login_required, name='dispatch')
class ChangePasswordPage(View):
    def get(self, request: HttpRequest):
        change_password_form = ChangePasswordForm()
        context = {
            'change_password_form': change_password_form
        }
        return render(request, 'user_panel_module/change_password_page.html', context)

    def post(self, request: HttpRequest):
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(change_password_form.cleaned_data.get('old_password')):
                current_user.set_password(change_password_form.cleaned_data.get('new_password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))



            else:
                change_password_form.add_error('old_password', 'current password is wrong')

        context = {
            'change_password_form': change_password_form
        }
        return render(request, 'user_panel_module/change_password_page.html', context)


@login_required
def user_basket(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
    total_amount = total_amount = current_order.calculate_total_price()

    context = {

        'order': current_order,
        'sum': total_amount,
    }

    return render(request, 'user_panel_module/user_basket.html', context)




@login_required
def user_remove_order(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False, order__user_id=request.user.id).delete()
    if deleted_count == 0:
        return JsonResponse({
            'status': 'not_found_detail'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)

    total_amount = current_order.calculate_total_price()

    context = {

        'order': current_order,
        'sum': total_amount,
    }
    data = render_to_string('user_panel_module/user_basket_content.html', context)

    return JsonResponse({
        'status': 'success',
        'body': data
    })


@login_required
def change_order_detail_count(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_id_and_state'
        })
    order_detail = OrderDetail.objects.filter(id=detail_id, order__is_paid=False, order__user_id=request.user.id).first()
    if order_detail is None:
        return JsonResponse({
            'status': 'not_found_detail'
        })
    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()

        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state invalid'
        })
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)

    total_amount = current_order.calculate_total_price()

    context = {

        'order': current_order,
        'sum': total_amount,
    }
    data = render_to_string('user_panel_module/user_basket_content.html', context)

    return JsonResponse({
        'status': 'success',
        'body': data
    })


@method_decorator(login_required, name='dispatch')
class MySopping(ListView):
    template_name = 'user_panel_module/user_shopping.html'
    model = Order

    def get_queryset(self):
        queryset = super(MySopping, self).get_queryset()
        request: HttpRequest = self.request
        queryset = queryset.filter(user_id=request.user.id, is_paid=True)
        return queryset


def my_shopping_detail(request: HttpRequest, order_id):
    order = Order.objects.prefetch_related('orderdetail_set').filter(id=order_id, user_id=request.user.id, is_paid=True).first()
    if order is None:
        return Http404('a error is occurred')
    context = {
        'order': order
    }
    return render(request, 'user_panel_module/user_shopping_detail.html', context)
