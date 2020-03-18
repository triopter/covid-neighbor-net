from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from engagements.forms import RequesterRegistrationForm


def search_engagements(request):
    return render(request, 'engagements/search.html', {'description': 'search form and results'})


def register_and_create_engagement(request):
    if request.method == 'POST':
        form = RequesterRegistrationForm(request.POST)
        if form.is_valid():
            engagement = form.save()
            return HttpResponseRedirect(
                reverse('create_engagement_thanks', kwargs={'engagement_id': engagement.id})
            )
    else:
        form = RequesterRegistrationForm()

    return render(request, 'engagements/register_requester.html', {'form': form},)


def create_engagement(request):
    return render(
        request,
        'engagements/create.html',
        {'description': 'create new engagement for logged in user'},
    )


def create_engagement_thanks(request, engagement_id):
    return render(
        request,
        'engagements/create_thanks.html',
        {
            'description': 'thanks page for engagement creation. visible only to creator, 403 for other users'
        },
    )


def register_and_claim_engagement(request, engagement_id):
    return render(
        request,
        'engagements/register_volunteer.html',
        {'description': 'registration form that also claims a previously clicked engagement'},
    )


def claim_engagement(request, engagement_id):
    return render(
        request,
        'home.html',
        {
            'description': 'assign engagement to already registered user. once implemented, this view will redirect instead of rendering'
        },
    )


def engagement_detail(request, engagement_id):
    return render(
        request,
        'engagements/detail.html',
        {
            'description': 'shows full detail (including contact info) of engagement.  Visible only to confirmed claimant, 403 for all other users.'
        },
    )
