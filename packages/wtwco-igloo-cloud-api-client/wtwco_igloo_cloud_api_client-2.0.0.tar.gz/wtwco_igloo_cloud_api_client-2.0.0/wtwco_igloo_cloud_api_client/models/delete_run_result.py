from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteRunResult")


@_attrs_define
class DeleteRunResult:
    """
    Attributes:
        deleted_run_ids (Union[List[int], None, Unset]): The list of run ids that were deleted by the request.
    """

    deleted_run_ids: Union[List[int], None, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        deleted_run_ids: Union[List[int], None, Unset]
        if isinstance(self.deleted_run_ids, Unset):
            deleted_run_ids = UNSET
        elif isinstance(self.deleted_run_ids, list):
            deleted_run_ids = self.deleted_run_ids

        else:
            deleted_run_ids = self.deleted_run_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if deleted_run_ids is not UNSET:
            field_dict["deletedRunIds"] = deleted_run_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_deleted_run_ids(data: object) -> Union[List[int], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                deleted_run_ids_type_0 = cast(List[int], data)

                return deleted_run_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[int], None, Unset], data)

        deleted_run_ids = _parse_deleted_run_ids(d.pop("deletedRunIds", UNSET))

        delete_run_result = cls(
            deleted_run_ids=deleted_run_ids,
        )

        return delete_run_result
