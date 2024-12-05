from functools import wraps
from fastapi import APIRouter, HTTPException, Query
from crud.crud import GenericCRUD, T
from typing import Generic, TypeVar, Type
from sqlalchemy.engine.result import ScalarResult
import re

# Request Model Type
W = TypeVar('W')
# Response Model Type
V = TypeVar('V')


def validate(*args, **kwargs):
    validation_func = kwargs.pop("func")
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            await validation_func(*args, **kwargs)
            return await func(self, *args, **kwargs)
        return wrapper
    return decorator


class GenericRouter(APIRouter, Generic[W, V]):
    def __init__(self, crud: GenericCRUD[T], request_model: Type[W], response_model: Type[V], C = True, R = True, U = True, D = True):
        super().__init__()
        self.crud = crud
        self.response_model = response_model

        model_name = self.response_model.__name__.split("DB")[0]
        self.prefix = f"/{model_name.lower()}s"
        self.tags = [model_name]

        # Wrapper functions for the CRUD operations that require the request model (at runtime)
        async def post(payload: request_model):
            return await self.post(payload)
        async def put(id: int, payload: request_model):
            return await self.put(id, payload)
        # Generate query description from fields of request model
        query_description = ", ".join([f"{field}: {type.__name__}" for field, type in request_model.__annotations__.items()])
        async def get_all(filter: list[str] = Query([], description = "Filter options: " + query_description + "\n\nExample form: ?filters=name=*TestName*,address=*TestAddress*")):
            return await self.get_all(filter)

        # Add routes to the router (same effect as @app.post, @app.get, etc.)
        if C:
            self.add_api_route("/", post, methods=["POST"], status_code=201, response_model=response_model)
        if R:
            self.add_api_route("/", get_all, methods=["GET"], status_code=200, response_model=list[response_model])
            self.add_api_route("/{id}/", self.get, methods=["GET"], status_code=200, response_model=response_model)
        if U:
            self.add_api_route("/{id}/", put, methods=["PUT"], status_code=200, response_model=response_model)
        if D:
            self.add_api_route("/{id}/", self.delete, methods=["DELETE"], status_code=200)

    async def post(self, payload): # type: ignore
        obj_id = await self.crud.post(payload)

        # Create the response object using the response model,passed into the constructor
        response_obj = self.response_model(id=obj_id, **vars(payload)) # type: ignore

        return response_obj

    async def get_all(self, filters: list[str]=[]):
        # Fetch all objects using the crud
        objs = await self.crud.get_all()

        return self.filter_objs(objs, filters) # type: ignore

    async def get(self, id: int): # type: ignore
        obj = await self.crud.get(id)

        if not obj:
            raise HTTPException(status_code=404, detail="Not found")

        return obj

    async def put(self, id: int, payload): # type: ignore
        obj = await self.crud.put(id, payload)

        if not obj:
            raise HTTPException(status_code=404, detail="Not found")

        return obj

    async def delete(self, id: int): # type: ignore
        deleted_id = await self.crud.delete(id)

        if deleted_id == 0 or not deleted_id:
            raise HTTPException(status_code=404, detail="Not found")

        return { "detail": "Deleted" }

    def filter_objs(self, objs: list[object], filters: list[str]=[]):
        # Remove empty strings from filters
        try:
            filters.remove("")
        except ValueError:
            pass
        # Loop through all filters
        for filter in filters:
            # Check if filter is in the form of key=value using regex
            if not re.match(r"^\w+=\w+$", filter):
                raise HTTPException(status_code=400, detail="Invalid filter: " + filter)

            filter_key = filter.split("=")[0]
            filter_value = filter.split("=")[1]

            # Check if filter key exists in as an attribute of the crud-model
            try:
                vars(self.crud.model)[filter_key]
            except KeyError:
                raise HTTPException(status_code=400, detail="Invalid filter key: " + filter_key)

            # Apply filter
            objs = [obj for obj in objs if vars(obj)[filter_key] == filter_value]

        return objs