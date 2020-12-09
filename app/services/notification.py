from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    # PushResponseError,
)

from app.services.user import UserService


class Notification:
    def __init__(self, user_svc: UserService) -> None:
        self.user_svc = user_svc


# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token, message, extra=None):
    response = PushClient().publish(PushMessage(to=token, body=message, data=extra))
    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        # self.user_svc.edit_user()
        # Mark the push token as inactive
        # PushToken.objects.filter(token=token).update(active=False)
        print("device not registered")
    except Exception as exc:
        # Encountered some other per-notification error.
        raise exc
