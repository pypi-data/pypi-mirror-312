from reqcurl.wrapper import reqcurl

def test_execute_get_request(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}

    mocker.patch("requests.request", return_value=mock_response)

    curl_command = "curl https://api.example.com"
    reqcurl_instance = reqcurl()
    response = reqcurl_instance.execute(curl_command)

    assert response.status_code == 200
    assert response.json() == {"success": True}
