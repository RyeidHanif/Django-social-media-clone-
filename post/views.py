from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .forms import (
    AddPostForm,
    ModifyPostForm,
    CommentForm,
    ChangeProfilePhotoForm,
    CommentFormModel,
)
from .models import Post, Comment, ProfilePhoto, FriendRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from time import time

# Create your views here.


def home(request):
    return render(request, "post/home.html")


@login_required(login_url="/login/")
def dashboard(request):
    if request.method == "POST":
        if request.POST.get("addbutton"):
            return redirect("addpost")
        elif request.POST.get("showmyposts"):
            return redirect("showmyposts")
        elif request.POST.get("showmyfeed"):
            return redirect("showmyfeed")
        elif request.POST.get("settings"):
            return redirect("settings")

        elif request.POST.get("friends"):
            return redirect("friends")
        elif request.POST.get("viewrecom"):
            return redirect("viewrecom")
        elif request.POST.get("viewpending"):
            return redirect("viewpending")
    return render(request, "post/dashboard.html", {"user": request.user.username})


@login_required(login_url="/login/")
def addpost(request):
    if request.method == "POST":
        print(request.POST)
        Addform = AddPostForm(request.POST, request.FILES)
        if Addform.is_valid():
            post = Addform.save(commit=False)
            post.owner = request.user
            post.save()
            messages.success(request, "Post saved successfully ")
            return redirect("dashboard")
        else:
            messages.warning(request, "form is invalid , please refill")
            return render(request, "post/addpost.html", {"form": Addform})
    else:
        Addform = AddPostForm()
    return render(request, "post/addpost.html", {"form": Addform})


@login_required(login_url="/login/")
def showmyposts(request):
    current_user = request.user
    posts = current_user.posts_set.all().order_by("-date_posted")
    if request.method == "POST":
        if request.POST.get("delete"):
            post_id = request.POST.get("delete")
            delete_to = Post.objects.get(id=post_id)
            delete_to.delete()
            messages.success(request, "Post successfully deleted")
            return render(request, "post/showmyposts.html", {"posts": posts})

        elif request.POST.get("modify"):
            post_id = request.POST.get("modify")
            return redirect("modifypost", postID=post_id)
    return render(request, "post/showmyposts.html", {"posts": posts})


@login_required(login_url="/login/")
def showmyfeed(request):
    all_posts = Post.objects.all().order_by("-date_posted")
    if request.method == "POST":
        if request.POST.get("comment"):
            return redirect("showcomments", postID=request.POST.get("comment"))
        elif request.POST.get("like"):
            post = Post.objects.get(id=request.POST.get("like"))

            if request.user in post.likes.all():
                post.likes.remove(request.user)  # Unlike
            else:
                post.likes.add(request.user)

            post.save()

    return render(request, "post/showmyfeed.html", {"posts": all_posts})


@login_required(login_url="/login/")
def settings(request):
    profile = ProfilePhoto.objects.filter(user=request.user).first()
    if not profile:
        profile = ProfilePhoto(user=request.user)
        profile.save()
    if request.method == "POST":
        if request.POST.get("delete"):
            if profile and profile.photo:
                profile.photo.delete(save=False)  # deletes just the image file
                profile.delete()
                messages.success(request, "Profile photo deleted")
            else:
                messages.error(request, "No profile photo to delete")
            return redirect("settings")

        changepfp = ChangeProfilePhotoForm(request.POST, request.FILES)
        if changepfp.is_valid():
            profile.photo = changepfp.cleaned_data["new_photo"]
            profile.save()
            return redirect("settings")

    else:
        changepfp = ChangeProfilePhotoForm()
    return render(
        request,
        "post/settings.html",
        {
            "form": changepfp,
            "originalphoto": profile.photo.url if profile and profile.photo else None,
        },
    )


@login_required(redirect_field_name="login")
def modifypost(request, postID):
    post = Post.objects.get(id=postID)
    if request.method == "POST":
        modifyform = ModifyPostForm(request.POST, request.FILES)
        if modifyform.is_valid():
            post_name = modifyform.cleaned_data["postname"]
            postcontent = modifyform.cleaned_data["content"]
            new_banner = modifyform.cleaned_data.get("banner") or post.banner
            post.postname = post_name
            post.content = postcontent
            post.banner = new_banner
            post.save()
            messages.success(request, "post modified  successfully")
            return redirect("dashboard")
    else:
        modifyform = ModifyPostForm(
            initial={
                "postname": post.postname,
                "content": post.content,
            }
        )
    return render(request, "post/modifypost.html", {"form": modifyform})


@login_required(login_url="/login/")
def showcomments(request, postID):
    post = Post.objects.get(id=postID)
    all_comments = post.comments_set.all()  

    if request.method == "POST":
        print("request has been posted")
        form = CommentFormModel(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, "Comment added")
            return redirect("dashboard")
        else:
            e = form.errors
            print(f"Is not valid because {e}")

    else:
        form = CommentFormModel()

    return render(
        request,
        "post/showcomments.html",
        {
            "comments": all_comments,
            "form": form,
            "post": post,  
        },
    )


@login_required(login_url="/login/")
def aboutuser(request, user_id):
    other_user = User.objects.get(id=user_id)
    current_user_friends = request.user.friends.all()
    if other_user in current_user_friends:
        posts = other_user.posts_set.all()
        profilephoto = ProfilePhoto.objects.filter(user=other_user).first()

        return render(
            request,
            "post/aboutuser.html",
            {"target_user": other_user, "posts": posts, "profilephoto": profilephoto},
        )
    else:
        messages.warning(request, "This user is inaccessible . you are not friends")
        return redirect("showmyfeed")


@login_required(login_url="/login/")
def friends(request):
    user = request.user
    myfriends = user.friends.all()

    if request.method == "POST":
        if "message" in request.POST:
            friend_id = request.POST.get("message")
            return redirect("chat_with", reciever_id=friend_id)

        elif "remove" in request.POST:
            friend_id = request.POST.get("remove")
            friend = User.objects.get(id=friend_id)
            user.friends.remove(friend)
            messages.success(request, f"Removed {friend.username} from your friends")
            return redirect("friends")
    return render(request, "post/friends.html", {"myfriends": myfriends})


from django.db.models import Q


@login_required(login_url="/login/")
def viewrecom(request):
    user = request.user
    friends = user.friends.all()

    sent_pending = FriendRequest.objects.filter(
        from_user=user, status="pending"
    ).values_list("to_user", flat=True)
    received_pending = FriendRequest.objects.filter(
        to_user=user, status="pending"
    ).values_list("from_user", flat=True)

    display = User.objects.exclude(
        Q(id__in=friends)
        | Q(id=user.id)
        | Q(id__in=sent_pending)
        | Q(id__in=received_pending)
    )

    if request.method == "POST":
        if request.POST.get("sendfriendreq"):
            receiver_id = request.POST.get("sendfriendreq")
            receiver_user = User.objects.get(id=receiver_id)
            new_friend_req = FriendRequest(
                from_user=user, to_user=receiver_user, status="pending"
            )
            new_friend_req.save()
            messages.success(request, "Sent successfully")
            return redirect("viewrecom")

    return render(request, "post/myrecom.html", {"contacts": display})


@login_required(login_url="/login/")
def viewpending(request):
    iamsender = FriendRequest.objects.filter(from_user=request.user, status="pending")
    iamreciever = FriendRequest.objects.filter(to_user=request.user, status="pending")

    if request.method == "POST":
        me = request.user

        if request.POST.get("accept"):
            other_user = User.objects.get(id=request.POST.get("accept"))
            friendrequest = FriendRequest.objects.filter(
                from_user=other_user, to_user=me, status="pending"
            ).first()
            if friendrequest:
                me.friends.add(other_user)
                friendrequest.status = "accepted"
                friendrequest.save()
                messages.success(request, "Friend added successfully.")
            else:
                messages.error(request, "That request never existed.")
            return redirect("viewpending")

        elif request.POST.get("reject"):
            other_user = User.objects.get(id=request.POST.get("reject"))
            friendrequest = FriendRequest.objects.filter(
                from_user=other_user, to_user=me, status="pending"
            ).first()
            if friendrequest:
                friendrequest.status = "rejected"
                friendrequest.save()
                messages.success(request, "Rejected successfully.")
            else:
                messages.error(request, "There was no request to begin with.")
            return redirect("viewpending")

        elif request.POST.get("cancel"):
            other_user = User.objects.get(id=request.POST.get("cancel"))
            friendrequest = FriendRequest.objects.filter(
                from_user=me, to_user=other_user, status="pending"
            ).first()
            if friendrequest:
                friendrequest.delete()
                messages.success(request, "Successfully deleted.")
            else:
                messages.error(request, "Friend request never existed.")
            return redirect("viewpending")

    return render(
        request,
        "post/viewpending.html",
        {"iamsender": iamsender, "iamreciever": iamreciever},
    )


def whatsnew(request):
    return render( request ,"post/whatsnew.html")