from django.shortcuts import render, redirect
from .models import User, DailyActivity
from django.contrib import messages
from .forms import DailyActivityForm



# Create your views here.
def index(request):
    return render(request, "myapp/index.html", {})


def menu(request):
    return render(request, "myapp/menu.html", {})


def signup(request):
    return render(request, "myapp/signup.html", {})


def insertuser(request):
    text_uname = request.POST['tuname']
    text_email = request.POST['tuemail']
    text_password = request.POST['tupassword']
    text_password2 = request.POST['tupassword2']

    if text_password != text_password2:
        messages.error(request, "Passwords do not match.")
        return redirect("/signup")

    if User.objects.filter(username=text_uname).exists():
        messages.error(request, "Username is already taken. Try another one.")
        return redirect("/signup")

    if User.objects.filter(email=text_email).exists():
        messages.error(request, "Email is already in use. Try logging in or use another email.")
        return redirect("/signup")

    ob = User(username=text_uname, email=text_email, password=text_password)
    ob.save()

    return redirect("/menu")


def login(request):
     return render(request, "myapp/login.html", {})

def loginuser(request):
    if request.method == "POST":
        text_uname = request.POST.get("tuname")
        text_password = request.POST.get("tupassword")

        try:
            user = User.objects.get(username=text_uname)  # Look up user by username
            if text_password == user.password:  # Compare passwords directly (⚠)
                request.session["user_id"] = user.id
                print(user.id)         # Manually set session
                messages.success(request, "Login successful!")
                return redirect("menu")
            else:
                messages.error(request, "Invalid username or password.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")

    return render(request, "myapp/login.html")


def logout(request):
    return render(request, "myapp/logout.html", {})


def logoutuser(request):
    if "user_id" in request.session:  # Check if the user is logged in
        del request.session["user_id"]  # Remove user from session
    messages.success(request, "You have been logged out.")
    return redirect("index")  # Redirect to login page after logout


def daily_activity_create(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect("login")  # Redirect to login if not logged in

    # Fetch the logged-in user
    user_id = request.session["user_id"]
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = DailyActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = user  # Link to the logged-in user manually
            activity.save()
            messages.success(request, "Daily activity recorded successfully!")
            return redirect("display_activity")  # Redirect to the menu page
    else:
        form = DailyActivityForm()
    return render(request, 'myapp/daily_activity.html', {'form': form})


def daily_activity_list_view(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect("login")  # Redirect to login page

    # Fetch the logged-in user
    user_id = request.session["user_id"]
    user = User.objects.get(id=user_id)

    # Retrieve all daily activities for this user
    activities = DailyActivity.objects.filter(user=user).order_by('-date')  # Show newest first

    return render(request, 'myapp/display_daily_activity.html', {'activity_list': activities})

def daily_activity_delete(request,id):

    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect("login")  # Redirect to login page

    activity = DailyActivity.objects.get(id=id)
    activity.delete()
    messages.success(request, "Activity was deleted successfully!")
    return redirect('display_activity')


#Update View
def daily_activity_update(request, id):

    if "user_id" not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect("login")  # Redirect to login page


    activity = DailyActivity.objects.get(id=id)
    form = DailyActivityForm(instance=activity)
    if request.method == "POST":
        form = DailyActivityForm(request.POST,instance=activity)
        if form.is_valid():
            form.save()
            return redirect('display_activity')
    return render(request, 'myapp/daily_activity.html', {'form':form})

