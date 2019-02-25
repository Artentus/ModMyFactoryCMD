import sys
import requests
import ApiDefinitions


API_DOMAIN = "https://auth.factorio.com"
LOGIN_ENDPOINT = API_DOMAIN + "/api-login"

class LoginError(ApiDefinitions.ApiError, ApiDefinitions.ServerError):
    """
    An error indicating an unsuccessful login atempt.
    
    message : str
        The error message returned by the server.
    status_code : int
        The http status code returned by the server.
    """

    def __init__(self, message, status_code):
        """
        Create a new LoginError instance.

        message : str
            The error message returned by the server.
        status_code : int
            The http status code returned by the server.
        """

        self.message = message
        self.status_code = status_code

def login(username_or_email, password, require_game_ownership=False, api_version=2):
    """
    Logs into the Factorio servers.

    Parameters
    ----------
    username_or_email : str
        The users name or email.
    password : str
        The users password.
    require_game_ownership : bool, optional
        Indicates whether the user has to own the game to successfully log in.
    api_version : int, optional
        The API version to use.

    Returns
    -------
    (username, token) : (str, str)
        A pair of usename and token to use with other APIs.

    Raises
    ------
    LoginError
        If the login was unsuccessful.
    """

    payload = dict(username=username_or_email, password=password, require_game_ownership=require_game_ownership, api_version=api_version)
    response = requests.post(LOGIN_ENDPOINT, data=payload)

    result = {}
    try:
        result = response.json()
    except:
        raise LoginError("No message", response.status_code)
    else:
        if (response.status_code != requests.codes.ok):
            message = ""
            try:
                message = result["message"]
            except:
                message = "No message"
            raise LoginError(message, response.status_code)

        return (result["username"], result["token"])


if (__name__ == '__main__'):
    args = sys.argv[1:]

    if (len(args) != 2):
        print("Usage: FactorioAuth.py <username> <password>")
        sys.exit()

    try:
        username, token = login(args[0], args[1])
    except LoginError as err:
        print("Login failed! Code {0}: {1}".format(err.status_code, err.message))
    else:
        print("Username:", username)
        print("Token:", token)