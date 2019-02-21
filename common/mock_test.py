from unittest import mock
import json


def mock_test(method, request_data, response_data):
    request_data = json.dumps(request_data)
    method = mock.Mock(return_value=response_data)
    res = method(request_data)
    return res
