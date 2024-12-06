import json
from aiwolf_nlp_common.protocol import Packet
from aiwolf_nlp_json_converter.gameInfo import gameInfoConverter

def test_get_game_info_dict(initialize_str, initialize_json) -> None:
    protocol = Packet(value=json.loads(initialize_str))
    test_result = gameInfoConverter.get_game_info_dict(protocol=protocol)

    assert type(test_result) is not None
    assert type(test_result) is dict
    assert test_result["day"] == initialize_json["info"]["day"]
    assert test_result["agent"] == initialize_json["info"]["agent"]
    assert test_result["attackVoteList"] == []
    assert test_result["statusMap"] == initialize_json["info"]["statusMap"]
    assert test_result["roleMap"] == initialize_json["info"]["roleMap"]