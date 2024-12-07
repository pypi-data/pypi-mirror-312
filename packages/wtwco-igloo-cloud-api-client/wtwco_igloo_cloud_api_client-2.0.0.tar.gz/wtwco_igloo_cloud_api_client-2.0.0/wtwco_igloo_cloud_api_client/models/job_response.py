from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job import Job
    from ..models.message import Message


T = TypeVar("T", bound="JobResponse")


@_attrs_define
class JobResponse:
    """
    Attributes:
        messages (Union[List['Message'], None, Unset]):
        result (Union[Unset, Job]):
    """

    messages: Union[List["Message"], None, Unset] = UNSET
    result: Union[Unset, "Job"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        messages: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.messages, Unset):
            messages = UNSET
        elif isinstance(self.messages, list):
            messages = []
            for messages_type_0_item_data in self.messages:
                messages_type_0_item = messages_type_0_item_data.to_dict()
                messages.append(messages_type_0_item)

        else:
            messages = self.messages

        result: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if messages is not UNSET:
            field_dict["messages"] = messages
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.job import Job
        from ..models.message import Message

        d = src_dict.copy()

        def _parse_messages(data: object) -> Union[List["Message"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                messages_type_0 = []
                _messages_type_0 = data
                for messages_type_0_item_data in _messages_type_0:
                    messages_type_0_item = Message.from_dict(messages_type_0_item_data)

                    messages_type_0.append(messages_type_0_item)

                return messages_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["Message"], None, Unset], data)

        messages = _parse_messages(d.pop("messages", UNSET))

        _result = d.pop("result", UNSET)
        result: Union[Unset, Job]
        if isinstance(_result, Unset):
            result = UNSET
        else:
            result = Job.from_dict(_result)

        job_response = cls(
            messages=messages,
            result=result,
        )

        return job_response
