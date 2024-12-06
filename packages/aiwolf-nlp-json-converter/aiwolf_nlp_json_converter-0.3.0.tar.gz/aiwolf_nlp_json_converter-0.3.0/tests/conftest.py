import pytest
import json

@pytest.fixture
def initialize_str() -> str:
    return """{"request":"INITIALIZE","info":{"day":0,"agent":"Agent[05]","statusMap":{"Agent[01]":"ALIVE","Agent[02]":"ALIVE","Agent[03]":"ALIVE","Agent[04]":"ALIVE","Agent[05]":"ALIVE"},"roleMap":{"Agent[05]":"VILLAGER"}},"setting":{"playerNum":5,"maxTalk":5,"maxTalkTurn":20,"maxWhisper":5,"maxWhisperTurn":20,"maxSkip":0,"isEnableNoAttack":false,"isVoteVisible":false,"isTalkOnFirstDay":true,"responseTimeout":120000,"actionTimeout":60000,"maxRevote":1,"maxAttackRevote":1,"roleNumMap":{"BODYGUARD":0,"MEDIUM":0,"POSSESSED":1,"SEER":1,"VILLAGER":2,"WEREWOLF":1}}}"""

@pytest.fixture
def initialize_json(initialize_str) -> dict:
    return json.loads(initialize_str)