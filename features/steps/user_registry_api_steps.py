from json import dumps as json_stringify
from functools import reduce
from faker import Faker
from user_registry_api.models import UserRegistry
from user_registry_api.rest import ResponseResult, ResponseMessage, ResponseErrorMessage

faker = Faker()

@given("a new user")
def step_impl(context):
    userData = __get_user_data()
    context.userData = userData


@when('posted to {url}')
def step_impl(context, url):
    userData = context.userData
    response = context.test.client.post(url, userData).json()
    errors = None

    if response['result'] == ResponseResult.failed:
        for fields_errors in response['data'].values():
            errors = reduce(lambda errors, data: errors + [data['error']], fields_errors, [])

    context.response = response
    context.errors = errors

@then('a new record should be added to the Users table')
def step_impl(context):
    userData = context.userData
    userRecord = UserRegistry.objects.get(email=userData['email'])

    context.test.assertIsNotNone(userRecord)

@given('a new user without a required field (e.g. {required_field_name})')
def step_impl(context, required_field_name):
    userData = __get_user_data()
    userDataMissingRequiredField = {k: v for k, v in userData.items() if k != required_field_name}

    context.userData = userDataMissingRequiredField

@then('response from {response_url} should fail with "{response_error}"')
def step_impl(context, response_url, response_error):
    context.test.assertEqual(ResponseResult.failed, context.response['result'])
    context.test.assertEqual(ResponseMessage.failed_to_add_new_user, context.response['message'])
    context.test.assertEqual(
        True,
        all(error.startswith(response_error) for error in context.errors)
    )

@given('a new user with numbers in the {nameField} or {surnameField} fields')
def step_impl(context, nameField, surnameField):
    userData = __get_user_data()

    userData[nameField] = '%s %s' % (1, userData[nameField])
    userData[surnameField] = '%s %s' % (userData[surnameField], 2)

    context.userData = userData

@given('a new user with an invalid {emailField}')
def step_impl(context, emailField):
    userData = __get_user_data()

    userData[emailField] = userData[emailField].replace('@', '=')

    context.userData = userData

@given('a new user posted to {url}')
def step_impl(context, url):
    userData = __get_user_data()
    response = context.test.client.post(url, userData)
    userRecord = UserRegistry.objects.get(email=userData['email'])

    context.userData  = userData
    context.userRecord = userRecord

@when('requested from {url_prefix}/<int:user_id>')
def step_impl(context, url_prefix):
    url = "%s/%s" % (url_prefix, context.userRecord.id)
    response = context.test.client.get(url)
    userResponse = response.json()

    context.userResponse = userResponse

@then('a user record should be retrieved')
def step_impl(context):
    userData = context.userData
    userResponse = context.userResponse

    context.test.assertEqual(True, set(userData.items()).issubset(set(userResponse['data']['user'].items())))

@given('{number_of_users:d} users posted to {url}')
def step_impl(context, number_of_users, url):
    userDataList = __get_user_data_list(number_of_users)
    responses = list(map(lambda userData: context.test.client.post(url, userData), userDataList))

@when('all users are requested from {url}')
def step_impl(context, url):
    response = context.test.client.get(url)
    paginatedUserResponse = response.json()
    paginatedUserResponses = [paginatedUserResponse]
    nextUrl = paginatedUserResponse['data']['users']['next_page_url']

    while nextUrl:
        response = context.test.client.get(nextUrl)
        paginatedUserResponse = response.json()

        paginatedUserResponses.append(paginatedUserResponse)

        if 'next_page_url' in paginatedUserResponse['data']['users']:
            nextUrl = paginatedUserResponse['data']['users']['next_page_url']
        else:
            nextUrl = None

    context.paginatedUserResponses = paginatedUserResponses

@then('{users_per_page:d} users per page should be retrieved')
def step_impl(context, users_per_page):
    context.test.assertEqual(
        True,
        all(len(response['data']['users']['data']) == users_per_page for response in context.paginatedUserResponses)
    )

@when('updated user data put to {url_prefix}/<int:user_id>')
def step_impl(context, url_prefix):
    url = '%s/%s' % (url_prefix, context.userRecord.id)
    updatedUserData = __get_user_data()
    updateResponse = context.test.client.put(url,json_stringify(updatedUserData)).json()
    updatedUserRecord = UserRegistry.objects.get(id=context.userRecord.id)

    context.updatedUserData = updatedUserData
    context.updatedUserRecord = updatedUserRecord
    context.updateResponse = updateResponse

@then('the user record should be updated')
def step_impl(context):
    context.test.assertNotEqual(context.userRecord.name, context.updatedUserRecord.name)
    context.test.assertNotEqual(context.userRecord.surname, context.updatedUserRecord.surname)
    context.test.assertNotEqual(context.userRecord.email, context.updatedUserRecord.email)
    context.test.assertNotEqual(context.userRecord.position, context.updatedUserRecord.position)

@when('deleted using {url_prefix}/<int:user_id>')
def step_impl(context, url_prefix):
    url = '%s/%s' % (url_prefix, context.userRecord.id)
    deleteResponse = context.test.client.delete(url).json()

    context.deleteResponse = deleteResponse

@then('the user record should be removed')
def step_impl(context):
    context.test.assertEqual(0, len(UserRegistry.objects.filter(id=context.userRecord.id)))

def __get_user_data():
    userData = {
        'name': faker.first_name(),
        'surname': faker.last_name(),
        'email': faker.email(),
        'position': faker.job()
    }

    return userData

def __get_user_data_list(size):
    userData = []

    for i in range(size):
        userData.append(__get_user_data())

    return userData