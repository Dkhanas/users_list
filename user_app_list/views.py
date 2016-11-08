import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from user_app_list.forms import SearchForm
from user_app_list.models import User, Comments


def index(request):
    get_users = User.objects.all()
    form = SearchForm(request.GET)
    responce = {}
    if request.is_ajax():
        if request.GET.get('created'):
            if request.GET.get('created') == 'ASC':
                users_qs = get_users.order_by('create_date').values(
                    'first_name', 'last_name', 'phone', 'address'
                )
                responce['ASC'] = json.dumps(
                    list(users_qs)
                )
            else:
                users_qs = get_users.order_by('-create_date').values(
                    'first_name', 'last_name', 'phone', 'address'
                )
                responce['DESC'] = json.dumps(
                    list(users_qs)
                )
            return JsonResponse(responce)
    results = []
    if form.is_valid():
        queries = [Q(**{
            '{}__icontains'.format(field_name): form.cleaned_data[field_name]})
                   for field_name in form.cleaned_data if
                   form.cleaned_data[field_name]]
        if queries:
            query = queries.pop()
            for item in queries:
                query |= item
            results = User.objects.filter(query)
    return render(request, 'base.html', {
        'users': get_users,
        'form': form,
        'search_results': results
    }
                  )
