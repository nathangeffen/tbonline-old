from django.shortcuts import render_to_response
from django.template import RequestContext
from userprofiles.forms import UserForm
from userprofiles.forms import UserProfileForm
from userprofiles.models import UserProfile


def update_profile(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            user_form = UserForm(request.POST,
                                 instance=request.user,)
            profile_form = UserProfileForm(request.POST,
                                           request.FILES,
                                           instance=request.user.userprofile)
            
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
        else:
            try:
                profile = request.user.userprofile
            except UserProfile.DoesNotExist:
                profile = UserProfile(user=request.user)
                profile.save()
                
        profile_form = UserProfileForm(instance=request.user.userprofile)
        user_form = UserForm(instance=request.user)

        context = {'user_form':user_form,
                   'profile_form':profile_form,
                   }
        return render_to_response('userprofiles/edit_profile.html',
                                  context,
                                  RequestContext(request))
        
    
