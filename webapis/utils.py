import argparse


def get_output_arg_parser(description: str="", require_credentials: bool=True,
                          parents: tuple=()) -> argparse.ArgumentParser:
    """
    Provide an arg parser for scripts that dump data to a file.

    The parser will expect the arguments:
    * --credentials: path to the credentials file to use to authenticate over the API.
    * --output: path of the file where the data must be written

    :param description: description of the parser
    :param require_credentials: tell whether or not the credentials
    argument must be required.
    :param parents: parents parser. Especially useful for Google API Client.
    """
    parser = argparse.ArgumentParser(description=description, parents=parents)
    parser.add_argument('--credentials',
                        dest="credentials",
                        required=require_credentials,
                        help='path to the credentials file to use to authenticate over the API.')
    parser.add_argument('--output',
                        dest="dump_file",
                        required=True,
                        help='path of the file where the data must be written')
    return parser


def get_input_arg_parser(description: str="", require_credentials: bool=True,
                         parents: tuple=()) -> argparse.ArgumentParser:
    """
    Provide an arg parser for scripts that process data from a file.

    The parser will expect the arguments:
    * --credentials: path to the credentials file to use to authenticate over the API.
    * --input: path of the file to use as the data input

    :param description: description of the parser
    :param require_credentials: tell whether or not the credentials
    argument must be required.
    :param parents: parents parser. Especially useful for Google API Client.
    """
    parser = argparse.ArgumentParser(description=description, parents=parents)
    parser.add_argument('--credentials',
                        dest="credentials",
                        required=require_credentials,
                        help='path to the credentials file to use to authenticate over the API.')
    parser.add_argument('--input',
                        dest="input_file",
                        required=True,
                        help='path of the file to use as the data input')
    return parser


def substring_before(initial_str: str, sub: str) -> str:
    """
    Substring *initial_str* before the first occurrence of *sub*.

    example:
    ```
    from src import utils
    utils.substring_before("www.ipsen.co.uk/", ".uk/")

    > "www.ipsen.co"
    ```

    :param initial_str: the string to be sub-stringed
    :param sub: the substring to cut before
    """
    return initial_str.split(sub, 1)[0]


def substring_after(initial_str: str, sub: str) -> str:
    """
    Substring *initial_str* after the first occurrence of *sub*.

    example:
    ```
    from src import utils
    utils.substring_before("www.ipsen.co.uk/", "www.")

    > "ipsen.co.uk/"
    ```

    :param initial_str: the string to be sub-stringed
    :param sub: the substring to cut before
    """
    parts = initial_str.split(sub, 1)
    if len(parts) > 1:
        return parts[1]
    return parts[0]


def get_domain_name_from_url(url: str) -> str:
    """
    Extract the domain name from an URL.

    Given an URL in the form http://www.ipsen.com/fr/,
    returns ipsen.com

    :param url: the URL from wich we want to extract a domain name
    :return: the domain name extracted from the URL
    """
    wo_url = substring_after(substring_after(substring_after(url, "http://"), "https://"), "www.")
    return substring_before(wo_url, "/")


class Console:
    """
    Helper to print messages in the console.
    """
    # console color codes
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END_COL = '\033[0m'

    @staticmethod
    def print_header(*msg: str):
        print(Console.HEADER, *msg, Console.END_COL)

    @staticmethod
    def print_yellow(*msg: str):
        print(Console.YELLOW, *msg, Console.END_COL)

    @staticmethod
    def print_green(*msg: str):
        print(Console.GREEN, *msg, Console.END_COL)

    @staticmethod
    def print_red(*msg: str):
        print(Console.RED, *msg, Console.END_COL)

    @staticmethod
    def print_good_bye_message():
        print(Console.HEADER + goodbye_msg + Console.END_COL)


goodbye_msg = """
-------------------------------------------------------------------------------------------------
**                                                                                             **
**                                      Good bye                                               **
**                                                                                             **
-------------------------------------------------------------------------------------------------
"""
