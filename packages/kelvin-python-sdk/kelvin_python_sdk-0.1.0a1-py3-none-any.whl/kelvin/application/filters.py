from __future__ import annotations

from typing import Callable

from typing_extensions import TypeAlias

from kelvin.krn import KRN, KRNAssetDataStream
from kelvin.message import ControlChangeStatus, KMessageTypeData, Message

KelvinFilterType: TypeAlias = Callable[[Message], bool]


def is_asset_data_message(msg: Message) -> bool:
    return isinstance(msg.resource, KRNAssetDataStream) and isinstance(msg.type, KMessageTypeData)


def is_data_message(msg: Message) -> bool:
    return isinstance(msg.type, KMessageTypeData)


def is_control_status_message(msg: Message) -> bool:
    return isinstance(msg, ControlChangeStatus)


def resource_equals(resource: KRN) -> KelvinFilterType:
    return lambda msg: msg.resource == resource


def input_equals(data: str) -> KelvinFilterType:
    def _check(msg: Message) -> bool:
        return isinstance(msg.resource, KRNAssetDataStream) and msg.resource.data_stream == data

    return _check


def asset_equals(asset: str) -> KelvinFilterType:
    def _check(msg: Message) -> bool:
        return isinstance(msg.resource, KRNAssetDataStream) and msg.resource.asset == asset

    return _check
