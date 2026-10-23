"""数勋科技开放平台 Python SDK。

.. code-block:: python

    from shuxuntech import ShuxunClient

    client = ShuxunClient("your-app-key", "your-app-secret")
    response = client.apis.identity.id_card_check("张三", "110101199001011234")
    if response.is_success:
        print(response.data.result_desc)
"""

from ._version import __version__
from .apis import ShuxunApis
from .auth import now_millis, sha256_hex, sign
from .client import DEFAULT_BASE_URL, ShuxunClient
from .exceptions import ShuxunApiError, ShuxunError, ShuxunTransportError
from .params import Params, ParamsLike
from .response import ApiResponse
from .response_codes import ResponseCode, ResponseCodes, describe_response_code

__all__ = [
    "DEFAULT_BASE_URL",
    "ApiResponse",
    "Params",
    "ParamsLike",
    "ResponseCode",
    "ResponseCodes",
    "ShuxunApiError",
    "ShuxunApis",
    "ShuxunClient",
    "ShuxunError",
    "ShuxunTransportError",
    "__version__",
    "describe_response_code",
    "now_millis",
    "sha256_hex",
    "sign",
]
