from webapis.utils import Console


def batch_http_request_default_callback(request_id: str, response: object, exception: Exception):
    """
    Default response handler for the Google API Client's BatchHttpRequest.

    Print the api response to the console.

    :param request_id: ID of the request in the batch
    :param response: response string from the API
    :param exception: when an error occured
    """
    if exception is not None:
        Console.print_red(str(exception))
    elif response:
        print(response)
    else:
        print("\tOK")
