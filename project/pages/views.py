from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import View
import datetime

from .models import RoomDetails, MyBooking, Contact, Gallery


# Create your views here.

class HomePage(View):
    def get(self, request):
        rooms = RoomDetails.objects.all().filter(room_status='Available')

        context = {'rooms': rooms}
        return render(request, 'index.html', context=context)


class AboutPage(View):
    def get(self, request):
        return render(request, 'about.html')


class Roomdetails(View):
    def get(self, request, id):
        rooms = get_object_or_404(RoomDetails, pk=id)
        context = {'room': rooms}
        return render(request, 'roomDetails.html', context=context)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class BookingView(View):
    def get(self, request):
        return render(request, 'bookings.html')


class ContactView(View):

    def get(self, request):
        return render(request, 'contact.html')

    def post(self, request):
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            contact = Contact(name=name, email=email, message=message, subject=subject)
            contact.save()
            messages.success(request, 'Your Inquiry has been submitted. Thank you!')
            return redirect("contact")
        messages.error(request, 'There is problem with submission. Please Try Again')
        return redirect("contact")


class RegisterView(View):
    def get(self, request):
        return render(request, 'create.html')

    def post(self, request):
        if request.method == "POST":
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            password_cf = request.POST.get('confirm_pw')

            if password == password_cf:
                if User.objects.filter(email=email).exists():
                    message = "User already exists."
                    print(message)
                else:
                    user = User.objects.create_user(email=email,
                                                    username=email,
                                                    first_name=first_name,
                                                    last_name=last_name,
                                                    password=password)
                    user.save()
                    messages.success(request, 'Your Account has been created')
                    return redirect("login")
            else:
                message = "Passwords do not match"
                print(message)
            context = {
                'error_msg': message
            }
            return render(request, 'create.html', context=context)
        else:
            return render(request, 'create.html')


class ForgetPasswordView(View):
    def get(self, request):
        return render(request, 'forgetPassword.html')


class GalleryView(View):
    def get(self, request):
        images = Gallery.objects.all()
        context = {'images': images}
        return render(request, 'Gallery.html', context=context)


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = auth.authenticate(username=email, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Account has been Created")
                return redirect("home")
            else:
                message = "Invalid login details."
                print(message)
                return redirect("login")
        else:
            return render(request, 'login.html')


@method_decorator(login_required(login_url='/login'), name='dispatch')
class CancelBookingsView(View):
    def get(self, request):
        cancel_bookings = MyBooking.objects.get(name=request.user)
        if cancel_bookings:
            if cancel_bookings.name == request.user:
                cancel_bookings.delete()
                messages.success(request, "Bookings Cancelled")
                return redirect("my_bookings")
        return redirect('home')


@method_decorator(login_required(login_url='/login'), name='dispatch')
class MyBookingsView(View):
    def get(self, request):
        try:
            my_bookings = MyBooking.objects.get(name=request.user)
        except:
            my_bookings = ""
        context = {'my_booking': my_bookings}
        return render(request, 'myBookings.html', context=context)

    def post(self, request):
        if request.method == 'POST':
            arrival_date = request.POST.get('arrival_date')
            departure_date = request.POST.get('departure_date')
            room = request.POST.get('room')
            nights = request.POST.get('nights')
            adults = request.POST.get('adults')
            children = request.POST.get('children')
            number = request.POST.get('number')
            address = request.POST.get('address')
            message = request.POST.get('message')
            print(datetime.date.today())
            print(arrival_date)
            print(departure_date)
            print(nights)

            give = str(arrival_date)
            give_time = give.split("-")
            
            give1 = str(departure_date)
            give_time1 = give.split("-")
            print(int(give_time[0]))
            print(int(give_time[1]))
            print(int(give_time[2]))

            times1 = datetime.date.today()
            timess = datetime.date(int(give_time[0]),int(give_time[1]),int(give_time[2]))
            timess1 = datetime.date(int(give_time1[0]),int(give_time1[1]),int(give_time1[2]))
            if (timess>=times1 and timess1>=times1):
                has_made_booking = MyBooking.objects.all().filter(name=request.user)

                if has_made_booking:
                    messages.error(request, 'Your have already made booking.')
                    return redirect('booking')
                book = MyBooking(name=request.user, arrival_date=arrival_date, departure_date=departure_date,
                                room_select=room,
                                num_nights=nights, num_person=adults, num_children=children, phone_num=number,
                                address=address, des=message,)
                book.save()
                return redirect('my_bookings')
            else:
                messages.info(request,"Date is not correct. Please change the date")
                print("go back home")     
            # has_made_booking = MyBooking.objects.all().filter(name=request.user)

            # if has_made_booking:
            #     messages.error(request, 'Your have already made booking.')
            #     return redirect('booking')
            # book = MyBooking(name=request.user, arrival_date=arrival_date, departure_date=departure_date,
            #                  room_select=room,
            #                  num_nights=nights, num_person=adults, num_children=children, phone_num=number,
            #                  address=address, des=message,)
            # book.save()
            return redirect('booking')
        return redirect('booking')


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect("login")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            print(data)
            associated_users = User.objects.filter(Q(email=data))
            print(associated_users)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="forgetPassword.html",
                  context={"password_reset_form": password_reset_form})
