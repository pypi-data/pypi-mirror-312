
from flask_restx.reqparse import RequestParser

parser = RequestParser(bundle_errors=True)
parser.add_argument('page', type=int, default=1, help='Page number')
parser.add_argument('limit', type=int, default=10, help='Number of items per page')
parser.add_argument('sort', type=str, default='desc', help='Sorting order')
parser.add_argument('filter', type=str, default='', help='Filter criteria')
parser.add_argument('mode', type=str, default='default', help='Mode of operation')
parser.add_argument('group_by', type=str, default='', help='Field to group by')

