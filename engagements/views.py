from django.shortcuts import render


def search_engagements(request):
    return render(request, 'engagements/search.html', {'description': 'search form and results'})


def register_and_create_engagement(request):
    return render(
        request,
        'engagements/register_requester.html',
        {'description': 'registration form with engagement creation'},
    )


def create_engagement(request):
    return render(
        request,
        'engagements/create.html',
        {'description': 'create new engagement for logged in user'},
    )


def create_engagement_thanks(request):
    return render(
        request,
        'engagements/create_thanks.html',
        {'description': 'thanks page for engagement creation'},
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
