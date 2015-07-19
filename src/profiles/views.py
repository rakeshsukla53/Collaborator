
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.forms.models import modelformset_factory

from questions.matching import points, match_percentage
from matches.models import Match, JobMatch
import urllib2
import json
from .models import Address, Job, UserPicture
from .forms import AddressForm, JobForm, UserPictureForm

def home(request):  #2 request here is HTTP request coming from the front end
    return render_to_response('home.html', locals(), context_instance=RequestContext(request))
    #1 if there is no user logged in then home.html will be shown
    #3 home.html is my front page <so you need to
    #4 if you see carefull this function is actually not used in the program as whole everything is handled by the
    #all function
    #5 home.html is my first function and you need to modify that

def all(request):
    if request.user.is_authenticated():  #6 if you are logged in then you will see the output otherwise only home.html
        #will be printed out to you
        #7 User is a predefined field in the django so you print out User it will show you
        # <<class 'django.contrib.auth.models.User'>
        #8 the user which is logged in has this property
        users = User.objects.filter(is_active=True)
        #print users[0] #13 it will printout the rrs402 user which is logged in there
        #print User.objects.all() #9 it will print out all the users which are present in my application
        try:
            matches = Match.objects.user_matches(request.user)  #10 Match is my model name which I have defined in my other
            #application matches
            #11 go to matches.models and then the function user_matches
            print matches
        except Exception:
            pass

        return render_to_response('profiles/all.html', locals(), context_instance=RequestContext(request))
    
    else:
        return render_to_response('front/index.html', locals(), context_instance=RequestContext(request))

def single_user(request, username):
    #14 this function will show you whether you are matched to a particular guy and how well you are matched to him/her
    #print username here the username is rrs402 the user which has logged into the website
    print username
    try:
        user = User.objects.get(username=username)
        if user.is_active:
            single_user = user
    except:
        raise Http404
    set_match, created = Match.objects.get_or_create(from_user=request.user, to_user=single_user)
    set_match.percent = round(match_percentage(request.user, single_user), 4)
    set_match.good_match = Match.objects.good_match(request.user, single_user)
    set_match.save()

    if set_match.good_match:
        single_user_jobs = Job.objects.filter(user=single_user)
        if len(single_user_jobs) > 0:
            for job in single_user_jobs:
                job_match, created = JobMatch.objects.get_or_create(user=request.user, job=job)
                print job_match
                job_match.save()
            
    
    match = set_match.percent * 100
    return render_to_response('profiles/single_user.html', locals(), context_instance=RequestContext(request))

def edit_profile(request):
    user = request.user
    picture = UserPicture.objects.get(user=user)
    addresses = Address.objects.filter(user=user)
    jobs = Job.objects.filter(user=user)
    user_picture_form = UserPictureForm(request.POST or None, request.FILES or None, prefix='pic', instance=picture)
    
    AddressFormset = modelformset_factory(Address, form=AddressForm, extra=1)
    formset_a = AddressFormset(queryset=addresses)
    
    JobFormset = modelformset_factory(Job, form=JobForm, extra=1)
    formset_j = JobFormset(queryset=jobs)
    
    if user_picture_form.is_valid():
        form3 = user_picture_form.save(commit=False)
        form3.save()
        
    return render_to_response('profiles/edit_profile.html', locals(), context_instance=RequestContext(request))

def edit_locations(request):
    if request.method == 'POST':
        user = request.user
        addresses = Address.objects.filter(user=user)
        
        # Address Formset
        AddressFormset = modelformset_factory(Address, form=AddressForm, extra=1)
        formset_a = AddressFormset(request.POST or None, queryset=addresses)
        
        if formset_a.is_valid():
           for form in formset_a:
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()
           messages.success(request, 'Profile details updated.')
           
        else:
            messages.error(request, 'Profile details did not update.')
        return HttpResponseRedirect('/edit/')
    
    else:
        raise Http404

    
def edit_jobs(request):
    if request.method == 'POST':
        user = request.user
        jobs = Job.objects.filter(user=user)
        
        # Job Formset
         
        JobFormset = modelformset_factory(Job, form=JobForm, extra=1)
        formset_j = JobFormset(request.POST, queryset=jobs)
        
        if formset_j.is_valid():
           for form in formset_j:
                new_form = form.save(commit=False)
                new_form.save()
           messages.success(request, 'Profile details updated.')
           
        else:
            messages.error(request, 'Profile details did not update.')
        return HttpResponseRedirect('/edit/')
    
    else:
        raise Http404
    

def find(request, username):

    #print request.user
    #user = User.objects.get(username=username)
    #job = Job.objects.filter(user=user)[1]  #it will return the object but you need specific element so this has
    #has to be used
    #print job.phone
    #print job.phone  #you need specific element in the object
    return render_to_response('backend/page2.html', locals(), context_instance=RequestContext(request))

def message(request, username):

    from twilio.rest import TwilioRestClient

    # put your own credentials here
    ACCOUNT_SID = "AC976f8a49a80efa6b3080e7316a43376e"
    AUTH_TOKEN = "130891e26dd1555afa339289188dbc1d"


    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    client.messages.create(to="+13024385450",  #9292389138
        from_="+13024070522", body="My profile perfectly matches with you. Let's connect")

    return render_to_response('backend/page2.html', locals(), context_instance=RequestContext(request))

def call(request, username):

    from twilio.rest import TwilioRestClient

    account = "AC976f8a49a80efa6b3080e7316a43376e"
    token = "130891e26dd1555afa339289188dbc1d"
    client = TwilioRestClient(account, token)

    call = client.calls.create(to="+13024385450",
        from_="+13024070522", url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
    print(call.sid)
#http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient

    return render_to_response('backend/page2.html', locals(), context_instance=RequestContext(request))

def search(request, username):

    obj = urllib2.urlopen("https://api.fullcontact.com/v2/person.json?email=rakesh.sukla53@gmail.com&apiKey=cee8985b6055428a")

    data = json.load(obj)

    fullName = data['contactInfo']['fullName']

    for line in data['socialProfiles']:
        try:
            if line['typeId'] == 'facebook':
                try:
                    facebookUrl = line['url']
                    facebookName = line['username']
                except:
                    pass
        except:
            pass
        try:
            if line['typeId'] == 'twitter':
                try:
                    twitterUrl = line['url']
                    twitterName = line['username']
                except:
                    pass
        except:
            pass
        try:

            if line['typeId'] == 'linkedin':
                try:
                    linkedUrl = line['url']
                    linkedId = line['id']
                except:
                    pass
        except:
            pass
        try:
            if line['typeId'] == 'pinterest':
                try:
                    pinterestUrl = line['url']
                    pinterestName = line['username']
                except:
                    pass
        except:
            pass


    return render_to_response('backend/page4.html', locals(), context_instance=RequestContext(request))

def job(request, username):

    __author__ = 'rakesh'

    #http://api.glassdoor.com/api/api.htm?t.p=34771&t.k=hY4Dey9RoIE&userip=0.0.0.0&useragent=&format=json&v=1&action=jobs-stats&returnStates=true&admLevelRequested=1

    #for finding all the jobs related to that particular area

    #http://api.glassdoor.com/api/api.htm?t.p=34771&t.k=hY4Dey9RoIE&userip=0.0.0.0&useragent=&format=json&v=1&action=employers&city=New%20York

    #Especially related to JOB TITLE ..find all the jobs and theirs links

    #http://api.glassdoor.com/api/api.htm?t.p=34771&t.k=hY4Dey9RoIE&userip=0.0.0.0&useragent=&format=json&v=1&action=employers&city=New%20York&jobTitle=Software
    '''
    HTTP REQUEST can be modified and changed accordingly
    Also go through this http://www.glassdoor.com/api/jobsApiActions.htm
    '''
    import urllib2
    import json

    site = "http://api.glassdoor.com/api/api.htm?t.p=34771&t.k=hY4Dey9RoIE&userip=0.0.0.0&useragent=&format=json&v=1&action=employers&city=New%20York&jobTitle=Software"
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    req = urllib2.Request(site, headers=hdr)

    page = urllib2.urlopen(req)

    data = json.load(page)

    employerInfo = data['response']['employers']

    employerName = []

    for line in employerInfo:
        employerName.append(line['name'])
        employerName.append(line['featuredReview']['location'])
        employerName.append(line['website'])



    return render_to_response('backend/job-search.html', locals(), context_instance=RequestContext(request))








































