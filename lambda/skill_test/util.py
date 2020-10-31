TEST_USER_AUTHORIZED = 'test_user_authorized'
TEST_USER_UNAUTHORIZED = 'test_user_unauthorized'


def update_request(request, locale, user_id):
    request["session"]["user"]["userId"] = user_id
    request["context"]["System"]["user"]["userId"] = user_id
    request["request"]["locale"] = locale
    return request
