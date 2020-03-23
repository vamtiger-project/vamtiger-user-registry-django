from json import loads as json_parse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.utils.http import urlencode
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import UserRegistry, UserRegistryForm, UserRegistryUpdateForm

class ResponseResult:
    successful = 'successful'
    failed = 'failed'
    error = 'error'

class ResponseMessage:
    added_new_user = 'added new user'
    failed_to_add_new_user = 'failed to add new user'
    retrieved_users = 'Retrieved user(s)'
    updated_user = 'Updated user'
    failed_to_update_user = 'Failed to update user'
    error_updating_user = 'Error updating user',
    removed_user = 'Removed user',
    failed_to_remove_user = 'Failed to remove user'

class ResponseErrorMessage:
    no_user_found_for_user_id = 'No user for user id',
    this_field_is_required = 'This field is required'

class Config:
    page_size = 10

@csrf_exempt
def add_new_user(request):
    response = {
        'POST': __add_new_user
    }
    get_response = response[request.method] or __not_found

    return JsonResponse(get_response(request))

@csrf_exempt
def handle_user(request, user_id):
    response = {
        'GET': __get_user,
        'PUT': __update_user,
        'DELETE': __delete_user
    }
    get_response = response[request.method] or __not_found

    return JsonResponse(get_response(request, user_id))

def get_users(request):
    response = {
        'GET': __get_users
    }
    get_response = response[request.method] or __not_found

    return JsonResponse(get_response(request))

def __not_found():
    response = {
        'status_code': 404,
        'error': 'The resource was not found',
        'result': ResponseResult.error
    }

    return response

def __add_new_user(request):
    user = UserRegistryForm(request.POST or {})

    if user.is_valid():
        user.save()
        response = {
            'result': 'successful',
            'data': {
                'user': user.instance.id
            }
        }
    else:
        response = {
            'result': ResponseResult.failed,
            'message': ResponseMessage.failed_to_add_new_user,
            'data': user.getResponseErrorData()
        }

    return response

def __get_user(request, user_id):
    user = UserRegistry.objects.get(id=user_id)
    response = None

    if user:
        response = {
            'result': ResponseResult.successful,
            'message': ResponseMessage.retrieved_users,
            'data': {
                'user': model_to_dict(user)
            }
        }
    else:
        response = __not_found()

        response['message'] = ResponseErrorMessage.no_user_found_for_user_id
        response['data'] = {
            'user_id': user_id
        }

    return response

def __get_users(request):
    url = request.path
    page = request.GET.get('page')
    users = UserRegistry.objects.all()
    paginator = Paginator(users, Config.page_size)
    page_number = 1 if page == None else min(int(page), paginator.num_pages)
    users_page = paginator.get_page(page_number)
    users = list(map(lambda user: model_to_dict(user), users_page.object_list))
    response = {
        'result': ResponseResult.successful,
        'message': ResponseMessage.retrieved_users,
        'data': {
            'users': {
                'path': url,
                'current_page': page_number,
                'from': users_page.paginator.page_range.start,
                'to': users_page.paginator.num_pages,
                'last_page': users_page.paginator.num_pages,
                'per_page': users_page.paginator.per_page,
                'total': users_page.paginator.count,
                'data': users,
                'first_page_url': '%s?%s' % (url, urlencode({'page': users_page.paginator.page_range.start}))
            }
        }
    }

    if users_page.paginator.num_pages > 1:
        response['data']['users']['last_page_url'] = '%s?%s' % (url, urlencode({'page': users_page.paginator.num_pages}))

    if page_number > 1:
        response['data']['users']['prev_page_url'] = '%s?%s' % (url, urlencode({'page': page_number - 1}))

    if users_page.has_next():
        response['data']['users']['next_page_url'] = '%s?%s' % (url, urlencode({'page': page_number + 1}))

    return response

def __update_user(request, user_id):
    response = None

    try:
        userData = {k: v for k, v in json_parse(request.body.decode()).items() if v}
        userForm = UserRegistryUpdateForm(userData, None)
        fields = userForm.Meta.fields
        user = UserRegistry.objects.only(*fields).get(id=user_id) if userForm.is_valid() else None

        if (user):
            for field in fields:
                setattr(user, field, userForm.cleaned_data[field])

            user.save(update_fields=fields)

            response = {
                'result': ResponseResult.successful,
                'message': ResponseMessage.updated_user,
                'data': {
                    'user': user_id
                }
            }
        else:
            response = {
                'result': ResponseResult.failed,
                'message': ResponseMessage.failed_to_update_user,
                'data': {
                    'user': user_id
                }
            }
    except:
        response = {
            'result': ResponseResult.error,
            'message': ResponseMessage.error_updating_user,
            'data': {
                'user': user_id
            }
        }

    return response

def __delete_user(request, user_id):
    response = None
    deleteUser = None

    try:
        deleteUser = UserRegistry.objects.get(id=user_id).delete()
        response = {
            'result': ResponseResult.successful,
            'message': ResponseMessage.removed_user,
            'data': {
                'user': user_id,
                'delete': deleteUser[0]
            }
        }
    except:
        response = {
            'result': ResponseResult.failed,
            'message': ResponseMessage.failed_to_remove_user,
            'data': {
                'user': user_id,
                'delete': 0
            }
        }

    return response