from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Client(_message.Message):
    __slots__ = ("username", "ip", "port")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    username: str
    ip: str
    port: int
    def __init__(self, username: _Optional[str] = ..., ip: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class ConnectionRequest(_message.Message):
    __slots__ = ("username", "others_username")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    OTHERS_USERNAME_FIELD_NUMBER: _ClassVar[int]
    username: str
    others_username: str
    def __init__(self, username: _Optional[str] = ..., others_username: _Optional[str] = ...) -> None: ...

class Boolean(_message.Message):
    __slots__ = ("done", "response")
    DONE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    done: bool
    response: str
    def __init__(self, done: bool = ..., response: _Optional[str] = ...) -> None: ...

class AnswerRequest(_message.Message):
    __slots__ = ("username", "others_username", "bool")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    OTHERS_USERNAME_FIELD_NUMBER: _ClassVar[int]
    BOOL_FIELD_NUMBER: _ClassVar[int]
    username: str
    others_username: str
    bool: bool
    def __init__(self, username: _Optional[str] = ..., others_username: _Optional[str] = ..., bool: bool = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("username", "body")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    username: str
    body: str
    def __init__(self, username: _Optional[str] = ..., body: _Optional[str] = ...) -> None: ...

class SendMessage(_message.Message):
    __slots__ = ("chat_id", "username", "body")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    username: str
    body: str
    def __init__(self, chat_id: _Optional[str] = ..., username: _Optional[str] = ..., body: _Optional[str] = ...) -> None: ...

class ReceiveMessage(_message.Message):
    __slots__ = ("chat_id", "username")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    username: str
    def __init__(self, chat_id: _Optional[str] = ..., username: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
