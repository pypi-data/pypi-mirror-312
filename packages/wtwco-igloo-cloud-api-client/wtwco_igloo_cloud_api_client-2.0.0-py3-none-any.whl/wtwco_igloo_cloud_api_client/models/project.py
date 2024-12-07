from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Project")


@_attrs_define
class Project:
    """
    Attributes:
        id (Union[Unset, int]): The id value of this project.
        name (Union[None, Unset, str]): The name for this project.
        description (Union[None, Unset, str]): The description of the project.
        run_count (Union[Unset, int]): The number of runs of this project.
        model_version_id (Union[Unset, int]): The id of the model version used by the project.
        default_pool (Union[None, Unset, str]): The default pool for the project.
    """

    id: Union[Unset, int] = UNSET
    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    run_count: Union[Unset, int] = UNSET
    model_version_id: Union[Unset, int] = UNSET
    default_pool: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        run_count = self.run_count

        model_version_id = self.model_version_id

        default_pool: Union[None, Unset, str]
        if isinstance(self.default_pool, Unset):
            default_pool = UNSET
        else:
            default_pool = self.default_pool

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if run_count is not UNSET:
            field_dict["runCount"] = run_count
        if model_version_id is not UNSET:
            field_dict["modelVersionId"] = model_version_id
        if default_pool is not UNSET:
            field_dict["defaultPool"] = default_pool

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        run_count = d.pop("runCount", UNSET)

        model_version_id = d.pop("modelVersionId", UNSET)

        def _parse_default_pool(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_pool = _parse_default_pool(d.pop("defaultPool", UNSET))

        project = cls(
            id=id,
            name=name,
            description=description,
            run_count=run_count,
            model_version_id=model_version_id,
            default_pool=default_pool,
        )

        return project
