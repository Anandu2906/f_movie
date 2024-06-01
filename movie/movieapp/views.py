from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.template import context
import mysql.connector
from .forms import Video_form, Review_Form
from .models import *
from django.contrib.auth import get_user
import logging


# Create your views here.
def home(request):
    return render(request, 'movieapp/index.html')


def index(request):
    return render(request, 'movieapp/index.html')


def user_signup(request):
    return render(request, 'movieapp/user_signup.html')


def uhome(request):
    fn = request.session['name']

    return render(request, 'movieapp/Userhome/index.html', {'name': fn})


def user_signupp(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST['email']
        passwd = request.POST['pass']
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="moviee")
        mycursor = mydb.cursor()
        q = "insert into movieapp_user( `fname`, `lname`, `email`, `password`) values('" + fname + "','" + lname + "','" + email + "','" + passwd + "')"
        mycursor.execute(q)
        mydb.commit()
        return render(request, 'movieapp/user_signup.html', {'msg': 'User Registered Successfully'})
    return render(request, 'movieapp/user_signup.html')


def user_login(request):
    return render(request, 'movieapp/user_login.html')


def ulogout(request):
    return render(request, 'movieapp/user_login.html')


def add_video(request):
    fn = request.session['name']
    if 'name' in request.session:
        if request.method == "POST":
            form = Video_form(data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                form = Video_form()
                return render(request, 'movieapp/Userhome/useradd_video.html',
                              {'msg': 'Details Uploaded', "form": form, 'name': fn})
            else:
                form = Video_form()
                return render(request, 'movieapp/Userhome/useradd_video.html',
                              {'msg': 'Error occured, Try another File', "form": form, 'name': fn})
        else:
            form = Video_form()
            return render(request, 'movieapp/Userhome/useradd_video.html', {"form": form, 'name': fn})
    else:
        return render(request, 'movieapp/user_login.html')


def udel_video(request):
    # all_video = Video.objects.filter()
    # "all": all_video
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='moviee')
    mycursor = conn.cursor()
    if 'name' in request.session:
        fn = request.session['name']
        if request.POST.get('delete'):
            id = request.POST["t_id"]
            print(id)
            query = "delete from movieapp_movie_details where id =" + id + " "
            mycursor.execute(query)
            conn.commit()

            em = request.session['email']
            id = request.session['id']
            print("hello")
            all_video = movie_details.objects.filter(user_id=id)
            print("hello")
            return render(request, 'movieapp/Userhome/userview_video.html',
                          {"all": all_video, 'name': fn, 'msg': "Video Deleted"})
        # return render(request, 'DEMOAPP/tview_video.html', {"all": all_video, 'name': fn,'msg':"Video Deleted"})
    else:
        return render(request, 'movieapp/user_login.html', {'msg': 'Login to Enter'})


def view_video(request):
    if 'name' in request.session:
        fn = request.session['name']
        em = request.session['email']
        id = request.session['id']
        print("hello")
        all_video = movie_details.objects.filter(user_id=id)
        print("hello")

        return render(request, 'movieapp/Userhome/userview_video.html', {"all": all_video, 'name': fn})

    else:
        return render(request, 'movieapp/user_login.html')

def showmovies(request):
    all_video = movie_details.objects.all()
    return render(request, 'movieapp/movies.html', {"all": all_video})
    
def movies(request):
    all_video = movie_details.objects.all()
    return render(request, 'movieapp/movies.html', {"all": all_video})

def search_movies(request):
    all_video = movie_details.objects.all()
    if request.method == 'GET':
        mo = request.GET.get('searchmovies')
        print(mo)
        if mo!=None:
            all_video = movie_details.objects.filter(title=mo)
    return render(request, 'movieapp/movies.html', {"all": all_video})

def post_review(request):
    if request.method == 'POST':
        id = request.POST["t_id"]
        all_video = movie_details.objects.filter(id=id)
        return render(request, 'movieapp/post_review.html', {"all": all_video})

logger = logging.getLogger(__name__)
def submit_review(request):
    if request.method == 'POST':
        mid = request.POST.get("m_id")
        form = None

        try:
            reviews = Review.objects.get(movie_details_id=mid)
            form = Review_Form(request.POST, instance=reviews)
            logger.info("Review found for movie ID %s", mid)
        except Review.DoesNotExist:
            form = Review_Form(request.POST)
            logger.info("No review found for movie ID %s, creating a new one", mid)
        except Exception as e:
            logger.error("Error retrieving review for movie ID %s: %s", mid, str(e))
            messages.error(request, 'There was an error retrieving the review.')
            all_video = movie_details.objects.filter(id=mid)
            return render(request, 'movieapp/post_review.html', {"all": all_video, "form": form,"msg":"Error retrieving review for movie"})

        if form.is_valid():
            review = form.save(commit=False)
            review.movie_details_id = mid  # Assuming you have a movie_details foreign key in the Review model
            review.save()
            messages.success(request,
                             'Thank you! Your review has been submitted.' if 'instance' not in form.initial else 'Thank you! Your review has been updated.')
        else:
            logger.error("Form is not valid: %s", form.errors)
            messages.error(request, 'There was an error submitting your review.')

        all_video = movie_details.objects.filter(id=mid)
        return render(request, 'movieapp/post_review.html', {"all": all_video, "form": form,"msg":"Thank you! Your review has been submitted"})
    else:
        return render(request, 'movieapp/movies.html',{"msg":"Thank you! Your review has been submitted"})
    

"""def submit_review(request):
    if request.method == 'POST':
        mid = request.POST["m_id"]
        print(mid)
        try:
            print("try")
            reviews = Review.objects.get(movie_details_id=mid)
            form = Review_Form(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you ! Your review has been updated')
            all_video = movie_details.objects.filter(id=mid)
            return render(request, 'movieapp/post_review.html', {"all": all_video})
        except Review.DoesNotExist:
            print("catch")
            form = Review_Form(request.POST)
            if form.is_valid():
                data = Review()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.comment = form.cleaned_data['comment']
                data.save()
                ms = ""
                messages.success(request, 'Thank you ! Your review has been updated')
                all_video = movie_details.objects.filter(id=mid)
                return render(request, 'movieapp/post_review.html', {"all": all_video})
    else:

        return render(request, 'movieapp/movies.html')"""



def update_video(request):
    vid = request.POST["t_id"]
    fn = request.session['name']
    post = get_object_or_404(movie_details, id=vid)
    if 'name' in request.session:
        if request.method == 'POST':
            form = Video_form(request.POST, instance=post)
            print("inside")
            if form.is_valid():
                form.save()
                messages.success(request, 'The post has been updated successfully.')
                form = Video_form(instance=post)
                return render(request, 'movieapp/Userhome/useredit_video.html', {'name': fn, 'form': form})
    else:
        return render(request, 'movieapp/user_login.html')


def uprofile(request):
    if 'name' in request.session:
        fn = request.session['name']
        ln = request.session['lname']
        em = request.session['email']
        return render(request, 'movieapp/Userhome/uprofile.html', {'fname': fn, 'lname': ln, 'email': em})
    else:
        return render(request, 'movieapp/user_login.html')


def uedit_profile(request):
    if 'name' in request.session:
        if request.method == "POST":
            fn = request.POST['fname']
            ln = request.POST['lname']
            em = request.POST['email']
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='moviee')
            mycursor = conn.cursor()
            q = "update movieapp_user set fname='" + fn + "',lname = '" + ln + "',email = '" + em + "' "
            mycursor.execute(q)
            conn.commit()
            return render(request, 'movieapp/Userhome/uprofile.html',
                          {'name': fn, 'fname': fn, 'lname': ln, 'email': em})
        else:
            return render(request, 'movieapp/user_login.html')
    else:
        return render(request, 'movieapp/user_login.html')


def uedit_video(request):
    fn = request.session['name']

    if request.method == 'GET':
        vidd = request.GET["t_id"]
        post = get_object_or_404(movie_details, id=vidd)
        form = Video_form(instance=post)
        return render(request, 'movieapp/Userhome/useredit_video.html', {'name': fn, 'form': form, 'id': vidd})
    elif request.method == 'POST':
        vid = request.POST["tt_id"]
        post = get_object_or_404(movie_details, id=vid)
        form = Video_form(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            form = Video_form(instance=post)
            return render(request, 'movieapp/Userhome/useredit_video.html', {'name': fn, 'form': form})
    else:
        return render(request, 'movieapp/user_login.html')


def user_loginn(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["pass"]
        # print(email + password)
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='moviee')
        mycursor = conn.cursor()
        mycursor1 = conn.cursor()
        mycursor2 = conn.cursor()
        mycursor3 = conn.cursor()
        query = "select * from movieapp_user where email ='" + email + "' and password='" + password + "' "
        mycursor.execute(query)
        mycursor.fetchall()
        query1 = "select fname from movieapp_user where email ='" + email + "' and password='" + password + "' "
        mycursor1.execute(query1)
        fname = mycursor1.fetchone()[0]
        query3 = "select lname from movieapp_user where email ='" + email + "' and password='" + password + "' "
        mycursor3.execute(query3)
        lname = mycursor3.fetchone()[0]
        query2 = "select id from movieapp_user where email ='" + email + "' and password='" + password + "' "
        mycursor2.execute(query2)
        id = mycursor2.fetchone()[0]
        print(id)

        request.session['name'] = fname
        request.session['lname'] = lname
        request.session['email'] = email
        request.session['id'] = id
        # print (fname)
        # print(mycursor.rowcount)
        if mycursor.rowcount != 0:
            # name = request.session['tchrn']
            # messages.error(request, "invalid username and password.")
            return render(request, 'movieapp/Userhome/index.html', {'name': fname})
        else:
            return render(request, 'movieapp/user_login.html')
    return render(request, 'movieapp/user_login.html')
