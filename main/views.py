from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from . models import Route, Bus, Seat, Booking, Review
from userprofile.forms import CustomSignupForm, CustomSignupUpdateForm
from blog.models import Post, Category, Tag
from services.models import Service
from contact.models import FAQs
from . forms import ReviewForm, SuggestionBoxForm, ContactForm,PaymentForm
import requests
from django.conf import settings
import paymentwall




# MOMO_API_SECRET = 'a9553b3fa91a4463b3516d963b373e73'  # Use the Primary or Secondary key
# MOMO_API_URL = 'https://sandbox.momodeveloper.mtn.com'

# def get_momo_access_token():
#     """
#     Function to obtain the MoMo API access token.
#     """
#     url = f"{MOMO_API_URL}/collection/token/"
#     headers = {
#         'Authorization': 'Basic YOUR_BASE64_ENCODED_CREDENTIALS',  # Your base64 encoded API credentials if needed
#         'Ocp-Apim-Subscription-Key': MOMO_API_SECRET,  # Your Primary or Secondary key
#     }
    
#     response = requests.post(url, headers=headers)
    
#     if response.status_code == 200:
#         return response.json().get('access_token')
#     else:
#         raise Exception(f"Failed to obtain MoMo token: {response.status_code}, {response.text}")

#     # Example usage:
#     try:
#         access_token = get_momo_access_token()
#         print(f"Access token: {access_token}")
#     except Exception as e:
#         print(str(e))
    

# def initiate_momo_payment(amount, phone_number, order_id):
#     """
#     Initiates a MoMo payment request.
#     """
#     # First, obtain the access token
#     access_token = get_momo_access_token()

#     # Define the payment initiation URL
#     url = f"{MOMO_API_URL}/collection/v1_0/requesttopay"
#     headers = {
#         'Authorization': f"Bearer {access_token}",
#         'Ocp-Apim-Subscription-Key': MOMO_API_SECRET,
#         'Content-Type': 'application/json',
#         'X-Reference-Id': order_id,  # Unique transaction ID
#         'X-Target-Environment': 'sandbox',  # Change to 'production' when live
#     }

#     # Define the payload
#     payload = {
#         'amount': str(float(amount)),  # Convert amount to string as per MoMo API requirements
#         'currency': 'XOF',  # Adjust according to your currency (e.g., 'USD', 'XOF')
#         'externalId': str(order_id),  # External transaction reference (e.g., order number)
#         'payer': {
#             'partyIdType': 'MSISDN',
#             'partyId': phone_number,  # Customer's phone number
#         },
#         'payerMessage': 'Payment for Order #{}'.format(order_id),
#         'payeeNote': 'Payment for Order #{}'.format(order_id),
#     }

#     # Send the POST request to initiate payment
#     response = requests.post(url, headers=headers, json=payload)

#     if response.status_code == 202:  # 202 indicates the request was accepted
#         return response.json()
#     else:
#         raise Exception(f"Payment initiation failed: {response.status_code}, {response.text}")

# # Example of usage
# def process_payment(amount, phone_number, order_id):
#     try:
#         payment_response = initiate_momo_payment(amount, phone_number, order_id)
#         # You can log or process payment_response as needed
#         print("Payment initiated successfully:", payment_response)
#     except Exception as e:
#         print("Error during payment initiation:", str(e))



def home(request):
    service = Service.objects.all()[:3]
    routes = Route.objects.all()
    post = Post.objects.filter(is_draft=False)[:3]
    ctx = {
    'service':service,
    'post': post,
	'routes':routes
	}
    return render(request, 'pages/home.html', ctx)

def services_single(request,slug):
    services = get_object_or_404(Service, slug=slug)
    return render(request, 'pages/services_single.html',{'services':services})

def services_list(request):
    service = Service.objects.all()
    return render(request, 'pages/services.html',{'service':service})


def post_list(request):
    post = Post.objects.filter(is_draft=False).all()
    category_list = Category.objects.all()
    context={
    'post':post,
    'category_list':category_list
    }
    return render(request, 'pages/blog.html', context)

def post_by_category(request, name):
    
    post_list = Post.objects.all()[:4]
    category_list = Category.objects.all()
    category = get_object_or_404(Category, name=name)
    post = Post.objects.filter(is_draft=False, category=category)
    
    context={
    'post':post,
    'category':category,
    'category_list':category_list,
    'post_list':post_list
    }
    return render(request, 'pages/post-list.html', context)

def post_by_tag(request, name):
    post_list = Post.objects.all()[:4]
    category_list = Category.objects.all()
    tags = get_object_or_404(Tag, name=name)
    post = Post.objects.filter(is_draft=False, tags=tags)
    
    context={
    'post':post,
    'tags':tags,
    'category_list':category_list,
    'post_list':post_list
    }
    return render(request, 'pages/post-by-tags.html', context)

def post_single(request,slug):
    post = get_object_or_404(Post, slug=slug)
    post_list = Post.objects.filter(is_draft=False).all()
    category_list = Category.objects.all()
    tags = Tag.objects.all()
    context={
    'post':post,
    'category_list':category_list,
    'tags':tags,
    'post_list':post_list
    }
    return render(request, 'pages/post_single.html', context)



def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact form successfully sent. We will get back to you shortly.')
            form = ContactForm()  # Reset the form to empty fields after successful submission
    else:
        form = ContactForm()

    return render(request, 'pages/contact-us.html', {'form': form})


def bus_list(request, id):
    route = get_object_or_404(Route, id=id)
    buses = route.buses.all()
    
    # Prepare the context
    ctx = {
        'buses': buses,
        'route': route
    }
    
    return render(request, 'pages/bus.html', ctx)


def bus_single(request, slug):
    bus = get_object_or_404(Bus, slug=slug)

    ctx = {
        'bus': bus
    }
    
    return render(request, 'pages/bus-single.html', ctx)


@login_required
def book_seat(request, bus_id, route_id):
    # Get the bus and route objects or return a 404 error if not found
    bus = get_object_or_404(Bus, id=bus_id)
    route = get_object_or_404(Route, id=route_id)

    # Get available seats for this bus
    available_seats = Seat.objects.filter(bus=bus, is_booked=False)

    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')

        # Use a transaction to ensure atomicity
        try:
            with transaction.atomic():
                seat = Seat.objects.select_for_update().get(id=seat_id, bus=bus, is_booked=False)

                # Create a booking
                booking = Booking(
                    user=request.user,
                    route=route,
                    seat=seat
                )
                booking.save()

                # Mark the seat as booked
                seat.is_booked = False
                seat.save()

            # Redirect to payment view with booking details
            return redirect('payment_view', booking_id=booking.id)

        except Seat.DoesNotExist:
            messages.error(request, "The seat is no longer available. Please choose another seat.")
            return redirect('book_seat', bus_id=bus.id, route_id=route.id)

    # Prepare context for rendering the page
    ctx = {
        'bus': bus,
        'route': route,
        'available_seats': available_seats,
    }

    # Render the template with the context
    return render(request, 'pages/book_seat.html', ctx)


def payment_view(request, booking_id):
    # Retrieve the booking object or show 404 if not found
    booking = get_object_or_404(Booking, id=booking_id)
    amount = float(booking.route.price)  # Ensure amount is a float

    if request.method == 'POST':
        # Get the email from the form POST data
        email = request.POST.get('email')

        # Generate a unique order ID using the booking ID
        order_id = f"booking-{booking.id}"

        # Construct the Paymentwall widget directly with API keys
        widget = paymentwall.Widget(
            uid=email,  # The user's unique ID (email in this case)
            widget_code='p1',  # Example widget code, change as needed
            goods=[
                paymentwall.Product(
                    id=order_id,
                    amount=amount,
                    currency='USD',  # Adjust currency as needed
                    name=f"Payment for booking {booking.id}"
                )
            ],
            extra_params={
                'email': email,  # Pass the user's email
                'order_id': order_id,  # Attach the unique order ID
            },
            public_key=settings.PAYMENTWALL_PUBLIC_KEY,  # Add your Paymentwall public key
            private_key=settings.PAYMENTWALL_PRIVATE_KEY  # Add your Paymentwall private key
        )

        # Get the widget HTML code
        widget_html = widget.get_html_code()

        # Render the widget for the user to complete the payment
        return render(request, 'pages/payment_widget.html', {'widget_html': widget_html})

    # If GET request, render the payment form
    return render(request, 'pages/check_form.html', {'amount': amount, 'booking': booking})

# @login_required
# def booking_confirmation(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)
    
#     return render(request, 'pages/booking_confirmation.html', {'booking': booking})

@login_required
def profile_settings(request):
    user = request.user

    if request.method == 'POST':
        form = CustomSignupUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Settings Successfully Updated')
            return redirect('dashboard')
    else:
        form = CustomSignupUpdateForm(instance=user)

    context = {
        'form': form
    }
    return render(request, 'panel/settings.html', context)

@login_required
def dashboard(request):
    return render(request, 'panel/dashboard.html', {})

@login_required
def my_booking(request):
    user = request.user
    my_booking = Booking.objects.filter( user=user).all()

    context = {'my_booking':my_booking}
    
    return render(request, 'panel/my-bookings.html', context)


@login_required
def user_ratings(request):
    user = request.user
    my_reveiw = Review.objects.filter( user=user).all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)  # Save the form without committing to the database
            review.user = user        # Assign the current user to the review
            review.save()                     # Save the review to the database
            messages.success(request, 'Rating added successfully')
            return redirect('user_ratings')  # Return the redirect to the same view
    
    form = ReviewForm()  # Instantiate a new form for GET requests
    context = {
    'form': form,
    'my_reveiw':my_reveiw

    }
    return render(request, 'panel/ratings.html', context)

def suggestions(request):
    if request.method == 'POST':
        form = SuggestionBoxForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Suggestions added successfully we will check your suggestions')
            return redirect('home')

    else:
        form = SuggestionBoxForm()


    return render(request, 'pages/suggestions.html', {'form': form})





def faqs(request):
    faqs = FAQs.objects.all()
    return render(request, 'pages/faqs.html', {'faqs':faqs})