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

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer,
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

class GetContinuousContractsReq(Message):
    DESCRIPTOR: Descriptor = ...
    CSYMBOL_FIELD_NUMBER: int
    START_DATE_FIELD_NUMBER: int
    END_DATE_FIELD_NUMBER: int
    csymbol: Text = ...
    """连续合约代码
    参数用法说明:
    必填，使用时参考查询代码，
    支持主力合约、次主力、前5个月份连续合约代码，如：
    1000股指期货主力连续合约：CFFEX.IM，
    """

    start_date: Text = ...
    """开始时间
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    end_date: Text = ...
    """结束时间
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    def __init__(self,
        *,
        csymbol : Text = ...,
        start_date : Text = ...,
        end_date : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"csymbol",b"csymbol",u"end_date",b"end_date",u"start_date",b"start_date"]) -> None: ...

class ContinuousContractsInfo(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    TRADE_DATE_FIELD_NUMBER: int
    symbol: Text = ...
    """标的代码"""

    @property
    def trade_date(self) -> Timestamp:
        """交易日期"""
        pass
    def __init__(self,
        *,
        symbol : Text = ...,
        trade_date : Optional[Timestamp] = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"trade_date",b"trade_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"symbol",b"symbol",u"trade_date",b"trade_date"]) -> None: ...

class GetContinuousContractsRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[ContinuousContractsInfo]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[ContinuousContractsInfo]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...

class FutGetContractInfoReq(Message):
    DESCRIPTOR: Descriptor = ...
    PRODUCT_CODES_FIELD_NUMBER: int
    @property
    def product_codes(self) -> RepeatedScalarFieldContainer[Text]:
        """品种代码
        参数用法说明:
        必填参数, 且列表至少包含一个 code
        必填，交易品种代码，如：IF，AL
        采用list格式时，多个标的代码示例：['IF', 'AL']
        """
        pass
    def __init__(self,
        *,
        product_codes : Optional[Iterable[Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"product_codes",b"product_codes"]) -> None: ...

class FutContractInfo(Message):
    DESCRIPTOR: Descriptor = ...
    PRODUCT_NAME_FIELD_NUMBER: int
    PRODUCT_CODE_FIELD_NUMBER: int
    UNDERLYING_SYMBOL_FIELD_NUMBER: int
    MULTIPLIER_FIELD_NUMBER: int
    TRADE_UNIT_FIELD_NUMBER: int
    PRICE_UNIT_FIELD_NUMBER: int
    PRICE_TICK_FIELD_NUMBER: int
    DELIVERY_MONTH_FIELD_NUMBER: int
    TRADE_TIME_FIELD_NUMBER: int
    PRICE_RANGE_FIELD_NUMBER: int
    MINIMUM_MARGIN_FIELD_NUMBER: int
    LAST_TRADE_DATE_FIELD_NUMBER: int
    DELIVERY_DATE_FIELD_NUMBER: int
    DELIVERY_METHOD_FIELD_NUMBER: int
    EXCHANGE_NAME_FIELD_NUMBER: int
    EXCHANGE_FIELD_NUMBER: int
    product_name: Text = ...
    """交易品种  --交易品种名称，如：沪深300指数，铝"""

    product_code: Text = ...
    """交易代码  --交易品种代码，如：IF，AL"""

    underlying_symbol: Text = ...
    """合约标的 --如：SHSE.000300， AL"""

    multiplier: int = ...
    """合约乘数  --如：200，5"""

    trade_unit: Text = ...
    """交易单位  --如：每点人民币200元，5吨/手"""

    price_unit: Text = ...
    """报价单位   --如：指数点，元（人民币）/吨"""

    price_tick: Text = ...
    """价格最小变动单位  --如：0.2点，5元/吨"""

    delivery_month: Text = ...
    """合约月份  --如：当月、下月及随后两个季月，1～12月"""

    trade_time: Text = ...
    """交易时间  --如：“9:30-11:30，13:00-15:00”，“上午9:00－11:30 ，下午1:30－3:00和交易所规定的其他交易时间”"""

    price_range: Text = ...
    """涨跌停板幅度  --每日价格最大波动限制，如：“上一个交易日结算价的±10%”，“上一交易日结算价±3%”"""

    minimum_margin: Text = ...
    """最低交易保证金  --交易所公布的最低保证金比例，如：“合约价值的8%”，“合约价值的5%”"""

    last_trade_date: Text = ...
    """最后交易日   -- 如：“合约到期月份的第三个星期五，遇国家法定假日顺延”，“合约月份的15日（遇国家法定节假日顺延，春节月份等最后交易日交易所可另行调整并通知）”"""

    delivery_date: Text = ...
    """交割日期  --如：“同最后交易日”，“最后交易日后连续三个工作日”"""

    delivery_method: Text = ...
    """交割方式  --如：现金交割，实物交割"""

    exchange_name: Text = ...
    """交易所名称 --上市交易所名称，如：中国金融期货交易所，上海期货交易所"""

    exchange: Text = ...
    """交易所代码  --上市交易所代码，如：CFFEX，SHFE"""

    def __init__(self,
        *,
        product_name : Text = ...,
        product_code : Text = ...,
        underlying_symbol : Text = ...,
        multiplier : int = ...,
        trade_unit : Text = ...,
        price_unit : Text = ...,
        price_tick : Text = ...,
        delivery_month : Text = ...,
        trade_time : Text = ...,
        price_range : Text = ...,
        minimum_margin : Text = ...,
        last_trade_date : Text = ...,
        delivery_date : Text = ...,
        delivery_method : Text = ...,
        exchange_name : Text = ...,
        exchange : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"delivery_date",b"delivery_date",u"delivery_method",b"delivery_method",u"delivery_month",b"delivery_month",u"exchange",b"exchange",u"exchange_name",b"exchange_name",u"last_trade_date",b"last_trade_date",u"minimum_margin",b"minimum_margin",u"multiplier",b"multiplier",u"price_range",b"price_range",u"price_tick",b"price_tick",u"price_unit",b"price_unit",u"product_code",b"product_code",u"product_name",b"product_name",u"trade_time",b"trade_time",u"trade_unit",b"trade_unit",u"underlying_symbol",b"underlying_symbol"]) -> None: ...

class FutGetContractInfoRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[FutContractInfo]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[FutContractInfo]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...

class FutGetTransactionRankingReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    TRADE_DATE_FIELD_NUMBER: int
    INDICATOR_FIELD_NUMBER: int
    symbol: Text = ...
    """期货合约代码
    参数用法说明:
    必填，期货具体合约代码，使用时参考symbol
    """

    trade_date: Text = ...
    """交易日期
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    indicator: Text = ...
    """排名指标
    参数用法说明:
    排名指标，即用于排名的依据，可选：
    'volume'-成交量排名（默认）
    ‘long’-持买单量排名
    ‘short’-持卖单量排名
    默认None表示成交量排名
    """

    def __init__(self,
        *,
        symbol : Text = ...,
        trade_date : Text = ...,
        indicator : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"indicator",b"indicator",u"symbol",b"symbol",u"trade_date",b"trade_date"]) -> None: ...

class FutTransactionRanking(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    TRADE_DATE_FIELD_NUMBER: int
    MEMBER_NAME_FIELD_NUMBER: int
    INDICATOR_NUMBER_FIELD_NUMBER: int
    INDICATOR_CHANGE_FIELD_NUMBER: int
    RANKING_FIELD_NUMBER: int
    RANKING_CHANGE_FIELD_NUMBER: int
    RANKING_CHANGE_IS_NULL_FIELD_NUMBER: int
    symbol: Text = ...
    """期货合约代码  --必填，使用时参考symbol"""

    @property
    def trade_date(self) -> Timestamp:
        """交易日期  --"""
        pass
    member_name: Text = ...
    """期货公司会员简称"""

    indicator_number: int = ...
    """排名指标数值  --单位：手。视乎所选的排名指标indicator，分别为：成交量（indicator为'volume'时）持买单量（indicator为'long'时）持卖单量（indicator为‘short’时）"""

    indicator_change: int = ...
    """排名指标比上交易日增减  --单位：手"""

    ranking: int = ...
    """排名名次"""

    ranking_change: int = ...
    """排名名次比上交易日增减"""

    ranking_change_is_null: bool = ...
    """判断 ranking_change 的值是否为空"""

    def __init__(self,
        *,
        symbol : Text = ...,
        trade_date : Optional[Timestamp] = ...,
        member_name : Text = ...,
        indicator_number : int = ...,
        indicator_change : int = ...,
        ranking : int = ...,
        ranking_change : int = ...,
        ranking_change_is_null : bool = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"trade_date",b"trade_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"indicator_change",b"indicator_change",u"indicator_number",b"indicator_number",u"member_name",b"member_name",u"ranking",b"ranking",u"ranking_change",b"ranking_change",u"ranking_change_is_null",b"ranking_change_is_null",u"symbol",b"symbol",u"trade_date",b"trade_date"]) -> None: ...

class FutGetTransactionRankingRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[FutTransactionRanking]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[FutTransactionRanking]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...

class FutGetTransactionRankingsReq(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOLS_FIELD_NUMBER: int
    TRADE_DATE_FIELD_NUMBER: int
    INDICATORS_FIELD_NUMBER: int
    @property
    def symbols(self) -> RepeatedScalarFieldContainer[Text]:
        """期货合约代码
        参数用法说明:
        必填，期货具体合约代码，使用时参考symbol
        """
        pass
    trade_date: Text = ...
    """交易日期
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    @property
    def indicators(self) -> RepeatedScalarFieldContainer[Text]:
        """排名指标
        参数用法说明:
        排名指标，即用于排名的依据，可选：
        'volume'-成交量排名（默认）
        ‘long’-持买单量排名
        ‘short’-持卖单量排名
        默认None表示成交量排名
        """
        pass
    def __init__(self,
        *,
        symbols : Optional[Iterable[Text]] = ...,
        trade_date : Text = ...,
        indicators : Optional[Iterable[Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"indicators",b"indicators",u"symbols",b"symbols",u"trade_date",b"trade_date"]) -> None: ...

class FutTransactionRankings(Message):
    DESCRIPTOR: Descriptor = ...
    SYMBOL_FIELD_NUMBER: int
    TRADE_DATE_FIELD_NUMBER: int
    MEMBER_NAME_FIELD_NUMBER: int
    INDICATOR_NUMBER_FIELD_NUMBER: int
    INDICATOR_CHANGE_FIELD_NUMBER: int
    RANKING_FIELD_NUMBER: int
    RANKING_CHANGE_FIELD_NUMBER: int
    RANKING_CHANGE_IS_NULL_FIELD_NUMBER: int
    INDICATOR_FIELD_NUMBER: int
    symbol: Text = ...
    """期货合约代码  --必填，使用时参考symbol"""

    @property
    def trade_date(self) -> Timestamp:
        """交易日期  --"""
        pass
    member_name: Text = ...
    """期货公司会员简称"""

    indicator_number: int = ...
    """排名指标数值  --单位：手。视乎所选的排名指标indicator，分别为：成交量（indicator为'volume'时）持买单量（indicator为'long'时）持卖单量（indicator为‘short’时）"""

    indicator_change: int = ...
    """排名指标比上交易日增减  --单位：手"""

    ranking: int = ...
    """排名名次"""

    ranking_change: int = ...
    """排名名次比上交易日增减"""

    ranking_change_is_null: bool = ...
    """判断 ranking_change 的值是否为空"""

    indicator: Text = ...
    """指标名称"""

    def __init__(self,
        *,
        symbol : Text = ...,
        trade_date : Optional[Timestamp] = ...,
        member_name : Text = ...,
        indicator_number : int = ...,
        indicator_change : int = ...,
        ranking : int = ...,
        ranking_change : int = ...,
        ranking_change_is_null : bool = ...,
        indicator : Text = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"trade_date",b"trade_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"indicator",b"indicator",u"indicator_change",b"indicator_change",u"indicator_number",b"indicator_number",u"member_name",b"member_name",u"ranking",b"ranking",u"ranking_change",b"ranking_change",u"ranking_change_is_null",b"ranking_change_is_null",u"symbol",b"symbol",u"trade_date",b"trade_date"]) -> None: ...

class FutGetTransactionRankingsRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[FutTransactionRankings]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[FutTransactionRankings]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...

class GetWarehouseReceiptReq(Message):
    DESCRIPTOR: Descriptor = ...
    PRODUCT_CODE_FIELD_NUMBER: int
    START_DATE_FIELD_NUMBER: int
    END_DATE_FIELD_NUMBER: int
    product_code: Text = ...
    """品种代码
    参数用法说明:
    必填，只能填写一个交易品种代码，如：AL
    """

    start_date: Text = ...
    """开始时间
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    end_date: Text = ...
    """结束时间
    参数用法说明:
    查询时间, 本地时间, 格式为: YYYY-MM-DD
    为空时, 表示当前日期
    """

    def __init__(self,
        *,
        product_code : Text = ...,
        start_date : Text = ...,
        end_date : Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"end_date",b"end_date",u"product_code",b"product_code",u"start_date",b"start_date"]) -> None: ...

class WarehouseReceiptInfo(Message):
    DESCRIPTOR: Descriptor = ...
    TRADE_DATE_FIELD_NUMBER: int
    EXCHANGE_FIELD_NUMBER: int
    EXCHANGE_NAME_FIELD_NUMBER: int
    PRODUCT_CODE_FIELD_NUMBER: int
    PRODUCT_NAME_FIELD_NUMBER: int
    ON_WARRANT_FIELD_NUMBER: int
    WARRANT_UNIT_FIELD_NUMBER: int
    WAREHOUSE_FIELD_NUMBER: int
    FUTURE_INVENTORY_FIELD_NUMBER: int
    FUTURE_INVENTORY_CHANGE_FIELD_NUMBER: int
    WAREHOUSE_CAPACITY_FIELD_NUMBER: int
    WAREHOUSE_CAPACITY_CHANGE_FIELD_NUMBER: int
    INVENTORY_SUBTOTAL_FIELD_NUMBER: int
    INVENTORY_SUBTOTAL_CHANGE_FIELD_NUMBER: int
    EFFECTIVE_FORECAST_FIELD_NUMBER: int
    PREMIUM_FIELD_NUMBER: int
    @property
    def trade_date(self) -> Timestamp:
        """交易日期 --"""
        pass
    exchange: Text = ...
    """期货交易所代码 --期货品种对应交易所代码，如：CFFEX，SHFE"""

    exchange_name: Text = ...
    """期货交易所名称 --上市交易所名称，如：中国金融期货交易所，上海期货交易所"""

    product_code: Text = ...
    """交易代码 --交易品种代码，如：IF，AL"""

    product_name: Text = ...
    """交易品种 --交易品种名称，如：沪深300指数，铝"""

    on_warrant: int = ...
    """注册仓单数量 --"""

    warrant_unit: Text = ...
    """仓单单位 -- 仅支持郑商所品种"""

    warehouse: Text = ...
    """仓库名称 --"""

    future_inventory: int = ...
    """期货库存 --"""

    future_inventory_change: int = ...
    """期货库存增减 --"""

    warehouse_capacity: int = ...
    """可用库容量 --"""

    warehouse_capacity_change: int = ...
    """可用库容量增减 --"""

    inventory_subtotal: int = ...
    """库存小计 --"""

    inventory_subtotal_change: int = ...
    """库存小计增减 --"""

    effective_forecast: int = ...
    """有效预报 --仅支持郑商所品种"""

    premium: int = ...
    """升贴水 --"""

    def __init__(self,
        *,
        trade_date : Optional[Timestamp] = ...,
        exchange : Text = ...,
        exchange_name : Text = ...,
        product_code : Text = ...,
        product_name : Text = ...,
        on_warrant : int = ...,
        warrant_unit : Text = ...,
        warehouse : Text = ...,
        future_inventory : int = ...,
        future_inventory_change : int = ...,
        warehouse_capacity : int = ...,
        warehouse_capacity_change : int = ...,
        inventory_subtotal : int = ...,
        inventory_subtotal_change : int = ...,
        effective_forecast : int = ...,
        premium : int = ...,
        ) -> None: ...
    def HasField(self, field_name: Literal[u"trade_date",b"trade_date"]) -> bool: ...
    def ClearField(self, field_name: Literal[u"effective_forecast",b"effective_forecast",u"exchange",b"exchange",u"exchange_name",b"exchange_name",u"future_inventory",b"future_inventory",u"future_inventory_change",b"future_inventory_change",u"inventory_subtotal",b"inventory_subtotal",u"inventory_subtotal_change",b"inventory_subtotal_change",u"on_warrant",b"on_warrant",u"premium",b"premium",u"product_code",b"product_code",u"product_name",b"product_name",u"trade_date",b"trade_date",u"warehouse",b"warehouse",u"warehouse_capacity",b"warehouse_capacity",u"warehouse_capacity_change",b"warehouse_capacity_change",u"warrant_unit",b"warrant_unit"]) -> None: ...

class GetWarehouseReceiptRsp(Message):
    DESCRIPTOR: Descriptor = ...
    DATA_FIELD_NUMBER: int
    @property
    def data(self) -> RepeatedCompositeFieldContainer[WarehouseReceiptInfo]: ...
    def __init__(self,
        *,
        data : Optional[Iterable[WarehouseReceiptInfo]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: Literal[u"data",b"data"]) -> None: ...
