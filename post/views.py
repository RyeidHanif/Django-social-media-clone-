from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import AddPostForm , ModifyPostForm, CommentForm
from .models import Post , comment
from django.contrib.auth.models import User
# Create your views here.


def home(request):
    return render(request , 'post/home.html')



def dashboard(request):
    if request.method =="POST":
        if request.POST.get("addbutton"):
            return redirect("addpost")
        elif request.POST.get("showmyposts"):
            return redirect("showmyposts")
        elif request.POST.get("showmyfeed"):
            return redirect("showmyfeed")
        elif request.POST.get("settings"):
            return redirect("mysettings")
        
        elif request.POST.get("messages"):
            return redirect("viewcontacts")
    return render(request , "post/dashboard.html", {"user" : request.user.username})
            

def addpost(request):
    if request.method == "POST":
        Addform= AddPostForm(request.POST, request.FILES)
        if Addform.is_valid():
            post = Addform.save(commit=False)
            post.owner = request.user
            post.save()
            messages.success(request ,"Post saved successfully ")
            return redirect("dashboard")
        else :
            messages.warning(request, "form is invalid , please refill")
            return render(request , "post/addpost.html", {"form" : Addform})
    else :
        Addform = AddPostForm()
    return render(request , "post/addpost.html", {"form" : Addform})
            
    
   


def showmyposts(request):
    current_user = request.user
    posts = current_user.posts_set.all().order_by('-date_posted')
    if request.method == "POST":
        if request.POST.get("delete"):
            post_id = request.POST.get("delete")
            delete_to = Post.objects.get(id=post_id)
            delete_to.delete()
            messages.success(request , "Post successfully deleted")
            return render(request , "post/showmyposts.html" , {"posts":posts})
        
        elif request.POST.get("modify"):
            post_id = request.POST.get("modify")
            return redirect("modifypost",postID=post_id)
    return render(request, "post/showmyposts.html", {"posts":posts})



def  showmyfeed(request):
    all_posts = Post.objects.all().order_by('-date_posted')
    if request.method == "POST":
        if request.POST.get("comment"):
            return redirect("showcomments")
        elif request.POST.get("like"):
            post = Post.objects.get(id=request.POST.get("like"))
            post.likes +=1
            post.save()

    return render(request, "post/showmyfeed.html", {"posts": all_posts})



def mysettings(request):
    return HttpResponse("here are all your settings ")

def modifypost(request, postID):
    post = Post.objects.get(id = postID)
    if request.method == "POST":
        modifyform = ModifyPostForm(request.POST , request.FILES)
        if modifyform.is_valid():
            post_name = modifyform.cleaned_data["postname"]
            postcontent =modifyform.cleaned_data["content"]
            new_banner = modifyform.cleaned_data.get("banner") or post.banner
            post.postname = post_name
            post.content = postcontent
            post.banner = new_banner
            post.save()
            messages.success(request , "post modified  successfully")
            return redirect("dashboard")
    else : 
        modifyform = ModifyPostForm(initial={
            'postname': post.postname,
            'content': post.content,
        })
    return render(request , "post/modifypost.html", {"form": modifyform})




def showcomments(request, postID):
    post = Post.objects.get(id=postID)
    all_comments = post.comments_set()
    if request.method == "POST":
        comform = CommentForm(request.POST)
        if comform.is_valid():
            content = comform.cleaned_data['content']
            new_comment = comment(content, post)
            new_comment.save()
            messages.info(request, "Comment added")
            return redirect("showmyfeed")
    
    return render(request , "post/showmyfeed.html", {"comments" : all_comments})

        





