from asyncio import AbstractEventLoop
from typing import TYPE_CHECKING, Any, Optional, Union, cast

from wtwco_igloo.api_client import AuthenticatedClient
from wtwco_igloo.api_client.api.calculation_pools import get_calculation_pools
from wtwco_igloo.api_client.api.models import get_models
from wtwco_igloo.api_client.api.projects import create_project, get_projects
from wtwco_igloo.api_client.models import (
    CalculationPool,
    CalculationPoolArrayResponse,
    CreateProject,
    ModelArrayResponse,
    ModelVersion,
    ProjectArrayResponse,
    ProjectResponse,
)
from wtwco_igloo.api_client.models import (
    Model as ClientModel,
)
from wtwco_igloo.api_client.models import (
    Project as ClientProject,
)
from wtwco_igloo.extensions.utils.authentication.authentication_with_refresh import (
    _AuthenticationManagerWithRefresh,
)
from wtwco_igloo.extensions.utils.authentication.authentication_without_refresh import (
    _AuthenticationManagerWithoutRefresh,
)
from wtwco_igloo.extensions.utils.errors.model_errors import ModelNotFoundError
from wtwco_igloo.extensions.utils.errors.project_errors import ProjectNotFoundError, ProjectParameterError
from wtwco_igloo.extensions.utils.errors.wtwco_igloo_errors import _log_and_get_exception
from wtwco_igloo.extensions.utils.helpers import _standardise_url
from wtwco_igloo.extensions.utils.uploader import _Uploader
from wtwco_igloo.extensions.utils.validators.response_validator import _ResponseValidator
from wtwco_igloo.logger import logger

if TYPE_CHECKING:
    from wtwco_igloo import Model, Project


class Connection(object):
    """Handles connecting to the WTW Igloo Cloud and initial functionality.

    Connection class is constructed via the class methods from_device_code, from_interactive_token, from_certificate,
    and from_secret. The class methods are used to authenticate and create a Connection object.

    Attributes:
        web_app_url (str): Igloo Cloud Web App URL.
    """

    def __init__(
        self,
        authentication_manager: Union[_AuthenticationManagerWithoutRefresh, _AuthenticationManagerWithRefresh],
        run_processing_minutes: int,
        event_loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        self.web_app_url: str = _standardise_url(authentication_manager._api_url, "/manager/projects/")
        self._authentication_manager = authentication_manager
        self._models: list["Model"] = []
        self._uploader = _Uploader(authentication_manager, event_loop)
        self._run_processing_minutes = run_processing_minutes
        self._validate_response = _ResponseValidator._validate_response
        self._import_classes()

    def __enter__(self) -> "Connection":
        self._uploader.__enter__()
        return self

    def __exit__(self) -> None:
        self._uploader.__exit__()

    def __str__(self) -> str:
        return self.web_app_url

    @classmethod
    def from_certificate(
        cls,
        api_url: str,
        client_id: str,
        thumbprint: str,
        certificate_path: str,
        tenant_id: str,
        run_processing_minutes: int = 15,
        refresh_connection: bool = False,
    ) -> "Connection":
        """Connect to Igloo Cloud using a certificate.

        Args:
            api_url: Igloo Cloud API URL
            client_id: App registration GUID.
            thumbprint: Certificate thumbprint.
            certificate_path: Path to .pem certificate file.
            tenant_id: Tenant GUID.
            run_processing_minutes: Maximum time to wait for runs to process. Defaults to 15 minutes.
            refresh_connection: If True, the connection will automatically refresh. Defaults to False.

        Returns:
            An authenticated connection to Igloo Cloud.

        Raises:
            AuthenticationError: Failed to authenticate.
        """
        authentication_manager = (
            _AuthenticationManagerWithRefresh(api_url, client_id, tenant_id)
            if refresh_connection
            else _AuthenticationManagerWithoutRefresh(api_url, client_id, tenant_id)
        )
        authentication_manager._from_certificate(thumbprint, certificate_path)

        return cls(authentication_manager, run_processing_minutes)

    @classmethod
    def from_device_code(
        cls,
        api_url: str,
        client_id: str,
        tenant_id: str,
        run_processing_minutes: int = 15,
        refresh_connection: bool = False,
        **kwargs: bool,
    ) -> "Connection":
        """Connect to Igloo Cloud using device code flow.

        After connecting your device will be remembered for future connections.

        Args:
            api_url: Igloo Cloud API URL
            client_id: App registration GUID.
            tenant_id: Tenant GUID.
            run_processing_minutes: Maximum time to wait for runs to process. Defaults to 15 minutes.
            refresh_connection: If True, the connection will automatically refresh. Defaults to False.
            **kwargs: Additional keyword arguments used for testing only.

        Returns:
            An authenticated connection to Igloo Cloud.

        Raises:
            AuthenticationError: Failed to authenticate.
        """
        authentication_manager = (
            _AuthenticationManagerWithRefresh(api_url, client_id, tenant_id)
            if refresh_connection
            else _AuthenticationManagerWithoutRefresh(api_url, client_id, tenant_id)
        )
        authentication_manager._from_device_code(**kwargs)

        return cls(authentication_manager, run_processing_minutes)

    @classmethod
    def from_interactive_token(
        cls,
        api_url: str,
        client_id: str,
        tenant_id: str,
        run_processing_minutes: int = 15,
        refresh_connection: bool = False,
        **kwargs: bool,
    ) -> "Connection":
        """Connect to Igloo Cloud using interactive token.

        After connecting your device will be remembered for future connections.

        Args:
            api_url: Igloo Cloud API URL
            client_id: App registration GUID.
            tenant_id: Tenant GUID.
            run_processing_minutes: Maximum time to wait for runs to process. Defaults to 15 minutes.
            refresh_connection: If True, the connection will automatically refresh. Defaults to False.
            **kwargs: Additional keyword arguments used for testing only.

        Returns:
            An authenticated connection to Igloo Cloud.

        Raises:
            AuthenticationError: Failed to authenticate.
        """
        authentication_manager = (
            _AuthenticationManagerWithRefresh(api_url, client_id, tenant_id)
            if refresh_connection
            else _AuthenticationManagerWithoutRefresh(api_url, client_id, tenant_id)
        )
        authentication_manager._from_interactive_token(**kwargs)

        return cls(authentication_manager, run_processing_minutes)

    @classmethod
    def from_secret(
        cls,
        api_url: str,
        client_id: str,
        secret: str,
        tenant_id: str,
        run_processing_minutes: int = 15,
        refresh_connection: bool = False,
    ) -> "Connection":
        """Connect to Igloo Cloud using a secret.

        Args:
            api_url: Igloo Cloud API URL
            client_id: App registration GUID.
            secret: Secret for authenticating with tenant.
            tenant_id: Tenant GUID.
            run_processing_minutes: Maximum time to wait for runs to process. Defaults to 15 minutes.
            refresh_connection: If True, the connection will automatically refresh. Defaults to False.

        Returns:
            An authenticated connection to Igloo Cloud.

        Raises:
            AuthenticationError: Failed to authenticate.
        """
        authentication_manager = (
            _AuthenticationManagerWithRefresh(api_url, client_id, tenant_id)
            if refresh_connection
            else _AuthenticationManagerWithoutRefresh(api_url, client_id, tenant_id)
        )
        authentication_manager._from_secret(secret)

        return cls(authentication_manager, run_processing_minutes)

    def create_project(
        self,
        project_name: str,
        description: str = "",
        model_version_id: int = 0,
        source_run_id: Optional[int] = None,
        source_project_id: Optional[int] = None,
    ) -> "Project":
        """Creates a new project.

        Args:
            project_name: Name of the project to create. Maximum of 100 characters and must be unique.
            description: A description of the project. Defaults to "".
            model_version_id: Id of model to use in this project. Defaults to 0. Note that it's not possible to change
                the model associated with a project after creation.
            source_run_id: Id of run to initialise the first run of the new project. Defaults to None. The source run
                must associated with a compatible model. Compatible meaning it the models share the same name. Models
                with the same name but different versions are also compatible.
            source_project_id: Id of project to copy. As with the source run a source project must be associated with a
                compatible model. Defaults to None.

        Returns:
            Newly created project.

        Raises:
            ProjectParameterError: source_run_id and source_project_id are both set.
            UnsuccessfulRequestError: API response was not successful.
            UnexpectedResponseError: An unexpected API response was received.
        """
        if source_project_id and source_run_id:
            raise _log_and_get_exception(ProjectParameterError, "Can not set both source_run_id and source_project_id.")

        project_to_create = CreateProject(
            name=project_name,
            description=description,
            model_version_id=model_version_id,
        )
        if source_run_id:
            project_to_create.source_run_id = source_run_id
        if source_project_id:
            project_to_create.source_project_id = source_project_id

        response = create_project.sync_detailed(client=self._get_authenticated_client(), body=project_to_create)
        raw_project: ClientProject = self._validate_response(response, ProjectResponse, ClientProject)
        logger.info(f"Project {project_name} was successfully created.")

        return Project(self, raw_project.to_dict())

    def delete_files(self, *file_ids: int) -> None:
        """Deletes specified files from Igloo Cloud.

        Args:
            *file_ids: Variable length argument list of file ids to delete.

        Raises:
            UnsuccessfulRequestError: API response was not successful.
        """
        self._uploader._delete_files(file_ids)

    def get_calculation_pools(self) -> list[dict[str, Any]]:
        """Retrieves the list of calculation pools available to the API.

        Returns:
            List of calculation pools.

        Raises:
            UnsuccessfulRequestError: API response was not successful.
            UnexpectedResponseError: An unexpected API response was received.
        """
        response = get_calculation_pools.sync_detailed(client=self._get_authenticated_client())
        calculation_pools: list[CalculationPool] = self._validate_response(
            response, CalculationPoolArrayResponse, CalculationPool
        )
        return [pool.to_dict() for pool in calculation_pools]

    def get_models(self) -> list["Model"]:
        """Retrieves the list of models available to the API.

        Returns:
            List of available models.

        Raises:
            UnsuccessfulRequestError: API response was not successful.
            UnexpectedResponseError: An unexpected API response was received.
        """
        response = get_models.sync_detailed(client=self._get_authenticated_client())
        raw_models: list[ClientModel] = self._validate_response(response, ModelArrayResponse, ClientModel)
        return [
            Model(
                {
                    "model_name": raw_model.name,
                    "version_name": version.name,
                    "id": version.id,
                },
                self,
            )
            for raw_model in raw_models
            for version in cast(list[ModelVersion], raw_model.versions)
        ]

    def get_model(self, model_name: str, version_name: str) -> "Model":
        """Retrieves model with the given name and version.

        Args:
            model_name: Name of model to return.
            version_name: Version name of the model to return.

        Returns:
            The requested model.

        Raises:
            ModelNotFoundError: Requested model was not found.
            UnsuccessfulRequestError: API response was not successful.
            UnexpectedResponseError: An unexpected API response was received.
        """
        for model in self.get_models():
            if model.model_name == model_name and model.version_name == version_name:
                return model
        raise _log_and_get_exception(ModelNotFoundError, f"Model {model_name} not found.")

    def get_projects(self) -> list["Project"]:
        """Retrieves the list of projects available to the API.

        Returns:
            List of available projects.

        Raises:
            UnsuccessfulRequestError: API response was not successful.
            UnexpectedResponseError: An unexpected API response was received.
        """
        response = get_projects.sync_detailed(client=self._get_authenticated_client())
        raw_projects: list[ClientProject] = self._validate_response(response, ProjectArrayResponse, ClientProject)
        return [Project(self, proj.to_dict()) for proj in raw_projects]

    def get_project(self, project_name: str) -> "Project":
        """Retrieves the project with the given name.

        Args:
            project_name: Name of project to return.

        Returns:
            Project with the given name.

        Raises:
            ProjectNotFoundError: Project with the given name was not found.
            UnsuccessfulRequestError: API response was not successful.
            UnexpectedResponseError: An unexpected API response was received.
        """
        projects = self.get_projects()
        for project in projects:
            if project.name == project_name:
                return project
        raise _log_and_get_exception(ProjectNotFoundError, f"Project {project_name} not found.")

    def upload_folder(self, folder_path: str, folder_description: str = "") -> dict[str, int]:
        """Uploads all csv files in a folder to Igloo Cloud. Returns a dictionary of file names to file ids.

        Args:
            folder_path: Path to directory containing csv files to upload.
            folder_description: Describes the files in the folder. Defaults to "". Note the description is applied to
                each file within the folder.

        Returns:
            Map of uploaded file names to their file ids.

        Raises:
            FolderNotFoundError: Given folder path is not an existing directory.
            FileNotFoundError: No files were found in the folder.
            NonCsvFileError: Only csv files are accepted.
            UnsuccessfulRequestError: API response was not successful.
            UnexpectedResponseError: An unexpected API response was received.
        """
        return self._uploader._upload_folder(folder_path, folder_description=folder_description)

    def upload_files(self, *files_and_descriptions: Union[str, tuple[str, str]]) -> dict[str, int]:
        """Uploads files to Igloo Cloud. Returns a dictionary of file names to file ids.

        If multiple files with the same base names are uploaded, the shared folder will be the common path of all files.

        Args:
            files_and_descriptions: Files to upload to Igloo Cloud and related
                descriptions. Descriptions default to empty strings if they are not provided.

        Returns:
            Map of uploaded file names to their file ids.

        Raises:
            FileNotFoundError: One or more of the files were not found.
            NonCsvFileError: Only csv files are accepted.
            UnsuccessfulRequestError: API response was not successful.
            UnexpectedResponseError: An unexpected API response was received.
        """
        return self._uploader._upload_files(list(files_and_descriptions))

    def _get_model_id(self, copy_model: "Model") -> int:
        for m in self.get_models():
            if m.version_name == copy_model.version_name and m.model_name == copy_model.model_name:
                return m.id
        raise _log_and_get_exception(ModelNotFoundError, f"Model {copy_model} not found in target connection.")

    def _validate_model_version(self, model_version_id: int) -> int:
        if any(m.id == model_version_id for m in self.get_models()):
            return model_version_id
        raise _log_and_get_exception(ModelNotFoundError, f"Model {model_version_id} not found in target connection.")

    def _clean_up(self) -> None:
        self._uploader._delete_all_files()

    def _get_authenticated_client(self) -> AuthenticatedClient:
        return self._authentication_manager._get_authenticated_client()

    @staticmethod
    def _import_classes() -> None:
        """Import classes to avoid circular imports."""
        global Model, Project
        from wtwco_igloo import Model, Project
