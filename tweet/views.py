from django.shortcuts import render
from .models import Tweet
from .forms import TwitForm
from django.shortcuts import get_object_or_404,redirect
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,'index.html')

#listing tweets
def tweet_list(request):
   tweets= Tweet.objects.all().order_by('-created_at')
   return render(request,'tweet_list.html',{'tweets':tweets})

#creating tweet
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
def delete_tweet(request,tweet_id):
        tweet= get_object_or_404(Tweet,pk=tweet_id,user=request.user)
        if request.method=='POST':
            tweet.delete()
            return redirect('tweet_list')
        
        return render(request,'tweet_delete.html',{'tweet':tweet})