# aiwolf-nlp-json-converter
人狼知能コンテスト自然言語処理部門は**2024冬季 国内大会**からゲームサーバの変更を行いました。 \
これに伴い、情報伝達を行う際に[旧サーバプログラム](https://github.com/aiwolfdial/AIWolfNLPServer)とは異なるJsonが使用されるようになりました。\
このプログラムは[新規サーバプログラム](https://github.com/kano-lab/aiwolf-nlp-server)から伝達される情報を[旧サーバプログラム](https://github.com/aiwolfdial/AIWolfNLPServer)から伝達される情報に変換するプログラムです。

## 対象者
人狼知能コンテスト2024冬季**以前**に人狼知能コンテスト(自然言語処理部門)の大会に参加された方で、過去のプログラムを流用したい方。

> [!WARNING]
> このプログラムは2024冬季大会の開催告知から開催までの期間が短いため作成しました。 \
> 今後のアップデートや2025年春大会以降の13人人狼に必要な情報に対応しない可能性があります。

## インストール方法
以下のコマンドでインストールできます。
```
pip install aiwolf-nlp-json-converter
```

> [!WARNING]
> `aiwolf-nlp-json-converter==0.2.0`, `aiwolf-nlp-common==0.3.5`であることを確認してください。

## 使い方
ゲームサーバから受け取った文字列の情報をそのまま`AIWolfNLPJsonConverter`に渡すことで、旧ゲームサーバから伝達される情報に変換します。
```python
from aiwolf_nlp_json_converter import AIWolfNLPJsonConverter

recv:str = """{"request":"INITIALIZE","info":{"day":0,"agent":"Agent[05]","statusMap":{"Agent[01]":"ALIVE","Agent[02]":"ALIVE","Agent[03]":"ALIVE","Agent[04]":"ALIVE","Agent[05]":"ALIVE"},"roleMap":{"Agent[05]":"VILLAGER"}},"setting":{"playerNum":5,"maxTalk":5,"maxTalkTurn":20,"maxWhisper":5,"maxWhisperTurn":20,"maxSkip":0,"isEnableNoAttack":false,"isVoteVisible":false,"isTalkOnFirstDay":true,"responseTimeout":120000,"actionTimeout":60000,"maxRevote":1,"maxAttackRevote":1,"roleNumMap":{"BODYGUARD":0,"MEDIUM":0,"POSSESSED":1,"SEER":1,"VILLAGER":2,"WEREWOLF":1}}}"""
json_data = AIWolfNLPJsonConverter.get_json_dict(received_str=recv)

print(type(json_data))
print(json_data)
```

### 結果
```
<class 'dict'>
{'request': 'INITIALIZE', 'gameInfo': {'agent': 'Agent[05]', 'attackVoteList': [], 'attackedAgent': None, 'day': 0, 'divineResult': None, 'executedAgent': None, 'lastDeadAgentList': [], 'roleMap': {'Agent[05]': 'VILLAGER'}, 'statusMap': {'Agent[02]': 'ALIVE', 'Agent[04]': 'ALIVE', 'Agent[01]': 'ALIVE', 'Agent[03]': 'ALIVE', 'Agent[05]': 'ALIVE'}, 'voteList': []}, 'gameSetting': {'enableNoAttack': False, 'enableNoExecution': False, 'maxAttackRevote': 1, 'maxRevote': 1, 'maxSkip': 0, 'maxTalk': 5, 'maxTalkTurn': 20, 'maxWhisper': 5, 'maxWhisperTurn': 20, 'playerNum': 5, 'roleNumMap': {'SEER': 1, 'VILLAGER': 2, 'MEDIUM': 0, 'BODYGUARD': 0, 'POSSESSED': 1, 'WEREWOLF': 1}, 'talkOnFirstDay': True, 'responseTimeout': 120, 'actionTimeout': 60, 'voteVisible': False}, 'talkHistory': [], 'whisperHistory': []}
```

## 対応していないキー
[旧ゲームサーバ](https://github.com/aiwolfdial/AIWolfNLPServer)から与えられる情報の内、本プログラムではいくつか含まれていない情報が存在します。 \
下記に詳細を記載しますので、ご確認の上ご使用ください。

### ゲームの現状態を示す情報 (gameInfo)
- `cursedFox`: 妖狐は5人、13人人狼で使用しない予定の役職なので対応していません。
- `englishTalkList`: 過去にここに割り当てられていた内容が`TalkList`と同一であったため、不要と判断し対応していません。
- `existingRoleList`: `gameSetting`の`roleNumMap`から把握できる内容であるため不要と判断し対応していません。
- `guardedAgent`: 騎士は5人人狼で使用しない予定の役職なので対応していません。
- `latestAttackVoteList`: 5人人狼において使用されない項目の上、`attackVoteList`から確認できる内容であるため不要と判断し対応していません。
- `latestExecutedAgent`: `executedAgent`の値から確認できる内容であるため不要と判断し対応していません。
- `latestVoteList`: `voteList`から確認できる内容であるため不要と判断し対応していません。
- `mediumResult`: 5人人狼において使用されない項目であるため不要と判断し対応していません。
- `remainTalkMap`: 旧サーバにおいて`INITIALIZE`,`DAILY_INITIALIZE`でのみ付与されていた情報である上、`maxTalk`から取得可能な内容であるため不要と判断し対応していません。
- `remainWhisperMap`: 5人人狼において`whisper`は行われないため不要と判断し対応していません。
- `talkList`:  旧サーバにおいて`INITIALIZE`,`DAILY_INITIALIZE`でのみ付与されていた情報である上、`talkHistory`から取得可能な内容であるため不要と判断し対応していません。
- `whisperList`: 5人人狼において使用されない項目であるため不要と判断し対応していません。

### ゲームの設定を示す情報 (gameSetting)
- `enableRoleRequest`: 新サーバにおいて削除された機能であるため対応していません。
- `validateUtterance`: 新サーバにおいて削除された機能であるため対応していません。
- `votableInFirstDay`: 大会において初日は挨拶の日であり、その人に投票は行わないため対応していません。
- `whisperBeforeRevote`: 5人人狼において使用されない項目であるため不要と判断し対応していません。

## 注意点が存在するキー
[旧ゲームサーバ](https://github.com/aiwolfdial/AIWolfNLPServer)から与えられる情報の内、本プログラムでは情報が少し変形された格納されている情報が存在します。 \
下記に詳細を記載しますので、ご確認の上ご使用ください。

### ゲームの設定を示す情報 (gameSetting)
- `responseTimeout`: ゲームサーバからは`ms`で渡されますが、本プログラムを使用した場合、`s`に変換されて返却されます。
- `actionTimeout`: ゲームサーバからは`ms`で渡されますが、本プログラムを使用した場合、`s`に変換されて返却されます。
