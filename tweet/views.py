from django.shortcuts import render
from .models import Tweet
from .forms import TwitForm,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# Create your views here.

def index(request):
    return render(request,'index.html')

#listing tweets
def tweet_list(request):
   tweets= Tweet.objects.all().order_by('-created_at')
   return render(request,'tweet_list.html',{'tweets':tweets})

#creating tweet
@login_required
def create_tweet(request):
    if request.method=='POST':
        form=TwitForm(request.POST,request.FILES)
        if form.is_valid:
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form=TwitForm()
    
    return render(request,'tweet_form.html', {'form':form})    

#editing tweet
@login_required
def edit_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        form = TwitForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TwitForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})  
    

#delete tweet
@login_required
def delete_tweet(request,tweet_id):
        tweet= get_object_or_404(Tweet,pk=tweet_id,user=request.user)
        if request.method=='POST':
            tweet.delete()
            return redirect('tweet_list')
        
        return render(request,'tweet_delete.html',{'tweet':tweet})
    
#user registration
def register(request):
    if request.method=='POST':
        form= UserRegistrationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form= UserRegistrationForm
    
    
    
    return render(request,'registration/register.html',{'form':form})
        