"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
from builtins import (
    bool,
    int,
)

from google.protobuf.descriptor import (
    Descriptor,
    FileDescriptor,
)

from google.protobuf.message import (
    Message,
)

from typing import (
    Text,
)

from typing_extensions import (
    Literal,
)


DESCRIPTOR: FileDescriptor = ...

class GetHistoryL2TicksReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOLS_FIELD_NUMBER: int
    START_TIME_FIELD_NUMBER: int
    END_TIME_FIELD_NUMBER: int
    FIELDS_FIELD_NUMBER: int
    SKIP_SUSPENDED_FIELD_NUMBER: int
    FILL_MISSING_FIELD_NUMBER: int
    ADJUST_FIELD_NUMBER: int
    ADJUST_END_TIME_FIELD_NUMBER: int
    symbols: Text = ...
    start_time: Text = ...
    end_time: Text = ...
    fields: Text = ...
    skip_suspended: bool = ...
    fill_missing: Text = ...
    adjust: int = ...
    adjust_end_time: Text = ...
    def __init__(self,
        *,
        symbols : Text = ...,
        start_time : Text = ...,
        end_time : Text = ...,
        fields : Text = ...,
        skip_suspended : bool = ...,
        fill_missing : Text = ...,
        adjust : int = ...,
        adjust_end_time : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"adjust",b"adjust",u"adjust_end_time",b"adjust_end_time",u"end_time",b"end_time",u"fields",b"fields",u"fill_missing",b"fill_missing",u"skip_suspended",b"skip_suspended",u"start_time",b"start_time",u"symbols",b"symbols"]) -> None: ...

class GetHistoryL2BarsReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOLS_FIELD_NUMBER: int
    FREQUENCY_FIELD_NUMBER: int
    START_TIME_FIELD_NUMBER: int
    END_TIME_FIELD_NUMBER: int
    FIELDS_FIELD_NUMBER: int
    SKIP_SUSPENDED_FIELD_NUMBER: int
    FILL_MISSING_FIELD_NUMBER: int
    ADJUST_FIELD_NUMBER: int
    ADJUST_END_TIME_FIELD_NUMBER: int
    symbols: Text = ...
    frequency: Text = ...
    start_time: Text = ...
    end_time: Text = ...
    fields: Text = ...
    skip_suspended: bool = ...
    fill_missing: Text = ...
    adjust: int = ...
    adjust_end_time: Text = ...
    def __init__(self,
        *,
        symbols : Text = ...,
        frequency : Text = ...,
        start_time : Text = ...,
        end_time : Text = ...,
        fields : Text = ...,
        skip_suspended : bool = ...,
        fill_missing : Text = ...,
        adjust : int = ...,
        adjust_end_time : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"adjust",b"adjust",u"adjust_end_time",b"adjust_end_time",u"end_time",b"end_time",u"fields",b"fields",u"fill_missing",b"fill_missing",u"frequency",b"frequency",u"skip_suspended",b"skip_suspended",u"start_time",b"start_time",u"symbols",b"symbols"]) -> None: ...

class GetHistoryL2OrdersReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOLS_FIELD_NUMBER: int
    START_TIME_FIELD_NUMBER: int
    END_TIME_FIELD_NUMBER: int
    FIELDS_FIELD_NUMBER: int
    symbols: Text = ...
    start_time: Text = ...
    end_time: Text = ...
    fields: Text = ...
    def __init__(self,
        *,
        symbols : Text = ...,
        start_time : Text = ...,
        end_time : Text = ...,
        fields : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"end_time",b"end_time",u"fields",b"fields",u"start_time",b"start_time",u"symbols",b"symbols"]) -> None: ...

class GetHistoryL2OrderQueuesReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOLS_FIELD_NUMBER: int
    START_TIME_FIELD_NUMBER: int
    END_TIME_FIELD_NUMBER: int
    FIELDS_FIELD_NUMBER: int
    symbols: Text = ...
    start_time: Text = ...
    end_time: Text = ...
    fields: Text = ...
    def __init__(self,
        *,
        symbols : Text = ...,
        start_time : Text = ...,
        end_time : Text = ...,
        fields : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"end_time",b"end_time",u"fields",b"fields",u"start_time",b"start_time",u"symbols",b"symbols"]) -> None: ...

class GetHistoryL2TransactionsReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOLS_FIELD_NUMBER: int
    START_TIME_FIELD_NUMBER: int
    END_TIME_FIELD_NUMBER: int
    FIELDS_FIELD_NUMBER: int
    symbols: Text = ...
    start_time: Text = ...
    end_time: Text = ...
    fields: Text = ...
    def __init__(self,
        *,
        symbols : Text = ...,
        start_time : Text = ...,
        end_time : Text = ...,
        fields : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"end_time",b"end_time",u"fields",b"fields",u"start_time",b"start_time",u"symbols",b"symbols"]) -> None: ...
