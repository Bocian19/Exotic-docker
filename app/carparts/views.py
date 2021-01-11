
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.loader import render_to_string, get_template
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView
from carparts.forms import OrderForm, SubscribeForm
from carparts.models import Product, Logo, PRODUCER, Bodykit, SubscribeModel
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from Exotic.settings import EMAIL_HOST_USER
from django.utils.encoding import force_text
import datetime

from carparts.tokens import account_activation_token


class HomeView(View):

    def get(self, request):
        # form = SubscribeForm()
        if request.method == "GET":
            products = Product.objects.all().order_by('-id')[:20]
            range_times = range(19)
            entry_products = products[:6]
            paginator = Paginator(products, 1)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            logos = Logo.objects.all()

            return render(request, 'index.html', {'page_obj': page_obj, 'logos': logos, 'range_times':range_times,
                                              'entry_products': entry_products})


class LoadHiddenView(View):

    def get(self, request):
            products = Product.objects.all().order_by('-id')[:20]
            paginator = Paginator(products, 1)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, 'hidden_product.html', {'page_obj': page_obj})


class ProductView(DetailView):

    model = Product
    query_pk_and_slug = True
    form = OrderForm

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['form'] = OrderForm

        return context

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            code = form.cleaned_data['post_code']
            current_site = get_current_site(request)
            slug = kwargs.get('slug')
            subject = 'Подтверждение заказа'
            recepient = form.cleaned_data['email']
            message = render_to_string('email_message.html', {
                'user': username,
                'domain': current_site.domain,
                'link_to_item': current_site,
                'phone_number': phone_number,
                'city': city,
                'street': street,
                'code': code,
                'slug': slug,
                'recepient': recepient

             })
            admin_email = 'exoticparts.eu@gmail.com'
            send_mail(subject,
                      message, EMAIL_HOST_USER, [recepient, admin_email], fail_silently=False)
            message = 'Спасибо за заказ. Ваш заказ отправлен нам а также на вашу электронную почту отправлено подтверждение.' \
                      ' Мы свяжемся с вами в ближайшее время для уточнения деталей сделки.'\
                        ' С уважением.'
            return redirect(request, 'kontakt.html', {'message': message}, *args)

        return redirect(request.META['HTTP_REFERER'])




class ProductsView(View):

    def get(self, request):

        products = Product.objects.all().order_by('-id')

        paginator = Paginator(products, 20)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'products.html', {'page_obj': page_obj, 'producers': PRODUCER})

    def post(self, request):

        if request.method == "POST":
            brand = request.POST.get('brand')
            products = Product.objects.all().filter(producer=brand).order_by('-price')

            return render(request, 'products.html', {'products': products, 'producers': PRODUCER, 'brand': brand})


class ContactView(View):

    def get(self, request):

        return render(request, 'kontakt.html')


class AboutView(View):

    def get(self, request):

        return render(request, 'about.html')


class BodykitsView(View):

    def get(self, request):
        bodykits_images = Bodykit.objects.all()
        return render(request, 'bodykits.html', {'bodykits_images': bodykits_images})


class SubscribeView(View):

    def get(self, request):
        if request.method == "GET":
            return HttpResponseNotFound('<h1>Page not found</h1>')

    def post(self, request):
        if request.method == "POST":
            form = SubscribeForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                try:
                    user = SubscribeModel.objects.get(email=email)
                except SubscribeModel.DoesNotExist:
                    user = None
                if user is not None:
                    return redirect(request.META['HTTP_REFERER'])
                else:
                    if email:
                        new_user = SubscribeModel.objects.create(email=email)
                        new_user.is_active = False
                        new_user.save()
                        current_site = get_current_site(request)
                        subject = 'Подписка на сайте Exoticparts.eu'
                        text_content = render_to_string('activation_email.html')
                        context = {
                            'user': new_user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                            'token': account_activation_token.make_token(new_user),
                        }

                        to_email = email
                        html_content = get_template('activation_email.html').render(context)

                        msg = EmailMultiAlternatives(subject,
                                  text_content, EMAIL_HOST_USER, [to_email])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()

                        return redirect(request.META['HTTP_REFERER'])

            else:
                return redirect(request.META['HTTP_REFERER'])


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = SubscribeModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, SubscribeModel.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        conf_info = "Спасибо за подтверждение подписки."
        return render(request, 'kontakt.html', {'message': conf_info})
    else:
        message = 'Срок действия ссылки для активации истек.'
        return render(request, 'kontakt.html', {'message': message})





