from functools import wraps

from tian_glog import logger
from flask import redirect, request, jsonify, url_for, make_response

# Only get pgae, limit, offest, sort, filter from params
def metadata(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            page = request.args.get('page', type=int)
            limit = request.args.get('limit', type=int)
            offset = request.args.get('offset', type=int)
            sort = request.args.get('sort', type=str)
            filter = request.args.get('filter', type=str)

            # Fallback to sessionStorage (for cookies) or defaults if parameters are missing
            if page is None:
                page = request.cookies.get('page', 1, type=int)
            if limit is None:
                limit = request.cookies.get('limit', 10, type=int)
            if offset is None:
                offset = request.cookies.get('offset', 0, type=int)
            if sort is None:
                sort = request.cookies.get('sort', 'desc', type=str)
            if filter is None:
                filter = request.cookies.get('filter', None, type=str)

            # Default values if not found in either request or storage
            page = page * limit
            limit = limit or 10
            offset = offset or 0
            sort = sort or 'desc'
            filter = filter or ''

            if page < 0:
                page = 0

            if limit < 0:
                limit = 10
                
            metadata = {
                "page": page,
                "limit": limit,
                "offset": offset,
                "sort": sort,
                "filter": filter
            }
            return f(*args, **kwargs, metadata=metadata)
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            return jsonify({"error": str(e)}), 500
    return decorated_function

def handle_request_params_report(args, params):
    publisher = args.get('publisher', None, type=str)
    domain = args.get('domain', None, type=str)
    start_time = args.get('start_time', None, type=str)
    end_time = args.get('end_time', None, type=str)
    if publisher is not None: 
        if domain is not None: 
            params.update({
                "publisher": publisher,
                "domain": domain
            })
        else:
            params.update({
                "publisher": publisher,
                
            })
    if start_time is not None:
        params.update({
            "start_time": start_time,
            
        })
    if end_time is not None:
        params.update({
            "end_time": end_time,
            
        })

# def process_request_params(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         # Get parameters from the request
#         page = request.args.get('page', None, type=int)
#         limit = request.args.get('limit', None, type=int)
#         sort = request.args.get('sort', None, type=str)
#         filter = request.args.get('filter', None, type=str)
#         mode = request.args.get('mode', None, type=str)
       
#         # Default values
#         default_params = {
#             "page": int(request.cookies.get("page", 1)),
#             "limit": int(request.cookies.get("limit", 10)),
#             "sort": request.cookies.get("sort", "desc"),
#             "filter": request.cookies.get("filter", ""),
#             "mode": request.cookies.get("mode", "default"),
#         }

#         # Resolve parameters
#         resolved_params = {
#             "page": page if page is not None else default_params["page"],
#             "limit": limit if limit is not None else default_params["limit"],
#             "sort": sort if sort is not None else default_params["sort"],
#             "filter": filter if filter is not None else default_params["filter"],
#             "mode": mode if mode is not None else default_params["mode"],
#         }

#         # Check if a redirection is needed
#         if any(param is None for param in [page, limit, sort, filter, mode]):
#             # Update cookies and redirect
#             response = make_response(redirect(url_for(request.endpoint, **resolved_params)))
#             response.set_cookie("page", str(resolved_params["page"]))
#             response.set_cookie("limit", str(resolved_params["limit"]))
#             response.set_cookie("sort", resolved_params["sort"])
#             response.set_cookie("filter", resolved_params["filter"])
#             response.set_cookie("mode", resolved_params["mode"])
#             return response

#         # Call the wrapped function with the metadata
#         metadata = {
#             **resolved_params,
#             "current_url": url_for(request.endpoint, **resolved_params),
#         }
#         return func(*args, **kwargs, metadata=metadata)

#     return wrapper



'''
def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True
    return False
    '''
