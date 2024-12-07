from typing import Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SubmitJob")


@_attrs_define
class SubmitJob:
    """
    Attributes:
        project_id (int): The id of the project that contains the run you wish to calculate.
        run_id (int): The id of the run that you wish to calculate.
        pool (str): The name of the pool you wish to use to calculate the model.
    """

    project_id: int
    run_id: int
    pool: str

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id

        run_id = self.run_id

        pool = self.pool

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "projectId": project_id,
                "runId": run_id,
                "pool": pool,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("projectId")

        run_id = d.pop("runId")

        pool = d.pop("pool")

        submit_job = cls(
            project_id=project_id,
            run_id=run_id,
            pool=pool,
        )

        return submit_job
