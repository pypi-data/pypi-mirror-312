class RequestMethod:
    name: str
    color: str
    
    def in_progress_msg(self) -> str:
        pass
    
    def completed_msg(self, url) -> str:
        return f"[{self.color}]{self.name}[/{self.color}] {url} completed"
        
    def __str__(self):
        return self.name
    

class Get(RequestMethod):
    name = "GET"
    color = "cyan"
    
    def in_progress_msg(self):
        return f"Fetching data"
    

class Post(RequestMethod):
    name = "POST"
    color = "magenta"
    
    def in_progress_msg(self):
        return f"Posting data"

class Put(RequestMethod):
    name = "PUT"
    color = "yellow"
    
    def in_progress_msg(self):
        return f"Updating data"

class Patch(RequestMethod):
    name = "PATCH"
    color = "blue"
    
    def in_progress_msg(self):
        return f"Patching data"

class Delete(RequestMethod):
    name = "DELETE"
    color = "red"
    
    def in_progress_msg(self):
        return f"Deleting data"


METHODS = {str(m).lower(): m for m in [Get(), Post(), Put(), Patch(), Delete()]}

