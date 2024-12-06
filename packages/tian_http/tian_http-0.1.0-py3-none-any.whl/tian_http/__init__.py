from tian_glog import logger
from flask import Flask, request, redirect, jsonify, render_template, url_for, Blueprint
from werkzeug.utils import import_string
from werkzeug.exceptions import HTTPException
from flask_restx import Api, Resource, fields

from http import HTTPStatus
from .config import Config, config_dict
import os
from importlib import import_module
from tian_glog import logger
import urllib
import traceback
# from .casbin import *

# Define a list of whitelisted paths
whitelist_paths = [
    '/account/login',
    '/account/register',
    '/account/welcome',
    '/account/logout',
    '/static/',
    '/public/'
]
class BaseService:
    def __init__(self, config: Config = None):
        if config is None:
            DEBUG = (os.getenv('DEBUG', 'False') == 'True')
            get_config_mode = 'Debug' if DEBUG else 'Production'
            config = config_dict[get_config_mode]
        _app = Flask(__name__)
        _app.config.from_object(config)
        # Add a route to serve the swagger ui

        self._app = _app
        self._app.static_folder = _app.config.get('ASSETS_ROOT', 'static')
        self._app.template_folder = _app.config.get('TEMPLATES_FOLDER', 'templates')
        self._app.static_url_path = _app.config.get('STATIC_FOLDER', '/static')

        # self._app.register_error_handler(HTTPException, self.handle_http_exception)
        self._app.errorhandler(400)(self.handle_400_error)
        self._app.errorhandler(404)(self.handle_404_error)
        self._app.errorhandler(500)(self.handle_500_error)

        #
        # self._register_casbin()
        self._app.before_request(self._log_request)
        self._app.before_request(self._remove_trailing_slash)

        self._is_documentation()

    def _remove_trailing_slash(self):
        # Get the request path
        path = request.path
        
        # Only remove trailing slashes for API routes
        if path.startswith('/api/') and path != '/' and path.endswith('/'):
            return redirect(path[:-1])

    def register(self, new_blueprint):
        self._app.register_blueprint(new_blueprint)

    def _log_request(self):
        logger.warning(f"Request: {request}")

    def _is_documentation(self): #TODO
        # if os.getenv('ENVIRONMENT', 'production') == 'development':
        #     return True
        
        authorizations = {
            "Authorization": {
                "description": "Please enter your token in the format 'Bearer [token]'",
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
            }
        }

        api_name = "api"
        pre_path = "/api/v1"


        blueprint = Blueprint(api_name, __name__, url_prefix=pre_path)
        self.api = Api(
            blueprint,
            doc="/docs",
            title=("Tài liệu kĩ thuật API",),
            version="0.1",
            description="Tài liệu kĩ thuật API cho dự án ",
            license_url="thienhang.com",
            authorizations=authorizations,
            security="Authorization",
        )
        self.register(blueprint)

    def load(self, module_dir: str):
        module_path = os.path.join(os.getcwd(), module_dir)
        modules = os.listdir(module_path)
        logger.debug("Loading modules from %s" % module_path)

        for module_name in modules:
            try:
                if module_name == "__pycache__":
                    continue
                if module_name == "middleware.py":
                    continue
                logger.debug("Loading module %s %s" % (module_dir, module_name))
                module = import_module('{}.{}.routes'.format(module_dir.replace(os.sep, '.'), module_name))
                #
                # Check if the module has a blueprint and api attributes
                logger.debug("Checking module %s" % module_name)

                if module_dir.endswith("api"):
                    # Check if the module has an attribute named `tian_api` for namespaces
                    if hasattr(module, 'tian_api'):
                        self.api.add_namespace(module.tian_api)
                        logger.debug("API namespace %s loaded" % module_name)
                    else:
                        logger.error(f"No 'tian_api' namespace found in module {module_name}")
                else:
                    # Check if the module has an attribute named `blueprint` for UI blueprints
                    if hasattr(module, 'blueprint'):
                        self.register(module.blueprint)
                        logger.debug("UI blueprint %s loaded" % module_name)
                    else:
                        logger.error(f"No 'blueprint' found in module {module_name}")
            except Exception as e:
                logger.error(f"Error occurred when init root {str(module_name)} : {str(e)}")
                traceback.print_exc()

    def get_resources(self) -> list:

        output = []
        for rule in self._app.url_map.iter_rules():
            if rule.endpoint in {'restx_doc.static', 'api.doc', 'api.specs'}:
                continue
            methods = ','.join(rule.methods)
            line = urllib.parse.unquote(f"{rule.endpoint:50s} {methods:20s} {str(rule)}")

            r = str(rule).rstrip('/')
            r = r.replace('/', '.')
            r = r.replace('-', '_')

            if any(r.endswith(suffix) for suffix in ['<uuid>', '<path:path>', '<string:resource_id>', '<path:filename>', '.<string:username>']):
                continue

            output.append(r)
        return sorted(output)

    def handle_400_error(self, error):
        logger.error(f"Bad request error: {error}")
        return render_template("pages/400.html"), 400

    def handle_404_error(self, error):
        logger.error(f"Not found error: {error}")
        return render_template("pages/401.html"), 404

    def handle_500_error(self, error):
        return render_template("pages/500.html"), 500

    def handle_http_exception(self, error):
        # Log the error
        logger.error(f"HTTP Exception occurred: {error}")

        # Default response
        error_response = {
            "error": "An unexpected error occurred"
        }

        # Handle specific HTTP exceptions
        if isinstance(error, HTTPException):
            error_response['error'] = error.description
            return jsonify(error_response), error.code

        # Handle other exceptions
        return render_template("pages/500.html",), 500
    # def has_no_empty_params(self, rule):
    #     defaults = rule.defaults if rule.defaults is not None else ()
    #     arguments = rule.arguments if rule.arguments is not None else ()
    #     return len(defaults) >= len(arguments)
    
    # def site_map(self) -> list:
    #     links = []
    #     for rule in self.app.url_map.iter_rules():
    #         # Filter out rules we can't navigate to in a browser
    #         # and rules that require parameters
    #         if "GET" in rule.methods and self.has_no_empty_params(rule):
    #             url = url_for(rule.endpoint, **(rule.defaults or {}))
    #             links.append((url, rule.endpoint))
    #     return links
    
    def run(self):
        self._app.run(os.environ.get('HOST', '0.0.0.0'), os.environ.get('PORT', 80))
