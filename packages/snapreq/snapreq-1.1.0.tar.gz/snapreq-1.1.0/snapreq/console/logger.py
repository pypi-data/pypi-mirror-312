from typing import Callable, Optional
from rich.console import Console, Group
from rich.panel import Panel
from rich.json import JSON
from snapreq.utils.methods import RequestMethod
from requests.models import Response
import time

CONSOLE = Console()



def print_response(res: Response, req_mehtod: RequestMethod, show_headers: bool=False):
    if show_headers:
        formatted_headers = "\n".join([f"[bold blue]{key}[/bold blue]: [green]{value}[/green]" for key, value in res.headers.items()])
    else:
        formatted_headers = None
        
    title = f"HTTP: {res.status_code} ({res.reason})"
    # print the response JSON if the 'Content-Type' == 'application/json' else just print the 'Content-Type'
    if 'application/json' in res.headers.get('Content-Type', ''):
        content = JSON.from_data(res.json())
    else:
        content = res.headers.get('Content-Type', 'No Content-Type')
    
    if formatted_headers:
        content_panel = Panel(
            content,
            title="Response",
            title_align='left',
            border_style=req_mehtod.color,
            padding=(1, 2),
        )
        main_panel_content = Group(content_panel, formatted_headers)
        CONSOLE.print(
            Panel(
                main_panel_content,
                title=title,
                title_align="left",
                padding=(1, 2),
            )
        )
    else:
        CONSOLE.print(
            Panel(
                content,
                title=f"{title} | Response",
                title_align='left',
                border_style=req_mehtod.color,
                padding=(1, 2),
            )
        )


def print_error(error_msg: str, error_data: Optional[dict] = None):
    if not error_data:
        CONSOLE.print(
            Panel(
                f"[bold red]{error_msg}",
                title="Error",
                title_align="left",
                border_style="red",
                padding=(1, 2),
            )
        )
    else:
        content_panel = Panel(
            JSON.from_data(error_data),
            # title="Details",
            title_align='left',
            border_style='yellow',
            padding=(1, 1),
        )
        error_str = f"[bold red]{error_msg}"
        main_panel_content = Group(error_str, content_panel)
        CONSOLE.print(
            Panel(
                main_panel_content,
                title="Error",
                title_align="left",
                border_style='red',
                padding=(0, 2),
            )
        )
    

def loading_required(task: Callable) -> Callable:
    def wrapper(*args, label: str = "Loading", completion_message: str = "Completed", **kwargs):
            start_time = time.time()
            with CONSOLE.status(f"[bold green]{label}") as status:
                result = task(*args, **kwargs)
            elapsed_time = time.time() - start_time
            CONSOLE.log(f"{completion_message} in {elapsed_time:.2f} seconds")
            return result
    return wrapper