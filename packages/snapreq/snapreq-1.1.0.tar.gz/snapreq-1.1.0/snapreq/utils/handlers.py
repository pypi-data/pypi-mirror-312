import requests
from requests.models import Response
from . import RequestMethod, transfer_str_to_dict, write_response_to_file
from snapreq.console.logger import loading_required, print_response, print_error

@loading_required
def make_request(method: RequestMethod, url, headers=None, data=None, params=None):
    headers = transfer_str_to_dict(headers) if headers else {}
    data = transfer_str_to_dict(data) if data and method.name != 'GET' else {}
    params = transfer_str_to_dict(params) if params else {}
    return requests.request(method.name, url, headers=headers, json=data, params=params)    

def handle_request(args):
    return make_request(
        args.method,
        args.url,
        args.headers,
        params=getattr(args, "params", None),
        data=getattr(args, "data", None),
        label=args.method.in_progress_msg(),
        completion_message=args.method.completed_msg(args.url)
    )

def handle_response(res: Response, args):
    if res.status_code < 400:
        print_response(res, args.method, args.show_headers)
        if args.output:
            write_response_to_file(res, args.output)
    else:
        if res.headers.get('Content-Type', '').startswith('application/json'):
            error_data = res.json()
            print_error(f"{res.status_code} - {res.reason}", error_data)
        else:
            print_error(f"{res.status_code} - {res.reason}\n{res.text}")
