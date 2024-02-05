"""Test central zoning mode"""
import json
import asyncio
from unittest.mock import patch
from lennoxs30api.s30api_async import lennox_system
from lennoxs30api.s30exception import EC_BAD_PARAMETERS, S30Exception

def test_set_central_mode_multizone(api):
    """Tests setting central mode on and off"""
    lsystem: lennox_system = api.system_list[0]
    assert lsystem.sysId == "0000000-0000-0000-0000-000000000001"
    assert lsystem.numberOfZones > 1
    with patch.object(api, "publishMessageHelper") as mock_message_helper:
        loop = asyncio.get_event_loop()
        _ = loop.run_until_complete(lsystem.centralMode_on())
        assert mock_message_helper.call_count == 1
        arg0 = mock_message_helper.await_args[0][0]
        assert arg0 == lsystem.sysId
        arg1 = mock_message_helper.await_args[0][1]
        jsbody = json.loads("{" + arg1 + "}")

        config = jsbody["Data"]["system"]["config"]
        assert config["centralMode"] is True

    with patch.object(api, "publishMessageHelper") as mock_message_helper:
        loop = asyncio.get_event_loop()
        _ = loop.run_until_complete(lsystem.centralMode_off())
        assert mock_message_helper.call_count == 1
        arg0 = mock_message_helper.await_args[0][0]
        assert arg0 == lsystem.sysId
        arg1 = mock_message_helper.await_args[0][1]
        jsbody = json.loads("{" + arg1 + "}")

        config = jsbody["Data"]["system"]["config"]
        assert config["centralMode"] is False


def test_set_central_mode_singlezone(api):
    """Test setting central mode on an unzoned system which should fail"""
    lsystem: lennox_system = api.system_list[1]
    assert lsystem.sysId == "0000000-0000-0000-0000-000000000002"
    assert lsystem.numberOfZones == 1
    with patch.object(api, "publishMessageHelper") as mock_message_helper:
        loop = asyncio.get_event_loop()
        ex = None
        try:
            _ = loop.run_until_complete(lsystem.centralMode_on())
        except S30Exception as e:
            ex = e
        assert ex is not None
        assert ex.error_code == EC_BAD_PARAMETERS
        assert mock_message_helper.call_count == 0

    with patch.object(api, "publishMessageHelper") as mock_message_helper:
        loop = asyncio.get_event_loop()
        ex = None
        try:
            _ = loop.run_until_complete(lsystem.centralMode_off())
        except S30Exception as e:
            ex = e
        assert ex is not None
        assert ex.error_code == EC_BAD_PARAMETERS
        assert mock_message_helper.call_count == 0
