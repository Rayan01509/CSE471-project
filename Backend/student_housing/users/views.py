from django.shortcuts import render, redirect
from users.models import Register
from .models import Register, Comment
# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
from users.models import DormRoom
from django.shortcuts import get_object_or_404
from .forms import CommentForm



def users_intro(request):
    return HttpResponse("Welcome")

def users_login(request):
    if(request.method == "POST"):
        username = request.POST['username']   
        password = request.POST['password']

        try:
            user_check = Register.objects.get(username=username, password=password)
            request.session['username'] = username
            a = request.session.get('username')
            print(a)
            return redirect('users_profile', username = a)

        except:
            messages.warning(request, 'Invalid username or password. Please Try again')


    return render(request, 'login.html') 

def users_register(request):
    if request.method=="POST":
        username= request.POST['username']
        email= request.POST['email']
        password= request.POST['password']
        nid= request.POST['nid']
        # Location= request.POST['Location']
        #print(username, email, password, nid)
        ins= Register(username=username, email=email, password=password, nid=nid)
        ins.save()
        # print("Those data are already saved in db")
        # return render(request, 'login.html')
        return redirect('users_login')
    return render(request, 'register.html')

def users_profile(request, username):
    session_data = request.session.get('username')
    if(session_data is not None):
        session_data_db = Register.objects.get(username=session_data)

    else:
        messages.warning(request, 'Please log in again to continue')
    
    return render(request, 'profile.html', {'username' : username, 'database_output' : session_data_db})

def create_post(request,username):
    created_by = request.session.get('username')
    if request.method=="POST":
        title=request.POST['title']
        content=request.POST['content']
        type= request.POST['type']
        price=request.POST['price']
        register_instance = get_object_or_404(Register, username=created_by)
       
        ins= DormRoom(title=title,content=content, type=type,  price=price, link='', posted_by = register_instance)
        ins.save()

        ins.link = f'http://127.0.0.1:8000/users/{created_by}/posts/learn_more/{ins.id}'
        ins.save()

        
    return render(request, 'create_post.html', {'username' : created_by})

def users_logout(request):
    request.session.clear()
    return redirect('users_login')

def show_posts(request, username):
    username = request.session.get('username')
    posts = DormRoom.objects.all()
    
    print(posts)

    return render(request, 'dorm_room_details.html', {'dorm_rooms' : posts, 'username' : username})

def learn_more(request, pk, username):
    username = request.session.get('username')
    post = DormRoom.objects.get(id = pk)
    show_del = False
    post_username = post.posted_by.username

    if(post_username == username):
        show_del = True

    return render(request, 'dorm_room_post_detail.html', {'details' : post, 'username' : username, 'delButton' : show_del})


def own_posts(request, username):
    username = request.session.get('username')
    user = get_object_or_404(Register, username=username)
    posts = DormRoom.objects.filter(posted_by = user)

    return render(request, 'own_posts.html', {'details' : posts, 'username' : username})

def delete_post(request, pk, username):
    username = request.session.get('username')
    post = DormRoom.objects.get(id = pk)
    post.delete()
    return render(request, 'delete_post.html', {'details' : post, 'username' : username})

def comment_dorm_room(request, username, pk):
    username = request.session.get('username')
    dorm_room = get_object_or_404(DormRoom, id=pk)
    commentor = get_object_or_404(Register, username= username)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment']
            
            # Create a new Comment instance
            new_comment = Comment(comment=comment_text, commented_by=commentor)
            new_comment.save()
            
            # Append the new comment to the DormRoom instance
            dorm_room.comments.add(new_comment)

    return redirect('learn_more', pk=pk, username=username)


