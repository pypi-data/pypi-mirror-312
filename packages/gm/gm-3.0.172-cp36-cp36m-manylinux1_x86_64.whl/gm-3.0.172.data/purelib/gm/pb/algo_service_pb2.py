# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gm/pb/algo_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gm.pb import common_pb2 as gm_dot_pb_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='gm/pb/algo_service.proto',
  package='trade.api',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x18gm/pb/algo_service.proto\x12\ttrade.api\x1a\x12gm/pb/common.proto\"\x8b\x02\n\x10GetAlgoOrdersReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x12\n\naccount_id\x18\x02 \x01(\t\x12\x14\n\x0c\x61\x63\x63ount_name\x18\x06 \x01(\t\x12\x12\n\nchannel_id\x18\x07 \x01(\t\x12\x0f\n\x07symbols\x18\x03 \x03(\t\x12\x12\n\ncl_ord_ids\x18\x04 \x03(\t\x12?\n\nproperties\x18\x05 \x03(\x0b\x32+.trade.api.GetAlgoOrdersReq.PropertiesEntry\x1a\x31\n\x0fPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x62\x06proto3'
  ,
  dependencies=[gm_dot_pb_dot_common__pb2.DESCRIPTOR,])




_GETALGOORDERSREQ_PROPERTIESENTRY = _descriptor.Descriptor(
  name='PropertiesEntry',
  full_name='trade.api.GetAlgoOrdersReq.PropertiesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='trade.api.GetAlgoOrdersReq.PropertiesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='trade.api.GetAlgoOrdersReq.PropertiesEntry.value', index=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=278,
  serialized_end=327,
)

_GETALGOORDERSREQ = _descriptor.Descriptor(
  name='GetAlgoOrdersReq',
  full_name='trade.api.GetAlgoOrdersReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='trade.api.GetAlgoOrdersReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='account_id', full_name='trade.api.GetAlgoOrdersReq.account_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='account_name', full_name='trade.api.GetAlgoOrdersReq.account_name', index=2,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='channel_id', full_name='trade.api.GetAlgoOrdersReq.channel_id', index=3,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='symbols', full_name='trade.api.GetAlgoOrdersReq.symbols', index=4,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cl_ord_ids', full_name='trade.api.GetAlgoOrdersReq.cl_ord_ids', index=5,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='properties', full_name='trade.api.GetAlgoOrdersReq.properties', index=6,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_GETALGOORDERSREQ_PROPERTIESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=60,
  serialized_end=327,
)

_GETALGOORDERSREQ_PROPERTIESENTRY.containing_type = _GETALGOORDERSREQ
_GETALGOORDERSREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
_GETALGOORDERSREQ.fields_by_name['properties'].message_type = _GETALGOORDERSREQ_PROPERTIESENTRY
DESCRIPTOR.message_types_by_name['GetAlgoOrdersReq'] = _GETALGOORDERSREQ
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetAlgoOrdersReq = _reflection.GeneratedProtocolMessageType('GetAlgoOrdersReq', (_message.Message,), {

  'PropertiesEntry' : _reflection.GeneratedProtocolMessageType('PropertiesEntry', (_message.Message,), {
    'DESCRIPTOR' : _GETALGOORDERSREQ_PROPERTIESENTRY,
    '__module__' : 'gm.pb.algo_service_pb2'
    # @@protoc_insertion_point(class_scope:trade.api.GetAlgoOrdersReq.PropertiesEntry)
    })
  ,
  'DESCRIPTOR' : _GETALGOORDERSREQ,
  '__module__' : 'gm.pb.algo_service_pb2'
  # @@protoc_insertion_point(class_scope:trade.api.GetAlgoOrdersReq)
  })
_sym_db.RegisterMessage(GetAlgoOrdersReq)
_sym_db.RegisterMessage(GetAlgoOrdersReq.PropertiesEntry)


_GETALGOORDERSREQ_PROPERTIESENTRY._options = None
# @@protoc_insertion_point(module_scope)
