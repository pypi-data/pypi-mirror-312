import re
from typing import List

import starlette.routing
from starlette.applications import Starlette
from swagger_ui import api_doc
from openapi_pydantic import (
    OpenAPI,
    Info,
    PathItem,
    Operation,
    Response,
)
from openapi_pydantic.util import (
    PydanticSchema,
    construct_open_api_with_schema_class,
)


class Route(starlette.routing.Route):

    def __init__(self, *args, **kwargs):
        if "include_in_schema" in kwargs:
            raise ValueError("include_in_schema is not allowed")
        self.tag = None
        self.request_model = kwargs.pop("request_model", None)
        self.response_ok_model = kwargs.pop("response_ok", None)
        self.response_fail_model = kwargs.pop("response_failed", None)
        super().__init__(*args, **kwargs)

    @classmethod
    def get(cls, path, endpoint, /, **kwargs):
        return cls(path=path, endpoint=endpoint, methods=["GET"], **kwargs)

    @classmethod
    def post(cls, path, endpoint, /, **kwargs):
        return cls(path=path, endpoint=endpoint, methods=["POST"], **kwargs)


class OpenAPIDoc(object):

    def __init__(self, routes: List[Route] = None):
        self.routes: List[Route] = routes or []

    def add_route(self, route: Route):
        self.routes.append(route)

    def to_openapi(self) -> OpenAPI:
        paths = {}
        for route in self.routes:
            path = route.path
            method = list(route.methods)[0].lower()
            request_body = None
            if route.request_model:
                request_body = {
                    "content": {
                        "application/json": {
                            "schema":
                            PydanticSchema(schema_class=route.request_model)
                        }
                    }
                }
            operation = Operation(
                tags=[route.tag],
                requestBody=request_body,
                responses={
                    "200":
                    Response(description="Success",
                             content={
                                 "application/json": {
                                     "schema":
                                     PydanticSchema(
                                         schema_class=route.response_ok_model)
                                 }
                             })
                })
            paths[path] = PathItem(**{method: operation})
        return OpenAPI(
            info=Info(title="My API", version="v0.1.0"),
            paths=paths,
        )


def urljoin(path1, path2):
    path = path1 + "/" + path2
    return re.sub(r'/+', '/', path)


class RouteGroup(object):

    def __init__(self, path: str, routes: List[Route] = None):
        if not path.startswith("/"):
            raise ValueError("path should start with `/`")
        if path.count("/") > 1:
            raise ValueError("path should not contain more than one `/`")
        self.tag = path[1:] if path != "/" else "default"
        self.path = path
        for route in routes or []:
            route.tag = self.tag
            route.path = urljoin(self.path, route.path)
        self.routes = routes or []

    def add_router(self, router: "RouteGroup"):
        if not isinstance(router, RouteGroup):
            raise TypeError(
                f"`router` should be type of RouteGroup, but got `{type(router)}` type"
            )
        for route in router.routes:
            route.path = urljoin(self.path, route.path)
        self.routes.extend(router.routes)

    def get(self, path, endpoint, /, **kwargs):
        route = Route(path=urljoin(self.path, path),
                      endpoint=endpoint,
                      methods=["GET"],
                      **kwargs)
        route.tag = self.tag
        self.routes.append(route)

    def post(self, path, endpoint, /, **kwargs):
        route = Route(path=urljoin(self.path, path),
                      endpoint=endpoint,
                      methods=["POST"],
                      **kwargs)
        route.tag = self.tag
        self.routes.append(route)


class Qyin(Starlette):

    def __init__(self, title: str, *args, **kwargs):
        self.title = title
        self.root_router = None
        super().__init__(*args, **kwargs)

    def set_root_router(self, router: RouteGroup):
        self.root_router = router
        doc = OpenAPIDoc(routes=router.routes)
        open_api = construct_open_api_with_schema_class(doc.to_openapi())
        self.root_router.get("/openapi.json", lambda: open_api)
        api_doc(self,
                config=open_api.model_dump(by_alias=True,
                                           exclude_none=True),
                url_prefix="/api/doc",
                title="API Doc")
