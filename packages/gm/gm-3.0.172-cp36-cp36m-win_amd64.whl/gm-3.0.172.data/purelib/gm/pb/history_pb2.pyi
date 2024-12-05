"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
from builtins import (
    bool,
    float,
    int,
)

from google.protobuf.descriptor import (
    Descriptor,
    FileDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer,
)

from google.protobuf.message import (
    Message,
)

from google.protobuf.timestamp_pb2 import (
    Timestamp,
)

from typing import (
    Iterable,
    Optional,
    Text,
)

from typing_extensions import (
    Literal,
)


DESCRIPTOR: FileDescriptor = ...

class GetCurrentTicksReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOLS_FIELD_NUMBER: int
    FIELDS_FIELD_NUMBER: int
    symbols: Text = ...
    fields: Text = ...
    def __init__(self,
        *,
        symbols : Text = ...,
        fields : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"fields",b"fields",u"symbols",b"symbols"]) -> None: ...

class GetHistoryTicksReq(Message):
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

class GetHistoryBarsReq(Message):
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

class GetHistoryTicksNReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    COUNT_FIELD_NUMBER: int
    END_TIME_FIELD_NUMBER: int
    FIELDS_FIELD_NUMBER: int
    SKIP_SUSPENDED_FIELD_NUMBER: int
    FILL_MISSING_FIELD_NUMBER: int
    ADJUST_FIELD_NUMBER: int
    ADJUST_END_TIME_FIELD_NUMBER: int
    FILTER_ZERO_VOLUME_FIELD_NUMBER: int
    symbol: Text = ...
    count: int = ...
    end_time: Text = ...
    fields: Text = ...
    skip_suspended: bool = ...
    fill_missing: Text = ...
    adjust: int = ...
    adjust_end_time: Text = ...
    filter_zero_volume: bool = ...
    def __init__(self,
        *,
        symbol : Text = ...,
        count : int = ...,
        end_time : Text = ...,
        fields : Text = ...,
        skip_suspended : bool = ...,
        fill_missing : Text = ...,
        adjust : int = ...,
        adjust_end_time : Text = ...,
        filter_zero_volume : bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"adjust",b"adjust",u"adjust_end_time",b"adjust_end_time",u"count",b"count",u"end_time",b"end_time",u"fields",b"fields",u"fill_missing",b"fill_missing",u"filter_zero_volume",b"filter_zero_volume",u"skip_suspended",b"skip_suspended",u"symbol",b"symbol"]) -> None: ...

class GetHistoryBarsNReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    FREQUENCY_FIELD_NUMBER: int
    COUNT_FIELD_NUMBER: int
    END_TIME_FIELD_NUMBER: int
    FIELDS_FIELD_NUMBER: int
    SKIP_SUSPENDED_FIELD_NUMBER: int
    FILL_MISSING_FIELD_NUMBER: int
    ADJUST_FIELD_NUMBER: int
    ADJUST_END_TIME_FIELD_NUMBER: int
    symbol: Text = ...
    frequency: Text = ...
    count: int = ...
    end_time: Text = ...
    fields: Text = ...
    skip_suspended: bool = ...
    fill_missing: Text = ...
    adjust: int = ...
    adjust_end_time: Text = ...
    def __init__(self,
        *,
        symbol : Text = ...,
        frequency : Text = ...,
        count : int = ...,
        end_time : Text = ...,
        fields : Text = ...,
        skip_suspended : bool = ...,
        fill_missing : Text = ...,
        adjust : int = ...,
        adjust_end_time : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"adjust",b"adjust",u"adjust_end_time",b"adjust_end_time",u"count",b"count",u"end_time",b"end_time",u"fields",b"fields",u"fill_missing",b"fill_missing",u"frequency",b"frequency",u"skip_suspended",b"skip_suspended",u"symbol",b"symbol"]) -> None: ...

class GetBenchmarkReturnReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    FREQUENCY_FIELD_NUMBER: int
    START_TIME_FIELD_NUMBER: int
    END_TIME_FIELD_NUMBER: int
    ADJUST_FIELD_NUMBER: int
    ADJUST_END_TIME_FIELD_NUMBER: int
    symbol: Text = ...
    frequency: Text = ...
    start_time: Text = ...
    end_time: Text = ...
    adjust: int = ...
    adjust_end_time: Text = ...
    def __init__(self,
        *,
        symbol : Text = ...,
        frequency : Text = ...,
        start_time : Text = ...,
        end_time : Text = ...,
        adjust : int = ...,
        adjust_end_time : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"adjust",b"adjust",u"adjust_end_time",b"adjust_end_time",u"end_time",b"end_time",u"frequency",b"frequency",u"start_time",b"start_time",u"symbol",b"symbol"]) -> None: ...

class GetBenchmarkReturnRsp(Message):
    DESCRIPTOR: Descriptor = ...
    class BenchmarkReturn(Message):
        DESCRIPTOR: Descriptor = ...
        RATIO_FIELD_NUMBER: int
        CREATED_AT_FIELD_NUMBER: int
        ratio: float = ...
        @property
        def created_at(self) -> Timestamp: ...
        def __init__(self,
            *,
            ratio : float = ...,
            created_at : Optional[Timestamp] = ...,
            ) -> None: ...
        def HasField(self, field_name: Literal[u"created_at",b"created_at"]) -> bool: ...
        def ClearField(self, field_name: Literal[u"created_at",b"created_at",u"ratio",b"ratio"]) -> None: ...

    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[GetBenchmarkReturnRsp.BenchmarkReturn]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[GetBenchmarkReturnRsp.BenchmarkReturn]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...
