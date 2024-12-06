import requests
from .parser import parse_curl

class reqcurl:
    """
    Wrapper class to execute API requests from cURL commands.
    """

    def execute(self, curl_command):
        """
        Executes the given cURL command using the requests library.
        """
        parsed_request = parse_curl(curl_command)

        response = requests.request(
            method=parsed_request["method"],
            url=parsed_request["url"],
            headers=parsed_request["headers"],
            data=parsed_request["data"],
            auth=parsed_request["auth"]
        )

        return response
