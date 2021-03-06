from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from models import Post, Vote
from forms import UserForm, PostForm, AnonPostForm, VoteForm
from django.template import RequestContext
from django.contrib import auth
from django.db.models import Count


def home(request):
    if not request.POST:
        posts = Post.objects.filter(quality=True)\
                .annotate(num_votes=Count('vote'))\
                .order_by('-num_votes')
        resp_dict = {'posts' : posts}
        if request.user.is_authenticated():
            pf = PostForm()
            resp_dict["post_form"] = pf
        return render_to_response('hello.html', resp_dict,
                context_instance=RequestContext(request))


def post_sub(request):
    if request.POST:
        pf = PostForm(request.POST)
        anonpf = AnonPostForm(request.POST)
        if pf.is_valid() and request.user.is_authenticated():
            post = Post(user=request.user, title=pf.cleaned_data["title"], body=pf.cleaned_data["body"],
                    markup=(not pf.cleaned_data["markup"]), quality=pf.cleaned_data["quality"])
            post.save()
            return HttpResponseRedirect("/")
        elif anonpf.is_valid():
            pf = anonpf
            anon = User.objects.get(username="anon")
            post = Post(user=anon, title=pf.cleaned_data["title"], body=pf.cleaned_data["body"],
                    markup=(not pf.cleaned_data["markup"]), quality=False)
            post.save()
            return HttpResponseRedirect("/freespeech")
    else:
        pf = PostForm()
    return render_to_response("sub_form.html", {
        'form' : pf,},
        context_instance=RequestContext(request))

def show_post(request, id_num):
    if request.method == "GET":
       post = get_object_or_404(Post, pk=id_num)
       author = False
       if request.user == post.user:
           author = True
       return render_to_response('single_post.html',
               {'post' : post, "edit": author},
                context_instance=RequestContext(request))
    else:
        return 1

def edit_post(request, id_num):
    if request.method == "POST":
        post = get_object_or_404(Post,pk=id_num)
        pf = PostForm(request.POST)
        if (pf.is_valid() and request.user.is_authenticated()
            and request.user == post.user):
            post.user = request.user
            post.title = pf.cleaned_data["title"]
            post.body = pf.cleaned_data["body"]
            post.markup = pf.cleaned_data["markup"]
            post.quality = pf.cleaned_data["quality"]
            post.save()
            return HttpResponseRedirect("/posts/" + str(id_num))
        return HttpResponse("You aren't allowed to do that guy")
    else:
        post = get_object_or_404(Post, pk=id_num)
        pf = PostForm(initial=
                {"title" : post.title,
                "body" : post.body},
                )
        return render_to_response("edit_post.html",
                {"post_form": pf},
                context_instance=RequestContext(request))

def create_user(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = User(username=username)
        user.set_password(password)
        user.save()
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        return HttpResponse("New user made with %s and %s params" % (username, password))
    else:
        uf = UserForm()


        return render_to_response("create.html", {"form" : uf},
                context_instance=RequestContext(request))

def delete_post(request, id_num):
    if request.method == "GET":
        post = get_object_or_404(Post, pk=id_num)
        if (request.user == post.user or request.user.username == "nick"):
            post.delete()
            return HttpResponse("Post Deleted")
        else:
            return HttpResponse("you cant delete that")

def login(request):
    if request.POST:
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect("/secret/home")
        else:
            return HttpResponse("bad creds, nice try kid")
    else:
        uf = UserForm()

        return render_to_response("login.html", {"form" : uf},
                context_instance=RequestContext(request))

def logged_in(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        return HttpResponse("not today you are not")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def user_page(request, name):
    if request.method == "GET":
        u = User.objects.get(username=name)
        posts = Post.objects.filter(user=u).order_by('date_last_edit')
        posts = posts[::-1]
        return render_to_response("user_page.html", {"the_user" : u,
                "posts" : posts},
                context_instance=RequestContext(request))
    else:
        return HttpResponse("wut")

def users(request):
    if request.method == "GET":
        users = User.objects.all()
        return render_to_response("users.html", {"users": users},
                context_instance=RequestContext(request))


def freedom(request):
    if request.method == "GET":
        pf = AnonPostForm()
        posts = Post.objects.filter(quality=False).order_by('date_last_edit')
        posts = posts[::-1]
        return render_to_response("freedom.html", {
            "posts" : posts, "form": pf},
                context_instance=RequestContext(request))
    else:
        return HttpResponse("wut")


def vote(request, id_num):
    vf = VoteForm(request.POST or None)
    post = get_object_or_404(Post, pk=id_num)
    if request.method == "POST" and vf.is_valid():
        if request.user.is_authenticated():
            user = request.user
        else:
            user = User.objects.get(username="anon")
        vote = Vote(post=post, user=user, ip=request.META["REMOTE_ADDR"])
        vote.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return render_to_response("vote.html",
            {"form": vf},
            context_instance=RequestContext(request))

def projects(request):
    posts = Post.objects.filter(user=User.objects.get(username="nskelsey")).order_by('date_post')
    posts = posts[::-1]
    return render_to_response("projects.html",
            {"posts" : posts},
            context_instance=RequestContext(request))



