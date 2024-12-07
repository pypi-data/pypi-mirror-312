import argparse
from snapreq.utils import METHODS, handle_request, handle_response, print_error


def main():
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(description="SnapReq: A simple API Client")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    for method_name, method in METHODS.items():
        parser_method = subparsers.add_parser(method_name, help=f"Make a {method.name} request")
        parser_method.add_argument("url", help="API endpoint URL")
        parser_method.add_argument("--headers", help="Headers as a string of key-value pairs (e.g. header1=value1&header2=value2)")
        parser_method.add_argument("--show-headers", '-sh', action="store_true", help="Show response headers")
        parser_method.add_argument("--output", '-o', help="Output file path")
        
        if method_name == "get":
            parser_method.add_argument("--params", '-p', help="Query parameters as a string of key-value pairs (e.g. key1=value1&key2=value2)")
        else:
            parser_method.add_argument("--data", '-d', help="Payload as a string of key-value pairs (e.g. key1=value1&key2=value2)")

        parser_method.set_defaults(func=handle_request, method=method)

    # Parse arguments
    args = parser.parse_args()

    if args.command:
        try:
            res = args.func(args)
            handle_response(res, args)
        except Exception as e:
            print_error(str(e))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()