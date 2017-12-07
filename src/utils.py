import argparse


def get_output_arg_parser(description="", default_credentials="", default_input_file=""):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--credentials', dest="credentials",
                        default=default_credentials,
                        help='path to the credentials file to use to authenticate over the API.')
    parser.add_argument('--output', dest="dump_file",
                        default=default_input_file,
                        help='path of the file where the data must be written')
    return parser


def get_input_arg_parser(description="", default_credentials="", default_input_file=""):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--credentials', dest="credentials",
                        default=default_credentials,
                        help='path to the credentials file to use to authenticate over the API.')
    parser.add_argument('--output', dest="dump_file",
                        default=default_input_file,
                        help='path of the file to use as the data input')
    return parser
