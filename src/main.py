##############################
# Program Entry
##############################
##############################
# Program Entry
##############################
from src.skill.intents.generic_intent_handlery import GenericIntentHandler
from src.skill.utils.constants import Constants
from src.skill.utils.exceptions import BackendException
from src.skill.utils.responses import statement, ResponseOptions


def lambda_handler(event, context):
    locale = event['request']['locale']
    request_type = event['request']['type']  # 'LaunchRequest' or 'IntentRequest'
    # cuz CustomIntentHandler does not exist yet. Needed for error messages
    generic_handler = GenericIntentHandler(locale)
    response_options = ResponseOptions()

    if Constants.APPLICATION_ID != event['session']['application']['applicationId']:
        response_options.set_options(generic_handler.i18n.ERROR, generic_handler.i18n.ERROR)
        return statement(response_options)
    try:
        if 'accessToken' not in event['session']['user']:
            Constants.ACCESS_TOKEN = None
        else:
            Constants.ACCESS_TOKEN = event['session']['user']["accessToken"]

        if Constants.ROUTER is None:
            try:
                Constants.ROUTER = IntentRouter(locale)
            except IndexError:
                # ok: self.bingbong_account_id = self.bingbong_service.get_bingbong_account().id
                # throws error. Not exactly sure why this happens..
                # actually I check if the user deletes his account --> http error 401
                title = generic_handler.i18n.ACCOUNT_LINKING_REQUIRED_TITLE
                body = generic_handler.i18n.ACCOUNT_LINKING_REQUIRED
                response_options.set_options(title, body, account_card=True)
                return statement(response_options)

        if event['session']['new']:
            # Constants.ROUTER.custom_intent_handler.update_objects_on_new_session()
            pass
        else:
            # Constants.ROUTER.custom_intent_handler.update_objects_on_new_lambda_call(locale)
            pass

        if request_type == 'LaunchRequest':
            return Constants.ROUTER.route_launch_request(event, context)
        elif request_type == 'IntentRequest':
            return Constants.ROUTER.route_intent_request(event, context)
    except BackendException as http_error_code:
        if http_error_code.args[0] == 401:
            # Unauthorized: Happens when user enables alexa skill with valid account
            # then deletes account on my webserver and uses skill again
            title = generic_handler.i18n.ACCOUNT_LINKING_REQUIRED_TITLE
            body = generic_handler.i18n.ACCOUNT_LINKING_REQUIRED
            response_options.set_options(title, body, account_card=True)
            return statement(response_options)

        if 500 <= http_error_code.args[0] < 600:
            response_options.set_options(generic_handler.i18n.ERROR,
                                         generic_handler.i18n.SERVER_ERROR)
            return statement(response_options)
        else:
            response_options.set_options(generic_handler.i18n.BACKEND_EXCEPTION_TITLE,
                                         generic_handler.i18n.BACKEND_EXCEPTION)
            return statement(response_options)
