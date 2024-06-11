from datetime import datetime

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

current_currency = [
    OpenApiParameter(
        'date',
        type=OpenApiTypes.STR,
        required=True,
        description='Date.',
        examples=[OpenApiExample('Example 1', value=datetime.now().strftime('%Y-%m-%d'))],
    ),
    OpenApiParameter(
        'currency_code',
        type=OpenApiTypes.STR,
        required=True,
        description='Currency code',
    ),
]

current_date = [
    OpenApiParameter(
        'date',
        type=OpenApiTypes.STR,
        required=True,
        description='Date.',
        examples=[OpenApiExample('Example 1', value=datetime.now().strftime('%Y-%m-%d'))],
    ),
]
