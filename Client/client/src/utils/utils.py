from . import *

# function to create a json response for the endpoint
def create_aliased_response(model: BaseModel, status_code=200) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(model, by_alias=True), status_code=status_code)

# function to check if a directory exists (used in logs)
def check_dir(path_dir) -> bool:
    if not os.path.isdir(path_dir):
        try:
            os.makedirs(path_dir)
        except FileExistsError:
            return False
        else:
            return True
