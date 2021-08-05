from ...exceptions import InitError
from ..base import Extension
from .cors import add_cors
from .methods import add_auto_handlers, add_http_methods


class HTTPExtension(Extension):
    name = "http"

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.all_http_methods: bool = self.options["all_http_methods"]
        self.auto_head: bool = self.options["auto_head"]
        self.auto_options: bool = self.options["auto_options"]
        self.auto_trace: bool = self.options["auto_trace"]
        self.cors: bool = self.options["cors"]

    def startup(self, _) -> None:
        if self.all_http_methods:
            add_http_methods(self.app, ["CONNECT", "TRACE"])

        if self.auto_head or self.auto_options or self.auto_trace:
            add_auto_handlers(
                self.app, self.auto_head, self.auto_options, self.auto_trace
            )

        if self.cors:
            add_cors(self.app)

        if self.app.ctx.cors.automatic_options and not self.auto_options:
            raise InitError(
                "Configuration mismatch. If CORS_AUTOMATIC_OPTIONS is set to "
                "True, then you must run SanicExt with "
                "apply(..., auto_options=True)."
            )