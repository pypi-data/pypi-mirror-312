from typing import TYPE_CHECKING

from wtwco_igloo.api_client.api.jobs import get_job
from wtwco_igloo.api_client.models import Job as ClientJob
from wtwco_igloo.api_client.models import JobResponse, JobState, JobStatus
from wtwco_igloo.extensions.utils.errors.wtwco_igloo_errors import UnexpectedResponseError, _log_and_get_exception
from wtwco_igloo.extensions.utils.validators.response_validator import _ResponseValidator

if TYPE_CHECKING:
    from wtwco_igloo import Connection, Run


class Job(object):
    """Represents a job in Igloo Cloud.

    Attributes:
        id (int): Identifier value of the job.
        run (Run): Run object associated with the job.
    """

    def __init__(self, job_dict: dict, connection: "Connection", run: "Run") -> None:
        self.id: int = job_dict["id"]
        self.Run = run
        self._connection = connection
        self._validate_response = _ResponseValidator._validate_response

    def __str__(self) -> str:
        return f"id: {self.id}, run: {self.Run.name}"

    def get_state(self) -> JobState:
        """Returns the job's state.

        Returns:
            State of the job. The following states are possible

            ``CANCELLATIONREQUESTED, CANCELLED, COMPLETED, ERROR, INPROGRESS, WARNED``

        Raises:
            UnsuccessfulRequestError: API response was not successful.
            UnexpectedResponseError: An unexpected API response was received.
        """
        response = get_job.sync_detailed(job_id=self.id, client=self._connection._get_authenticated_client())
        job_result: ClientJob = self._validate_response(response, JobResponse, ClientJob)

        if isinstance(job_result.status, JobStatus):
            if isinstance(job_result.status.state, JobState):
                return job_result.status.state

        raise _log_and_get_exception(
            UnexpectedResponseError, f"Job status could not be retrieved: {job_result.to_dict()}"
        )
