from typing import Any, Dict, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateUploadedFile")


@_attrs_define
class CreateUploadedFile:
    """
    Attributes:
        name (str): The unique name to give to the new file that will be uploaded.
        extension (str): The file extension of the new file to be uploaded, e.g. ".csv"
        description (Union[None, Unset, str]): The description for the new file.
    """

    name: str
    extension: str
    description: Union[None, Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        extension = self.extension

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "extension": extension,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        extension = d.pop("extension")

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        create_uploaded_file = cls(
            name=name,
            extension=extension,
            description=description,
        )

        return create_uploaded_file
