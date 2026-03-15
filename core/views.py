from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import activate
from products.models import Product
from orders.models import ContactMessage


def home(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:6]
    return render(request, 'core/home.html', {
        'featured_products': featured_products,
    })


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', 'general')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )

        if request.LANGUAGE_CODE == 'mn':
            messages.success(request, 'Мессежийн төлөө баярлалаа! Бид удахгүй хариулна.')
        else:
            messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
        return redirect('core:contact')

    return render(request, 'core/contact.html')


def newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # TODO: Save to newsletter subscribers or send to email service
        if request.LANGUAGE_CODE == 'mn':
            messages.success(request, 'Бүртгүүлсэнд баярлалаа!')
        else:
            messages.success(request, 'Thank you for subscribing!')
    return redirect('core:home')


def set_language(request):
    """Switch between Mongolian and English"""
    lang = request.GET.get('lang', 'mn')
    next_url = request.GET.get('next', '/')

    # Activate the language
    activate(lang)

    response = redirect(next_url)
    response.set_cookie('django_language', lang, max_age=365*24*60*60)  # 1 year

    return response
