from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from .models import Contact
from .forms import ContactForm

def contact_view(request: HttpRequest):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save() 
            
            # Send Confirmation Email
            content_html = render_to_string("contact/mail/confirmation.html", {'contact': contact})
            email_message = EmailMessage(
                subject="Confirmation",
                body=content_html,
                from_email=settings.EMAIL_HOST_USER,
                to=[contact.email]
            )
            email_message.content_subtype = "html"
            email_message.send()
            
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact:contact_view')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})



# Contact Us Messages page (admin or staff)
def contact_messages_view(request):
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'contact/contact_messages.html', {'contacts': contacts})