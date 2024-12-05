"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
from builtins import (
    bool,
    float,
    int,
)

from gm.pb.account_pb2 import (
    Position,
)

from google.protobuf.descriptor import (
    Descriptor,
    FileDescriptor,
)

from google.protobuf.duration_pb2 import (
    Duration,
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

class Indicator(Message):
    """绩效指标定义"""
    DESCRIPTOR: Descriptor = ...
    ACCOUNT_ID_FIELD_NUMBER: int
    PNL_RATIO_FIELD_NUMBER: int
    PNL_RATIO_ANNUAL_FIELD_NUMBER: int
    SHARP_RATIO_FIELD_NUMBER: int
    MAX_DRAWDOWN_FIELD_NUMBER: int
    RISK_RATIO_FIELD_NUMBER: int
    OPEN_COUNT_FIELD_NUMBER: int
    CLOSE_COUNT_FIELD_NUMBER: int
    WIN_COUNT_FIELD_NUMBER: int
    LOSE_COUNT_FIELD_NUMBER: int
    WIN_RATIO_FIELD_NUMBER: int
    CALMAR_RATIO_FIELD_NUMBER: int
    CREATED_AT_FIELD_NUMBER: int
    UPDATED_AT_FIELD_NUMBER: int
    account_id: Text = ...
    """账号ID"""

    pnl_ratio: float = ...
    """累计收益率(pnl/cum_inout)"""

    pnl_ratio_annual: float = ...
    """年化收益率"""

    sharp_ratio: float = ...
    """夏普比率"""

    max_drawdown: float = ...
    """最大回撤"""

    risk_ratio: float = ...
    """风险比率"""

    open_count: int = ...
    """开仓次数"""

    close_count: int = ...
    """平仓次数"""

    win_count: int = ...
    """盈利次数"""

    lose_count: int = ...
    """亏损次数"""

    win_ratio: float = ...
    """胜率"""

    calmar_ratio: float = ...
    """卡玛比率"""

    @property
    def created_at(self) -> Timestamp:
        """指标创建时间"""
        pass
    @property
    def updated_at(self) -> Timestamp:
        """指标变更时间"""
        pass
    def __init__(self,
        *,
        account_id : Text = ...,
        pnl_ratio : float = ...,
        pnl_ratio_annual : float = ...,
        sharp_ratio : float = ...,
        max_drawdown : float = ...,
        risk_ratio : float = ...,
        open_count : int = ...,
        close_count : int = ...,
        win_count : int = ...,
        lose_count : int = ...,
        win_ratio : float = ...,
        calmar_ratio : float = ...,
        created_at : Optional[Timestamp] = ...,
        updated_at : Optional[Timestamp] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"created_at",b"created_at",u"updated_at",b"updated_at"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"account_id",b"account_id",u"calmar_ratio",b"calmar_ratio",u"close_count",b"close_count",u"created_at",b"created_at",u"lose_count",b"lose_count",u"max_drawdown",b"max_drawdown",u"open_count",b"open_count",u"pnl_ratio",b"pnl_ratio",u"pnl_ratio_annual",b"pnl_ratio_annual",u"risk_ratio",b"risk_ratio",u"sharp_ratio",b"sharp_ratio",u"updated_at",b"updated_at",u"win_count",b"win_count",u"win_ratio",b"win_ratio"]) -> None: ...

class Indicators(Message):
    """指标集合"""
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[Indicator]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[Indicator]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...

class IndicatorDuration(Message):
    """按周期统计的指标（目前只有日频和分钟频）"""
    DESCRIPTOR: Descriptor = ...
    ACCOUNT_ID_FIELD_NUMBER: int
    PNL_RATIO_FIELD_NUMBER: int
    PNL_FIELD_NUMBER: int
    FPNL_FIELD_NUMBER: int
    FROZEN_FIELD_NUMBER: int
    CASH_FIELD_NUMBER: int
    NAV_FIELD_NUMBER: int
    POSITIONS_FIELD_NUMBER: int
    CUM_PNL_FIELD_NUMBER: int
    CUM_BUY_FIELD_NUMBER: int
    CUM_SELL_FIELD_NUMBER: int
    CUM_COMMISSION_FIELD_NUMBER: int
    DURATION_FIELD_NUMBER: int
    CREATED_AT_FIELD_NUMBER: int
    UPDATED_AT_FIELD_NUMBER: int
    account_id: Text = ...
    """账号ID"""

    pnl_ratio: float = ...
    """周期快照类指标
    收益率快照
    """

    pnl: float = ...
    """收益快照"""

    fpnl: float = ...
    """浮盈浮亏快照"""

    frozen: float = ...
    """持仓冻结快照"""

    cash: float = ...
    """资金快照"""

    nav: float = ...
    """资金快照"""

    @property
    def positions(self) -> RepeatedCompositeFieldContainer[Position]:
        """持仓快照"""
        pass
    cum_pnl: float = ...
    """周期累计类指标
    周期累计盈亏
    """

    cum_buy: float = ...
    """周期累计买入额"""

    cum_sell: float = ...
    """周期累计卖出额"""

    cum_commission: float = ...
    """周期累计手续费"""

    @property
    def duration(self) -> Duration:
        """指标统计周期"""
        pass
    @property
    def created_at(self) -> Timestamp:
        """指标创建时间"""
        pass
    @property
    def updated_at(self) -> Timestamp:
        """指标创建时间"""
        pass
    def __init__(self,
        *,
        account_id : Text = ...,
        pnl_ratio : float = ...,
        pnl : float = ...,
        fpnl : float = ...,
        frozen : float = ...,
        cash : float = ...,
        nav : float = ...,
        positions : Optional[Iterable[Position]] = ...,
        cum_pnl : float = ...,
        cum_buy : float = ...,
        cum_sell : float = ...,
        cum_commission : float = ...,
        duration : Optional[Duration] = ...,
        created_at : Optional[Timestamp] = ...,
        updated_at : Optional[Timestamp] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"created_at",b"created_at",u"duration",b"duration",u"updated_at",b"updated_at"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"account_id",b"account_id",u"cash",b"cash",u"created_at",b"created_at",u"cum_buy",b"cum_buy",u"cum_commission",b"cum_commission",u"cum_pnl",b"cum_pnl",u"cum_sell",b"cum_sell",u"duration",b"duration",u"fpnl",b"fpnl",u"frozen",b"frozen",u"nav",b"nav",u"pnl",b"pnl",u"pnl_ratio",b"pnl_ratio",u"positions",b"positions",u"updated_at",b"updated_at"]) -> None: ...

class IndicatorDurations(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[IndicatorDuration]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[IndicatorDuration]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...
