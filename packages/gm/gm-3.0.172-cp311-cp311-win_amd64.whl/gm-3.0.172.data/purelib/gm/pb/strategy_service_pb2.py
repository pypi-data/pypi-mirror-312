# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gm/pb/strategy_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gm.pb import common_pb2 as gm_dot_pb_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='gm/pb/strategy_service.proto',
  package='strategy.api',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1cgm/pb/strategy_service.proto\x12\x0cstrategy.api\x1a\x12gm/pb/common.proto\"I\n\x0eSetAccountsReq\x12\x13\n\x0bstrategy_id\x18\x01 \x01(\t\x12\r\n\x05stage\x18\x02 \x01(\x05\x12\x13\n\x0b\x61\x63\x63ount_ids\x18\x03 \x03(\t\"4\n\x0eGetAccountsReq\x12\x13\n\x0bstrategy_id\x18\x01 \x01(\t\x12\r\n\x05stage\x18\x02 \x01(\x05\"%\n\x0eGetAccountsRsp\x12\x13\n\x0b\x61\x63\x63ount_ids\x18\x02 \x03(\t\"/\n\x19GetStrategiesToAccountReq\x12\x12\n\naccount_id\x18\x01 \x01(\t\"J\n\x10GetStrategiesReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x14\n\x0cstrategy_ids\x18\x02 \x03(\t\"K\n\x17GetStrategiesOfStageReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x0e\n\x06stages\x18\x02 \x03(\x05\"(\n\x10\x44\x65lStrategiesReq\x12\x14\n\x0cstrategy_ids\x18\x01 \x03(\t\"M\n\x13GetStartCommandsReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x14\n\x0cstrategy_ids\x18\x02 \x03(\t\"P\n\x16GetStrategyStatusesReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x14\n\x0cstrategy_ids\x18\x02 \x03(\t\"K\n\x12GetStrategyLogsReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x13\n\x0bstrategy_id\x18\x02 \x01(\tb\x06proto3'
  ,
  dependencies=[gm_dot_pb_dot_common__pb2.DESCRIPTOR,])




_SETACCOUNTSREQ = _descriptor.Descriptor(
  name='SetAccountsReq',
  full_name='strategy.api.SetAccountsReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='strategy_id', full_name='strategy.api.SetAccountsReq.strategy_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stage', full_name='strategy.api.SetAccountsReq.stage', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='account_ids', full_name='strategy.api.SetAccountsReq.account_ids', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=66,
  serialized_end=139,
)


_GETACCOUNTSREQ = _descriptor.Descriptor(
  name='GetAccountsReq',
  full_name='strategy.api.GetAccountsReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='strategy_id', full_name='strategy.api.GetAccountsReq.strategy_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stage', full_name='strategy.api.GetAccountsReq.stage', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=141,
  serialized_end=193,
)


_GETACCOUNTSRSP = _descriptor.Descriptor(
  name='GetAccountsRsp',
  full_name='strategy.api.GetAccountsRsp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_ids', full_name='strategy.api.GetAccountsRsp.account_ids', index=0,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=195,
  serialized_end=232,
)


_GETSTRATEGIESTOACCOUNTREQ = _descriptor.Descriptor(
  name='GetStrategiesToAccountReq',
  full_name='strategy.api.GetStrategiesToAccountReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='strategy.api.GetStrategiesToAccountReq.account_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=234,
  serialized_end=281,
)


_GETSTRATEGIESREQ = _descriptor.Descriptor(
  name='GetStrategiesReq',
  full_name='strategy.api.GetStrategiesReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='strategy.api.GetStrategiesReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='strategy_ids', full_name='strategy.api.GetStrategiesReq.strategy_ids', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=283,
  serialized_end=357,
)


_GETSTRATEGIESOFSTAGEREQ = _descriptor.Descriptor(
  name='GetStrategiesOfStageReq',
  full_name='strategy.api.GetStrategiesOfStageReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='strategy.api.GetStrategiesOfStageReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stages', full_name='strategy.api.GetStrategiesOfStageReq.stages', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=359,
  serialized_end=434,
)


_DELSTRATEGIESREQ = _descriptor.Descriptor(
  name='DelStrategiesReq',
  full_name='strategy.api.DelStrategiesReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='strategy_ids', full_name='strategy.api.DelStrategiesReq.strategy_ids', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=436,
  serialized_end=476,
)


_GETSTARTCOMMANDSREQ = _descriptor.Descriptor(
  name='GetStartCommandsReq',
  full_name='strategy.api.GetStartCommandsReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='strategy.api.GetStartCommandsReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='strategy_ids', full_name='strategy.api.GetStartCommandsReq.strategy_ids', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=478,
  serialized_end=555,
)


_GETSTRATEGYSTATUSESREQ = _descriptor.Descriptor(
  name='GetStrategyStatusesReq',
  full_name='strategy.api.GetStrategyStatusesReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='strategy.api.GetStrategyStatusesReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='strategy_ids', full_name='strategy.api.GetStrategyStatusesReq.strategy_ids', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=557,
  serialized_end=637,
)


_GETSTRATEGYLOGSREQ = _descriptor.Descriptor(
  name='GetStrategyLogsReq',
  full_name='strategy.api.GetStrategyLogsReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='strategy.api.GetStrategyLogsReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='strategy_id', full_name='strategy.api.GetStrategyLogsReq.strategy_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=639,
  serialized_end=714,
)

_GETSTRATEGIESREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
_GETSTRATEGIESOFSTAGEREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
_GETSTARTCOMMANDSREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
_GETSTRATEGYSTATUSESREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
_GETSTRATEGYLOGSREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
DESCRIPTOR.message_types_by_name['SetAccountsReq'] = _SETACCOUNTSREQ
DESCRIPTOR.message_types_by_name['GetAccountsReq'] = _GETACCOUNTSREQ
DESCRIPTOR.message_types_by_name['GetAccountsRsp'] = _GETACCOUNTSRSP
DESCRIPTOR.message_types_by_name['GetStrategiesToAccountReq'] = _GETSTRATEGIESTOACCOUNTREQ
DESCRIPTOR.message_types_by_name['GetStrategiesReq'] = _GETSTRATEGIESREQ
DESCRIPTOR.message_types_by_name['GetStrategiesOfStageReq'] = _GETSTRATEGIESOFSTAGEREQ
DESCRIPTOR.message_types_by_name['DelStrategiesReq'] = _DELSTRATEGIESREQ
DESCRIPTOR.message_types_by_name['GetStartCommandsReq'] = _GETSTARTCOMMANDSREQ
DESCRIPTOR.message_types_by_name['GetStrategyStatusesReq'] = _GETSTRATEGYSTATUSESREQ
DESCRIPTOR.message_types_by_name['GetStrategyLogsReq'] = _GETSTRATEGYLOGSREQ
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SetAccountsReq = _reflection.GeneratedProtocolMessageType('SetAccountsReq', (_message.Message,), {
  'DESCRIPTOR' : _SETACCOUNTSREQ,
  '__module__' : 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.SetAccountsReq)
  })
_sym_db.RegisterMessage(SetAccountsReq)

GetAccountsReq = _reflection.GeneratedProtocolMessageType('GetAccountsReq', (_message.Message,), {
  'DESCRIPTOR' : _GETACCOUNTSREQ,
  '__module__' : 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetAccountsReq)
  })
_sym_db.RegisterMessage(GetAccountsReq)

GetAccountsRsp = _reflection.GeneratedProtocolMessageType('GetAccountsRsp', (_message.Message,), {
  'DESCRIPTOR' : _GETACCOUNTSRSP,
  '__module__' : 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetAccountsRsp)
  })
_sym_db.RegisterMessage(GetAccountsRsp)

GetStrategiesToAccountReq = _reflection.GeneratedProtocolMessageType('GetStrategiesToAccountReq', (_message.Message,), {
  'DESCRIPTOR' : _GETSTRATEGIESTOACCOUNTREQ,
  '__module__' : 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetStrategiesToAccountReq)
  })
_sym_db.RegisterMessage(GetStrategiesToAccountReq)

GetStrategiesReq = _reflection.GeneratedProtocolMessageType('GetStrategiesReq', (_message.Message,), {
  'DESCRIPTOR' : _GETSTRATEGIESREQ,
  '__module__' : 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetStrategiesReq)
  })
_sym_db.RegisterMessage(GetStrategiesReq)

GetStrategiesOfStageReq = _reflection.GeneratedProtocolMessageType('GetStrategiesOfStageReq', (_message.Message,), {
  'DESCRIPTOR' : _GETSTRATEGIESOFSTAGEREQ,
  '__module__' : 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetStrategiesOfStageReq)
  })
_sym_db.RegisterMessage(GetStrategiesOfStageReq)

DelStrategiesReq = _reflection.GeneratedProtocolMessageType('DelStrategiesReq', (_message.Message,), {
  'DESCRIPTOR' : _DELSTRATEGIESREQ,
  '__module__' : 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.DelStrategiesReq)
  })
_sym_db.RegisterMessage(DelStrategiesReq)

GetStartCommandsReq = _reflection.GeneratedProtocolMessageType('GetStartCommandsReq', (_message.Message,), {
  'DESCRIPTOR' : _GETSTARTCOMMANDSREQ,
  '__module__' : 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetStartCommandsReq)
  })
_sym_db.RegisterMessage(GetStartCommandsReq)

GetStrategyStatusesReq = _reflection.GeneratedProtocolMessageType('GetStrategyStatusesReq', (_message.Message,), {
  'DESCRIPTOR' : _GETSTRATEGYSTATUSESREQ,
  '__module__' : 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetStrategyStatusesReq)
  })
_sym_db.RegisterMessage(GetStrategyStatusesReq)

GetStrategyLogsReq = _reflection.GeneratedProtocolMessageType('GetStrategyLogsReq', (_message.Message,), {
  'DESCRIPTOR' : _GETSTRATEGYLOGSREQ,
  '__module__' : 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetStrategyLogsReq)
  })
_sym_db.RegisterMessage(GetStrategyLogsReq)


# @@protoc_insertion_point(module_scope)
