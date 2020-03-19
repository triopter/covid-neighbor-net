from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from engagements.forms import RequesterRegistrationForm
from engagements.models import Engagement


def search_engagements(request):
    return render(request, 'engagements/search.html', {'description': 'search form and results'})


def register_and_create_engagement(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('create_engagement'))

    if request.method == 'POST':
        form = RequesterRegistrationForm(request.POST)
        if form.is_valid():
            engagement = form.save()
            login(request, engagement.requester)
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
    engagement = get_object_or_404(Engagement, id=int(engagement_id))
    if engagement.requester != request.user:
        raise PermissionDenied
    return render(request, 'engagements/create_thanks.html', {'engagement': engagement},)


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
