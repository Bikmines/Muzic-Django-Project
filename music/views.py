from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views import generic
from .forms import userform
from django.views.generic import View
from .models import Album, song, FriendRequest
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


class Indexview(ListView):
    template_name = 'music/index.html'
    context_object_name = "album_list"
    paginate_by = 9

    def get_queryset(self):
        queryset = Album.objects.all()

        query = self.request.GET.get("q")

        user = self.request.user

        if user is not None and user.is_active:
            if user.is_superuser is False:
                queryset = queryset.filter(created_by=user)

        if query:
            queryset = queryset.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query) |
                Q(genre__icontains=query)
            ).distinct()

        return queryset


class Detailview(DetailView):
    model = Album
    paginate_by = 5
    template_name = 'music/details.html'

class songs(ListView):
    template_name = 'music/songs.html'
    paginate_by = 10


    def get_queryset(self):
        # get all albums that was created by currently logged in user
        albums = Album.objects.all().filter(created_by=self.request.user)
        # get all songs that belongs to above albums
        queryset = song.objects.all().filter(album__in=albums)
        query = self.request.GET.get("q")
        user = self.request.user

        if user is not None and user.is_active:
            if user.is_superuser:
                queryset = song.objects.all()


        if query:
            queryset = queryset.filter(Q(title_name__icontains=query)).distinct()

        return queryset


class Albumcreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'album_logo', 'genre']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(Albumcreate, self).form_valid(form)


class addsong(CreateView):
    model = song
    fields = ['title_name', 'title']


    def form_valid(self, form):
        form.instance.album = Album.objects.get(id=self.kwargs['album'])
        return super(addsong, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(addsong, self).get_context_data(**kwargs)

        if 'album' in self.kwargs:
            context['album'] = get_object_or_404(Album, id=self.kwargs['album'])

        return context

class Albumupdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'album_logo', 'genre']

class Albumdelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')

class songdelete(DeleteView):
    model = song

    def get_success_url(self):
        return reverse('music:detail', kwargs={"pk": self.object.album_id})





class userformview(View):
    form_class = userform
    template_name = 'music/registration-form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

                return render(request, self.template_name, {'form': form})


def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return redirect('music:index')
    elif request.user.is_authenticated():
        return redirect('music:index')
    else:
        return render(request, 'music/login.html')


def logout_view(request):
    logout(request)
    return redirect('music:index')

class ProfileView(DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'music/profile.html'

class FriendRequestView(CreateView):
    model = FriendRequest
    fields = ['from_user_id', 'to_user_id']

    def form_valid(self, form):
        form.instance.from_user_id = self.request.user
        form.instance.to_user_id = get_object_or_404(User, id=self.kwargs['pk'])

        return super(FriendRequestView, self).form_valid(form)
