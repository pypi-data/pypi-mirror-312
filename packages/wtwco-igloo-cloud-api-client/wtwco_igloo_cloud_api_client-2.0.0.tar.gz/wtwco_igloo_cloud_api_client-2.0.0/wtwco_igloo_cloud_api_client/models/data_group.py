from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.id_and_name import IdAndName


T = TypeVar("T", bound="DataGroup")


@_attrs_define
class DataGroup:
    """
    Attributes:
        id (Union[Unset, int]): The id of the data group.
        name (Union[None, Unset, str]): The name of the data group, to be used in the API.
        help_ (Union[None, Unset, str]): A url linking to the documentation for this data group.
        position (Union[Unset, int]): Provides a user-friendly ordering of the data groups for the run.
        display_name (Union[None, Unset, str]): The user-friendly display name of the data group.
        owner_run_if_not_owned (Union[Unset, IdAndName]):
        version (Union[None, Unset, int]): The version of the data in this data group being used by this run.
        revision (Union[None, Unset, int]): The revision number of the data. The revision is incremented every time a
            change is made to the
            data in the data group.
        is_in_use (Union[Unset, bool]): Whether the datagroup is currently in use
    """

    id: Union[Unset, int] = UNSET
    name: Union[None, Unset, str] = UNSET
    help_: Union[None, Unset, str] = UNSET
    position: Union[Unset, int] = UNSET
    display_name: Union[None, Unset, str] = UNSET
    owner_run_if_not_owned: Union[Unset, "IdAndName"] = UNSET
    version: Union[None, Unset, int] = UNSET
    revision: Union[None, Unset, int] = UNSET
    is_in_use: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        help_: Union[None, Unset, str]
        if isinstance(self.help_, Unset):
            help_ = UNSET
        else:
            help_ = self.help_

        position = self.position

        display_name: Union[None, Unset, str]
        if isinstance(self.display_name, Unset):
            display_name = UNSET
        else:
            display_name = self.display_name

        owner_run_if_not_owned: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.owner_run_if_not_owned, Unset):
            owner_run_if_not_owned = self.owner_run_if_not_owned.to_dict()

        version: Union[None, Unset, int]
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        revision: Union[None, Unset, int]
        if isinstance(self.revision, Unset):
            revision = UNSET
        else:
            revision = self.revision

        is_in_use = self.is_in_use

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if help_ is not UNSET:
            field_dict["help"] = help_
        if position is not UNSET:
            field_dict["position"] = position
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if owner_run_if_not_owned is not UNSET:
            field_dict["ownerRunIfNotOwned"] = owner_run_if_not_owned
        if version is not UNSET:
            field_dict["version"] = version
        if revision is not UNSET:
            field_dict["revision"] = revision
        if is_in_use is not UNSET:
            field_dict["isInUse"] = is_in_use

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.id_and_name import IdAndName

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_help_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        help_ = _parse_help_(d.pop("help", UNSET))

        position = d.pop("position", UNSET)

        def _parse_display_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        display_name = _parse_display_name(d.pop("displayName", UNSET))

        _owner_run_if_not_owned = d.pop("ownerRunIfNotOwned", UNSET)
        owner_run_if_not_owned: Union[Unset, IdAndName]
        if isinstance(_owner_run_if_not_owned, Unset):
            owner_run_if_not_owned = UNSET
        else:
            owner_run_if_not_owned = IdAndName.from_dict(_owner_run_if_not_owned)

        def _parse_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        version = _parse_version(d.pop("version", UNSET))

        def _parse_revision(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        revision = _parse_revision(d.pop("revision", UNSET))

        is_in_use = d.pop("isInUse", UNSET)

        data_group = cls(
            id=id,
            name=name,
            help_=help_,
            position=position,
            display_name=display_name,
            owner_run_if_not_owned=owner_run_if_not_owned,
            version=version,
            revision=revision,
            is_in_use=is_in_use,
        )

        return data_group
