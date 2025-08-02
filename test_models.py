from models import Endpoint, Loader


def test_endpoint_add_request():
    ep = Endpoint('2023-01-01', '200', '/test', 'GET', 0.5, 'agent')
    ep.add_request(1.0)
    assert ep.total == 2
    assert abs(ep.get_average()[2] - 0.75) < 1e-6


def test_endpoint_get_average():
    ep = Endpoint('2023-01-01', '200', '/test', 'GET', 0.5, 'agent')
    ep.add_request(1.5)
    url, total, avg = ep.get_average()
    assert url == '/test'
    assert total == 2
    assert abs(avg - 1.0) < 1e-6


def test_pars_log():
    log_line = '{"@timestamp": "2023-01-01", "status": "200", "url": "test", "request_method": "GET", "response_time": 0.3, "http_user_agent": "..."}'
    result = Loader.pars_log(log_line[1:-1].split(','))
    assert result == ['"2023-01-01"', '"200"',
                      '"test"', '"GET"', '0.3', '"..."']


def test_load_log_creates_endpoint(tmp_path):
    log_content = [
        '{"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/home", "request_method": "GET", "response_time": 0.024, "http_user_agent": "..."}\n',
        '{"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/about", "request_method": "GET", "response_time": 0.024, "http_user_agent": "..."}\n'
    ]
    file_path = tmp_path / "log.txt"
    file_path.write_text(''.join(log_content))

    loader = Loader()
    loader.load_log([str(file_path)])

    assert '"/home"' in loader.dict_endpoint.keys()
    assert '"/about"' in loader.dict_endpoint.keys()
    assert loader.dict_endpoint['"/home"'].total == 1
    assert loader.dict_endpoint['"/about"'].total == 1
