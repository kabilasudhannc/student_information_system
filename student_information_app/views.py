# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from student_information_app.EmailBackEnd import EmailBackEnd
from student_information_app.models import CustomUser, Courses, SessionYearModel


def home(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'),
                                         password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            # return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_home')

            elif user_type == '2':
                # return HttpResponse("Staff Login")
                return redirect('staff_home')

            elif user_type == '3':
                # return HttpResponse("Student Login")
                return redirect('student_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            # return HttpResponseRedirect("/")
            return redirect('login')


def get_user_details(request):
    if request.user is not None:
        return HttpResponse("User: " + request.user.email + " User Type: " + request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login')


def signup_admin(request):
    return render(request, 'signup_admin_page.html')


def signup_student(request):
    courses = Courses.objects.all()
    session_years = SessionYearModel.objects.all()
    return render(request, 'signup_student_page.html', {'courses': courses, 'session_years': session_years})


def signup_staff(request):
    return render(request, 'signup_staff_page.html')


def do_admin_signup(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email, user_type=1)
        user.save()
        messages.success(request, "Successfully Created Admin")
        return HttpResponseRedirect(reverse('login'))

    except:
        messages.error(request, "Failed to create Admin")
        return HttpResponseRedirect(reverse('login'))


def do_staff_signup(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    address = request.POST.get('address')

    try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                              first_name=first_name, last_name=last_name, user_type=2)
        user.staffs.address = address
        user.save()
        messages.success(request, "Staff Added Successfully!")
        return redirect('login')

    except:
        messages.error(request, "Failed to Add Staff!")
        return redirect('login')


def do_student_signup(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    address = request.POST.get('address')
    session_year_id = request.POST.get('session_year')
    course_id = request.POST.get('course_id')
    gender = request.POST.get('gender')

    # Getting Profile Pic first
    # First Check whether the file is selected or not
    # Upload only if file is selected
    if len(request.FILES) != 0:
        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)
    else:
        profile_pic_url = None

    try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                                  last_name=last_name, user_type=3)
        user.students.address = address

        course_obj = Courses.objects.get(id=course_id)
        user.students.course_id = course_obj

        session_year_obj = SessionYearModel.objects.get(id=session_year_id)
        user.students.session_year_id = session_year_obj

        user.students.gender = gender
        user.students.profile_pic = profile_pic_url
        user.save()
        messages.success(request, "Student Added Successfully!")
        return redirect('login')

    except:
        messages.error(request, "Failed to Add Student!")
        return redirect('login')
