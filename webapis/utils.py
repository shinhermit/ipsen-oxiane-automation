import argparse


def get_output_arg_parser(description="", parents=()):
    parser = argparse.ArgumentParser(description=description, parents=parents)
    parser.add_argument('--credentials',
                        dest="credentials",
                        required=True,
                        help='path to the credentials file to use to authenticate over the API.')
    parser.add_argument('--output',
                        dest="dump_file",
                        required=True,
                        help='path of the file where the data must be written')
    return parser


def get_input_arg_parser(description="", parents=None):
    parser = argparse.ArgumentParser(description=description, parents=parents)
    parser.add_argument('--credentials',
                        dest="credentials",
                        required=True,
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
