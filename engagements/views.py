from django.http import HttpResponse
from django.shortcuts import render


def search_engagements(request):
    return HttpResponse('search form and results')


def register_and_create_engagement(request):
    return HttpResponse('registration form with engagement creation')


def create_engagement(request):
    return HttpResponse('create new engagement for logged in user')


def create_engagement_thanks(request):
    return HttpResponse('thanks page for engagement creation')


def register_and_claim_engagement(request, engagement_id):
    return HttpResponse('registration form that also claims a previously clicked engagement')


def claim_engagement(request, engagement_id):
    return HttpResponse('assign engagement to already registered user')


def engagement_detail(request, engagement_id):
    return HttpResponse(
        'shows full detail (including contact info) of engagement.  Visible only to confirmed claimant, 403 for all other users.'
    )
