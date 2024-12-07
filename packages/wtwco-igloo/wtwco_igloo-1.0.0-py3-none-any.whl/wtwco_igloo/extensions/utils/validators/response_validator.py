from http import HTTPStatus
from typing import Any, Type, TypeVar, Union, cast

from wtwco_igloo.api_client.models import (
    CalculationPool,
    CalculationPoolArrayResponse,
    DataGroup,
    DataGroupArrayResponse,
    DataTableNode,
    DataTableNodeArrayResponse,
    DeleteRunResult,
    DeleteRunResultResponse,
    InputData,
    InputDataResponse,
    JobResponse,
    ModelArrayResponse,
    OutputData,
    OutputDataResponse,
    ProjectArrayResponse,
    ProjectResponse,
    RunArrayResponse,
    RunResponse,
    TableData,
    TableDataResponse,
    Upload,
    UploadedFile,
    UploadedFileResponse,
    UploadResponse,
)
from wtwco_igloo.api_client.models import (
    Job as ClientJob,
)
from wtwco_igloo.api_client.models import (
    Model as ClientModel,
)
from wtwco_igloo.api_client.models import (
    Project as ClientProject,
)
from wtwco_igloo.api_client.models import (
    Run as ClientRun,
)
from wtwco_igloo.api_client.types import Response
from wtwco_igloo.extensions.utils.errors.connection_errors import UnsuccessfulRequestError
from wtwco_igloo.extensions.utils.errors.wtwco_igloo_errors import UnexpectedResponseError, _log_and_get_exception

T = TypeVar(
    "T",
    bound=Union[
        CalculationPoolArrayResponse,
        DataGroupArrayResponse,
        DataTableNodeArrayResponse,
        ModelArrayResponse,
        ProjectArrayResponse,
        ProjectResponse,
        RunArrayResponse,
        RunResponse,
        JobResponse,
        OutputDataResponse,
        TableDataResponse,
        InputDataResponse,
        DeleteRunResultResponse,
        UploadedFileResponse,
        UploadResponse,
    ],
)
X = TypeVar(
    "X",
    bound=Union[
        ClientJob,
        ClientModel,
        ClientProject,
        CalculationPool,
        ClientRun,
        DataTableNode,
        OutputData,
        TableData,
        InputData,
        DeleteRunResult,
        DataGroup,
        UploadedFile,
        Upload,
    ],
)


class _ResponseValidator:
    @staticmethod
    def _check_response_is_valid(response: Response[Any]) -> None:
        if response.status_code not in [
            HTTPStatus.OK,
            HTTPStatus.CREATED,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NON_AUTHORITATIVE_INFORMATION,
            HTTPStatus.NO_CONTENT,
        ]:
            raise _log_and_get_exception(
                UnsuccessfulRequestError, "Request unsuccessful.", response.status_code, f"{response.content.decode()}"
            )

    @classmethod
    def _validate_response(
        cls,
        response: Response[Union[Any, T, Any]],
        expected_parsed_type: Type[T],
        expected_result_type: Type[X],
    ) -> Any:
        cls._check_response_is_valid(response)
        return cls._validate_response_type(response, expected_parsed_type, expected_result_type)

    @classmethod
    def _validate_response_type(
        cls,
        response: Response[Union[Any, T, Any]],
        parsed_expected_type: Type[T],
        result_expected_type: Type[X],
    ) -> Any:
        if isinstance(response.parsed, parsed_expected_type):
            return cls._validate_result_type(response.parsed, result_expected_type)
        raise _log_and_get_exception(
            UnexpectedResponseError,
            f"Unexpected parsed response type {type(response.parsed)}; expected {parsed_expected_type}",
        )

    @staticmethod
    def _validate_result_type(parsed_response: T, result_expected_type: Type[X]) -> Any:
        if isinstance(parsed_response.result, list):
            if isinstance(parsed_response.result[0], dict):
                return _handle_v2_api(cast(list[dict], parsed_response.result))
            elif isinstance(parsed_response.result[0], result_expected_type):
                return parsed_response.result
            else:
                raise _log_and_get_exception(
                    UnexpectedResponseError,
                    f"Unexpected result item type: got {type(parsed_response.result[0])}, expected {result_expected_type}",
                )
        elif isinstance(parsed_response.result, result_expected_type):
            return parsed_response.result
        else:
            raise _log_and_get_exception(
                UnexpectedResponseError,
                f"Unexpected result type: got {type(parsed_response.result)}, expected {result_expected_type}",
            )


def _handle_v2_api(parsed_response_result: list[dict]) -> list[Union[DataGroup, TableData]]:
    # Handle v2 API: Remove 'ownerRunIfNotOwned' key from data group dictionary if None or 'readOnlyReason' key from table data dictionary if None
    key_to_remove, data_class = _get_key_and_data_class(parsed_response_result)
    for data_group_dict in parsed_response_result:
        _remove_key_if_none(key_to_remove, data_group_dict)
    return [data_class.from_dict(data_group_dict) for data_group_dict in parsed_response_result]


def _get_key_and_data_class(parsed_response_result: list[dict]) -> tuple[str, Union[Type[DataGroup], Type[TableData]]]:
    data_class: Union[Type[DataGroup], Type[TableData]]
    if "ownerRunIfNotOwned" in parsed_response_result[0]:
        key_to_remove, data_class = "ownerRunIfNotOwned", DataGroup
    elif "readOnlyReason" in parsed_response_result[0]:
        key_to_remove, data_class = "readOnlyReason", TableData
    else:
        raise _log_and_get_exception(
            UnexpectedResponseError,
            "Unexpected result item type: got dictionary, but no expected key found",
        )

    return key_to_remove, data_class


def _remove_key_if_none(key_to_remove: str, data_group_dict: dict) -> None:
    if data_group_dict[key_to_remove] is None:
        del data_group_dict[key_to_remove]
