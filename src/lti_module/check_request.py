from lti.tool_provider import ToolProvider
from .lti_validator import LTIRequestValidator
from .utils import check_content


def check_request(request_info):
    # request_info must contains keys: ('headers', 'data', 'url', 'secret')
    check_content(request_info)
    
    provider = ToolProvider.from_unpacked_request(
        secret=request_info.get('secret', None),
        params=request_info.get('data', {}),
        headers=request_info.get('headers', {}),
        url=request_info.get('url', '')
    )
    return provider.is_valid_request(LTIRequestValidator())