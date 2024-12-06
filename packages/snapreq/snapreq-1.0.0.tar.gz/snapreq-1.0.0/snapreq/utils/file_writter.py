from requests.models import Response
import json
import os

def write_response_to_file(response: Response, file_path: str) -> None:
    content_type = response.headers.get('Content-Type', '')

    if 'application/json' in content_type:
        file_path = file_path if file_path.endswith('.json') else f"{file_path}.json"
        with open(file_path, 'w') as file:
            json.dump(response.json(), file, indent=4)
    elif 'image/' in content_type:
        extension = content_type.split('/')[1]
        file_path = file_path if file_path.endswith(f'.{extension}') else f"{file_path}.{extension}"
        with open(file_path, 'wb') as file:
            file.write(response.content)
    else:
        file_path = file_path if file_path.endswith('.txt') else f"{file_path}.txt"
        with open(file_path, 'w') as file:
            file.write(response.text)
