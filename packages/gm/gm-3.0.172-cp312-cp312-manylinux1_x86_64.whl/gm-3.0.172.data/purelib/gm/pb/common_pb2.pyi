"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
from builtins import (
    bool,
    int,
    type,
)

from google.protobuf.descriptor import (
    Descriptor,
    EnumDescriptor,
    FileDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer,
    ScalarMap,
)

from google.protobuf.internal.enum_type_wrapper import (
    _EnumTypeWrapper,
)

from google.protobuf.message import (
    Message,
)

from google.protobuf.timestamp_pb2 import (
    Timestamp,
)

from typing import (
    Iterable,
    Mapping,
    NewType,
    Optional,
    Text,
)

from typing_extensions import (
    Literal,
)


DESCRIPTOR: FileDescriptor = ...

class Property(Message):
    DESCRIPTOR: Descriptor = ...
    KEY_FIELD_NUMBER: int
    VAL_FIELD_NUMBER: int
    NAME_FIELD_NUMBER: int
    INDEX_FIELD_NUMBER: int
    VISIBLE_FIELD_NUMBER: int
    key: Text = ...
    val: Text = ...
    name: Text = ...
    index: int = ...
    visible: bool = ...
    def __init__(self,
        *,
        key : Text = ...,
        val : Text = ...,
        name : Text = ...,
        index : int = ...,
        visible : bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"index",b"index",u"key",b"key",u"name",b"name",u"val",b"val",u"visible",b"visible"]) -> None: ...

class Filter(Message):
    DESCRIPTOR: Descriptor = ...
    FIELDS_FIELD_NUMBER: int
    FILTER_FIELD_NUMBER: int
    SORT_FIELD_NUMBER: int
    LIMIT_FIELD_NUMBER: int
    PAGE_FIELD_NUMBER: int
    PAGESIZE_FIELD_NUMBER: int
    FROMDATE_FIELD_NUMBER: int
    TODATE_FIELD_NUMBER: int
    fields: Text = ...
    filter: Text = ...
    sort: Text = ...
    limit: int = ...
    page: int = ...
    pagesize: int = ...
    fromdate: Text = ...
    todate: Text = ...
    def __init__(self,
        *,
        fields : Text = ...,
        filter : Text = ...,
        sort : Text = ...,
        limit : int = ...,
        page : int = ...,
        pagesize : int = ...,
        fromdate : Text = ...,
        todate : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"fields",b"fields",u"filter",b"filter",u"fromdate",b"fromdate",u"limit",b"limit",u"page",b"page",u"pagesize",b"pagesize",u"sort",b"sort",u"todate",b"todate"]) -> None: ...

class Error(Message):
    DESCRIPTOR: Descriptor = ...
    CODE_FIELD_NUMBER: int
    TYPE_FIELD_NUMBER: int
    INFO_FIELD_NUMBER: int
    code: int = ...
    type: Text = ...
    info: Text = ...
    def __init__(self,
        *,
        code : int = ...,
        type : Text = ...,
        info : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"code",b"code",u"info",b"info",u"type",b"type"]) -> None: ...

class ConnectionAddress(Message):
    DESCRIPTOR: Descriptor = ...
    class AddressEntry(Message):
        DESCRIPTOR: Descriptor = ...
        KEY_FIELD_NUMBER: int
        VALUE_FIELD_NUMBER: int
        key: Text = ...
        value: Text = ...
        def __init__(self,
            *,
            key : Text = ...,
            value : Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: Literal[u"key",b"key",u"value",b"value"]) -> None: ...

    TITLE_FIELD_NUMBER: int
    ADDRESS_FIELD_NUMBER: int
    SITES_FIELD_NUMBER: int
    ID_FIELD_NUMBER: int
    title: Text = ...
    @property
    def address(self) -> ScalarMap[Text, Text]: ...
    @property
    def sites(self) -> RepeatedScalarFieldContainer[Text]:
        """site_id列表, 用来说明该地址可在哪些站点环境下使用
        如果该列表为空, 表示不限制站点(即该地址在所有站点下都可用)
        """
        pass
    id: Text = ...
    """管理中心自动生成的uuid，用于用户选择地址时方便区分"""

    def __init__(self,
        *,
        title : Text = ...,
        address : Optional[Mapping[Text, Text]] = ...,
        sites : Optional[Iterable[Text]] = ...,
        id : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"address",b"address",u"id",b"id",u"sites",b"sites",u"title",b"title"]) -> None: ...

class ConnectionStatus(Message):
    DESCRIPTOR: Descriptor = ...
    class State(_State, metaclass=_StateEnumTypeWrapper):
        pass
    class _State:
        V = NewType('V', int)
    class _StateEnumTypeWrapper(_EnumTypeWrapper[_State.V], type):
        DESCRIPTOR: EnumDescriptor = ...
        State_UNKNOWN = ConnectionStatus.State.V(0)
        """未知"""

        State_CONNECTING = ConnectionStatus.State.V(1)
        """连接中"""

        State_CONNECTED = ConnectionStatus.State.V(2)
        """已连接"""

        State_LOGGEDIN = ConnectionStatus.State.V(3)
        """已登录"""

        State_DISCONNECTING = ConnectionStatus.State.V(4)
        """断开中"""

        State_DISCONNECTED = ConnectionStatus.State.V(5)
        """已断开"""

        State_ERROR = ConnectionStatus.State.V(6)
        """错误"""


    State_UNKNOWN = ConnectionStatus.State.V(0)
    """未知"""

    State_CONNECTING = ConnectionStatus.State.V(1)
    """连接中"""

    State_CONNECTED = ConnectionStatus.State.V(2)
    """已连接"""

    State_LOGGEDIN = ConnectionStatus.State.V(3)
    """已登录"""

    State_DISCONNECTING = ConnectionStatus.State.V(4)
    """断开中"""

    State_DISCONNECTED = ConnectionStatus.State.V(5)
    """已断开"""

    State_ERROR = ConnectionStatus.State.V(6)
    """错误"""


    STATE_FIELD_NUMBER: int
    ERROR_FIELD_NUMBER: int
    state: int = ...
    """连接状态"""

    @property
    def error(self) -> Error:
        """连接错误"""
        pass
    def __init__(self,
        *,
        state : int = ...,
        error : Optional[Error] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"error",b"error"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"error",b"error",u"state",b"state"]) -> None: ...

class Log(Message):
    """日志"""
    DESCRIPTOR: Descriptor = ...
    SOURCE_FIELD_NUMBER: int
    LEVEL_FIELD_NUMBER: int
    MSG_FIELD_NUMBER: int
    OWNER_ID_FIELD_NUMBER: int
    CREATED_AT_FIELD_NUMBER: int
    source: Text = ...
    level: Text = ...
    msg: Text = ...
    owner_id: Text = ...
    @property
    def created_at(self) -> Timestamp: ...
    def __init__(self,
        *,
        source : Text = ...,
        level : Text = ...,
        msg : Text = ...,
        owner_id : Text = ...,
        created_at : Optional[Timestamp] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"created_at",b"created_at"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"created_at",b"created_at",u"level",b"level",u"msg",b"msg",u"owner_id",b"owner_id",u"source",b"source"]) -> None: ...

class Logs(Message):
    """日志集合"""
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[Log]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[Log]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...

class Heartbeat(Message):
    DESCRIPTOR: Descriptor = ...
    CREATED_AT_FIELD_NUMBER: int
    @property
    def created_at(self) -> Timestamp: ...
    def __init__(self,
        *,
        created_at : Optional[Timestamp] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"created_at",b"created_at"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"created_at",b"created_at"]) -> None: ...

class MFP(Message):
    """交易账户留痕信息"""
    DESCRIPTOR: Descriptor = ...
    CPU_FIELD_NUMBER: int
    FDSN_FIELD_NUMBER: int
    HD_FIELD_NUMBER: int
    LIP_FIELD_NUMBER: int
    IIP_FIELD_NUMBER: int
    IPORT_FIELD_NUMBER: int
    MAC_FIELD_NUMBER: int
    OSV_FIELD_NUMBER: int
    PCN_FIELD_NUMBER: int
    PI_FIELD_NUMBER: int
    VER_FIELD_NUMBER: int
    PRDID_FIELD_NUMBER: int
    UUID_FIELD_NUMBER: int
    VOL_FIELD_NUMBER: int
    CPU: Text = ...
    """CPU 唯一标识"""

    FDSN: Text = ...
    """Hard Disk Serieal Number (compatible old spec)"""

    HD: Text = ...
    """Hard Disk"""

    LIP: Text = ...
    """Lan IP"""

    IIP: Text = ...
    """互联网IP"""

    IPORT: Text = ...
    """互联网PORT"""

    MAC: Text = ...
    """mac 地址"""

    OSV: Text = ...
    """Operating System Version"""

    PCN: Text = ...
    """Personal Computer Name"""

    PI: Text = ...
    """Partition Information，磁盘分区信息"""

    VER: Text = ...
    """客户端版本信息"""

    PRDID: Text = ...
    """客户端产品ID(Product ID)"""

    UUID: Text = ...
    """uuid"""

    VOL: Text = ...
    """系统盘卷标号，是指硬盘格式化时，为系统启动盘自动生成的磁盘标识信息，简称磁盘ID，由一串十六进制字符组成。"""

    def __init__(self,
        *,
        CPU : Text = ...,
        FDSN : Text = ...,
        HD : Text = ...,
        LIP : Text = ...,
        IIP : Text = ...,
        IPORT : Text = ...,
        MAC : Text = ...,
        OSV : Text = ...,
        PCN : Text = ...,
        PI : Text = ...,
        VER : Text = ...,
        PRDID : Text = ...,
        UUID : Text = ...,
        VOL : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"CPU",b"CPU",u"FDSN",b"FDSN",u"HD",b"HD",u"IIP",b"IIP",u"IPORT",b"IPORT",u"LIP",b"LIP",u"MAC",b"MAC",u"OSV",b"OSV",u"PCN",b"PCN",u"PI",b"PI",u"PRDID",b"PRDID",u"UUID",b"UUID",u"VER",b"VER",u"VOL",b"VOL"]) -> None: ...

class ServiceStatus(Message):
    DESCRIPTOR: Descriptor = ...
    class ExtInfoEntry(Message):
        DESCRIPTOR: Descriptor = ...
        KEY_FIELD_NUMBER: int
        VALUE_FIELD_NUMBER: int
        key: Text = ...
        value: Text = ...
        def __init__(self,
            *,
            key : Text = ...,
            value : Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: Literal[u"key",b"key",u"value",b"value"]) -> None: ...

    ERR_FIELD_NUMBER: int
    SERVICE_NAME_FIELD_NUMBER: int
    STARTUP_AT_FIELD_NUMBER: int
    EXT_INFO_FIELD_NUMBER: int
    @property
    def err(self) -> Error: ...
    service_name: Text = ...
    """服务名称"""

    @property
    def startup_at(self) -> Timestamp:
        """服务启动时间"""
        pass
    @property
    def ext_info(self) -> ScalarMap[Text, Text]:
        """其他描述信息"""
        pass
    def __init__(self,
        *,
        err : Optional[Error] = ...,
        service_name : Text = ...,
        startup_at : Optional[Timestamp] = ...,
        ext_info : Optional[Mapping[Text, Text]] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"err",b"err",u"startup_at",b"startup_at"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"err",b"err",u"ext_info",b"ext_info",u"service_name",b"service_name",u"startup_at",b"startup_at"]) -> None: ...

class CustomizedMessage(Message):
    """用户自定义消息, 参考: https://gnuixbiqmy.feishu.cn/docx/C6XWdYXQTon8H3xNPmMcrkxcn2b#KOEbdRvbMocm90xa2w0c0YwUnRe"""
    DESCRIPTOR: Descriptor = ...
    MSG_TYPE_FIELD_NUMBER: int
    MSG_BODY_FIELD_NUMBER: int
    msg_type: Text = ...
    """用户自定义消息类型"""

    msg_body: Text = ...
    """用户自定义消息内容"""

    def __init__(self,
        *,
        msg_type : Text = ...,
        msg_body : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"msg_body",b"msg_body",u"msg_type",b"msg_type"]) -> None: ...
