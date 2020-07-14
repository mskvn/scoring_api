# Scoring API

API for calculating users interests and scores

## Requirements

* python 3.6

## Usage

### Score

Request

```shell script
curl --location --request POST 'http://127.0.0.1:8080/method/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "account": "horns&hoofs",
  "login": "admin",
  "method": "online_score",
  "arguments": {
    "phone": "79990000000",
    "email": "user@domain"
  },
  "token": "a1469c2ae1080ad8dea6d0943345cba6a50077e6aba6963c3e080593603bafbdd1efcbf86032d55540ced68a6257c099dea3289761ca3cf4b4d4ea8ceb0aaec1"
}'
```

Response

```json
{
    "response": {
        "score": 42
    },
    "code": 200
}
```

### Interests

Request

```shell script
curl --location --request POST 'http://127.0.0.1:8080/method/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "account": "horns&hoofs",
  "login": "h&f",
  "method": "clients_interests",
  "arguments": {
    "client_ids": [
      1,
      2,
      3
    ],
    "date": "04.07.2020"
  },
  "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95"
}'
```


Response

```json
{
    "response": {
        "1": [
            "geek",
            "cars"
        ],
        "2": [
            "books",
            "cinema"
        ],
        "3": [
            "music",
            "sport"
        ]
    },
    "code": 200
}
```

