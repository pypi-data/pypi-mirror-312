import warnings

from trail.userconfig.search_config_file import find_config_file_in_directory_hierarchy

# Suppress all warnings -- mlflow produces ugly pydantic warnings rn
warnings.filterwarnings("ignore")

import inspect
import os.path
import signal
import time
from collections import defaultdict
from typing import Union
import requests


import mlflow
import sentry_sdk
from mlflow.entities import Run
from mlflow.tracking import MlflowClient

from trail.exception.trail import RemoteTrailException, TrailUnavailableException
from trail.libconfig import is_development_environment, libconfig
from trail.userconfig import userconfig
from trail.util import uploads
from trail.util.gql_client import build_gql_client
from gql.transport.exceptions import TransportServerError

FALLBACK_CONTENT_TYPE = "application/octet-stream"


class Trail:
    ADD_EXPERIMENT_MUTATION = """
        mutation (
            $projectId: String!,
            $parentExperimentId: String!,
            $title: String!,
            $comments: String!,
            $instanceRunParameters: GenericScalar!,
            $instanceRunMetrics: GenericScalar!,
            $instanceRunComplete: Boolean!
            $hypothesis: String,
            $metricsHistoryEntries: [MetricsHistoryInput],
            $gitCommitHash: String
        ) {
            addExperiment(
                projectId: $projectId,
                parentExperimentId: $parentExperimentId,
                title: $title,
                comments: $comments,
                hypothesis: $hypothesis
                metricsHistory: $metricsHistoryEntries
                gitCommitHash: $gitCommitHash
                instanceRuns: {
                    comment: "",
                    parameters: $instanceRunParameters,
                    metrics: $instanceRunMetrics,
                    isComplete: $instanceRunComplete
                }
            ) {
                experiment {
                    id
                    title
                    comments
                    instanceRuns {
                        id
                        comment
                        parameters
                        metrics
                        isComplete
                    }
                }
            }
        }
    """
    UPDATE_EXPERIMENT_MUTATION = """
            mutation (
                $experimentId: String!,
                $title: String!,
                $comments: String!,
                $instanceRunParameters: GenericScalar!,
                $instanceRunMetrics: GenericScalar!,
                $instanceRunComplete: Boolean!
                $hypothesis: String,
                $metricsHistoryEntries: [MetricsHistoryInput],
                $gitCommitHash: String
            ) {
                updateExperiment(
                    experimentId: $experimentId,
                    title: $title,
                    comments: $comments,
                    hypothesis: $hypothesis
                    metricsHistory: $metricsHistoryEntries
                    gitCommitHash: $gitCommitHash
                    instanceRuns: {
                        comment: "",
                        parameters: $instanceRunParameters,
                        metrics: $instanceRunMetrics,
                        isComplete: $instanceRunComplete
                    }
                ) {
                    experiment {
                        id
                        title
                        comments
                        instanceRuns {
                            id
                            comment
                            parameters
                            metrics
                            isComplete
                        }
                    }
                }
            }
        """

    PUT_ARTIFACT_MUTATION = """
        mutation (
            $experimentId: String!,
            $name: String!,
            $size: Int!,
            $contentType: String!,
            $tags: [String!],
            $callSiteKey: String,
        ) {
            putArtifact(
                experimentId: $experimentId,
                name: $name,
                size: $size,
                contentType: $contentType,
                tags: $tags,
                callSiteKey: $callSiteKey
            ) {
                artifact {
                    id
                    name
                    contentType
                    size
                    tags
                    callSiteKey
                }
                presignedUrl
            }
        }
    """

    YDATA_PROFILING_TAG = "TRAIL_YDATA_DATASET_PROFILE"
    TRAIL_PACKAGE_NAME = "trail"

    def __init__(
        self,
        experiment_title="Unnamed Run",
        experiment_id=None,
        parent_experiment_id=None,
        project_id=None,
    ):
        userconfig().merge(
            project_id=project_id,
            parent_experiment_id=parent_experiment_id,
        )

        self._project_config = userconfig().project()
        self._project_id = self._project_config.id
        self._experiment_id = experiment_id
        self._parent_experiment_id = self._project_config.parent_experiment_id
        self._experiment_title = experiment_title
        self._artifacts = []
        self._default_sigint_handler = signal.getsignal(signal.SIGINT)
        self._is_complete = True
        self._hypothesis = ""

        self.__client = None
        self._last_client_creation_time = 0

    def _sigint_handler(self, _signum, _frame):
        self._is_complete = False
        print("Latest run is logged.")

        raise KeyboardInterrupt()

    def __enter__(self):
        if mlflow.active_run() is None:
            raise RuntimeError("No active MLflow run found!")
        signal.signal(signal.SIGINT, self._sigint_handler)

        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        run = mlflow.active_run()
        if run is None:
            raise RuntimeError("No active mlflow run found!")

        # we fetch the run like this because of
        # https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.active_run
        materialized_run = mlflow.get_run(run_id=run.info.run_id)

        if materialized_run:
            self._log_experiment(materialized_run)
            self._upload_artifacts(materialized_run)
        signal.signal(signal.SIGINT, self._default_sigint_handler)

    @property
    def _client(self):
        current_time = time.time()

        if not self.__client:
            self._last_client_creation_time = current_time
            return build_gql_client()

        return self.__client

    def _execute(
        self, query: str, variable_values: dict, error_message: Union[str, None] = None
    ):
        try:
            return self._client.execute(
                query=query,
                variable_values=variable_values,
            )
        except (TransportServerError, Exception) as e:
            if not is_development_environment():
                sentry_sdk.capture_exception(e)

            if isinstance(e, TransportServerError):
                if e.code == 403:
                    raise RemoteTrailException(
                        "Access forbidden. Please check your authentication credentials."
                    ) from e
                elif e.code == 401:
                    raise RemoteTrailException(
                        "Unauthorized. Please check your authentication credentials."
                    ) from e
                elif e.code == 404:
                    raise RemoteTrailException("Resource not found.") from e
                elif e.code is not None and e.code >= 500:
                    raise RemoteTrailException(
                        "Server error. Please try again later."
                    ) from e

                raise RemoteTrailException(
                    f"Server returned status code {e.code}"
                ) from e

            if error_message:
                raise RemoteTrailException(error_message) from e
            raise TrailUnavailableException() from e

    def _log_experiment(self, run: Run):
        run_id = run.info.run_id
        tags = {k: v for k, v in run.data.tags.items() if not k.startswith("mlflow.")}
        mlflow_artifacts = [
            artifact.path for artifact in MlflowClient().list_artifacts(run_id, "model")
        ]
        d = {  # noqa: F841
            "run_id": run_id,
            "timestamp": run.info.start_time / 1000.0,
            "user": run.info.user_id,
            "artifacts": mlflow_artifacts,
            "tags": tags,
        }
        # Convert numeric parameter values to their respective types
        converted_params = run.data.params.copy()
        for key, value in converted_params.items():
            try:
                converted_params[key] = float(value)
            except ValueError as e:
                sentry_sdk.capture_exception(e)
        variable_values = {
            "title": self._experiment_title,
            "comments": "",
            "instanceRunParameters": converted_params,
            "instanceRunMetrics": run.data.metrics,
            "instanceRunComplete": self._is_complete,
            "hypothesis": self._hypothesis,
            "gitCommitHash": run.data.tags.get("mlflow.source.git.commit", ""),
            "metricsHistoryEntries": self._get_metric_history_data(run_id=run_id),
        }
        if self._experiment_id:
            variable_values["experimentId"] = self._experiment_id
            query = self.UPDATE_EXPERIMENT_MUTATION
            mutation_name = "updateExperiment"
        else:
            query = self.ADD_EXPERIMENT_MUTATION
            variable_values["projectId"] = self._project_id
            variable_values["parentExperimentId"] = self._parent_experiment_id
            mutation_name = "addExperiment"

        result = self._execute(
            query=query,
            variable_values=variable_values,
        )
        if result:
            experiment_id = result[mutation_name]["experiment"]["id"]
            self._project_config.update_parent_experiment_id(experiment_id)
            self._parent_experiment_id = experiment_id

    @staticmethod
    def _get_metric_history_data(run_id):
        client = mlflow.tracking.MlflowClient()
        run = mlflow.active_run()
        mlflow_run = mlflow.get_run(run_id=run.info.run_id)
        metric_list = list(mlflow_run.data.metrics.keys())
        metrics = defaultdict(list)
        for metric in metric_list:
            metric_history = client.get_metric_history(run_id, metric)
            for entry in metric_history:
                metric_name = entry.key
                data_point = {
                    "value": entry.value,
                    "timeStamp": str(entry.timestamp),
                    "step": entry.step,
                }
                metrics[metric_name].append(data_point)

        metrics_history = []
        for metric in metrics:
            metrics_history.append({"metricName": metric, "history": metrics[metric]})

        return metrics_history

    def _upload_artifact(self, data: bytes, name: str, tags: list, call_site_key: str):
        """Upload an artifact using presigned URL.

        Args:
            data: Raw bytes of the artifact
            name: Name of the artifact
            tags: List of tags to apply
            call_site_key: Call site identifier
        """
        import mimetypes

        content_type, _ = mimetypes.guess_type(name)
        if content_type is None:
            content_type = FALLBACK_CONTENT_TYPE

        result = self._execute(
            query=self.PUT_ARTIFACT_MUTATION,
            variable_values={
                "experimentId": self._parent_experiment_id,
                "name": name,
                "size": len(data),
                "contentType": content_type,
                "tags": tags,
                "callSiteKey": call_site_key,
            },
            error_message="Error getting presigned URL for artifact upload.",
        )
        presigned_url = result["putArtifact"]["presignedUrl"]

        response = requests.put(
            presigned_url,
            data=data,
            headers={"Content-Type": content_type, "Content-Length": str(len(data))},
        )

        if response.status_code != 200:
            raise RemoteTrailException(
                f"Failed to upload artifact to storage. Status: {response.status_code}"
            )

    def _create_temp_zip(self, source_dir: str) -> tuple[str, str]:
        """Creates a temporary zip file from a directory.

        Args:
            source_dir: Path to the directory to zip

        Returns:
            Tuple of (path to zip file, base name of zip file)
        """
        import tempfile
        import shutil

        tmp_zip = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
        zip_path = tmp_zip.name
        tmp_zip.close()

        # Create zip archive (removing .zip suffix as make_archive adds it)
        shutil.make_archive(zip_path[:-4], "zip", source_dir)
        return zip_path, os.path.basename(source_dir) + ".zip"

    def _upload_single_artifact(
        self, file_path: str, artifact_name: str, additional_tags: list[str] = None
    ):
        """Uploads a single file as an artifact.

        Args:
            file_path: Path to the file to upload
            artifact_name: Name to give the artifact
            additional_tags: Optional list of additional tags to apply
        """
        tags = ["mlflow"]
        if additional_tags:
            tags.extend(additional_tags)

        with open(file_path, "rb") as f:
            data = f.read()
            self._upload_artifact(
                data=data,
                name=artifact_name,
                tags=tags,
                call_site_key="",
            )

    def _handle_directory_artifact(self, artifact_location: str, artifact_name: str):
        """Handles uploading a directory artifact by zipping it first.

        Args:
            artifact_location: Path to the directory
            artifact_name: Original name of the artifact
        """
        zip_path, zip_name = self._create_temp_zip(artifact_location)
        try:
            with open(zip_path, "rb") as f:
                data = f.read()
                self._upload_artifact(
                    data=data,
                    name=zip_name,
                    tags=["mlflow", "zipped_directory"],
                    call_site_key="",
                )
        finally:
            # Clean up temporary zip file
            os.unlink(zip_path)

    def _upload_artifacts(self, run: Run):
        run_id = run.info.run_id

        # upload cached artifacts
        client = MlflowClient()
        mlflow_artifacts = client.list_artifacts(run_id, "model")

        for artifact in mlflow_artifacts:
            # Get the full local filesystem path where MLflow stored the artifact
            # Note: download_artifacts() doesn't actually download anything when using local MLflow tracking
            artifact_location = client.download_artifacts(run_id, artifact.path)

            try:
                if os.path.isdir(artifact_location):
                    self._handle_directory_artifact(
                        artifact_location, os.path.basename(artifact.path)
                    )
                else:
                    self._upload_single_artifact(
                        artifact_location, os.path.basename(artifact.path)
                    )
            except FileNotFoundError:
                warnings.warn(
                    f"Artifact {artifact_location} not found on disk, skipping upload."
                )
                continue

    def _get_user_call_site_key(self):
        """
        returns the filename and line number of the first frame outside the trail package
        """
        config_path = find_config_file_in_directory_hierarchy()
        config_dir = os.path.dirname(os.path.dirname(config_path))
        for frame_info in inspect.stack():
            module_name = frame_info.frame.f_globals.get("__name__", "")
            if not module_name.startswith(self.TRAIL_PACKAGE_NAME):
                relative_filename = os.path.relpath(frame_info.filename, config_dir)
                return f"{relative_filename}:{frame_info.lineno}"

    @property
    def project_id(self):
        return self._project_id

    @property
    def parent_experiment_id(self):
        return self._parent_experiment_id

    def put_artifact(
        self, src: Union[str, bytes], name: str, tags: Union[str, list, None] = None
    ):
        """Queues an artifact for upload to Trail.
        The artifact is uploaded when leaving the `with Trail` block.
        The `src` parameter can be either a string or a bytes object. In case
        of a string, it is assumed to be a path to a file. In case of a bytes
        object, it is assumed to be the raw data of the artifact.

        :param src: The artifact path or bytes to upload
        :param name: The name of the artifact
        :param tags: A single tag or a list of tags
        """

        if isinstance(src, str):
            with open(src, "rb") as f:
                data = f.read()
        elif isinstance(src, bytes):
            data = src
        else:
            raise ValueError("Artifact source must be of type string or bytes.")

        if not tags:
            tags = []
        elif isinstance(tags, str):
            tags = [tags]

        self._artifacts.append(
            (
                data,
                name,
                tags,
                self._get_user_call_site_key(),
            )
        )

    def put_dataset_analysis(self, src: str, name: str):
        """
        Wrapper function for put_artifact that sets specific tags to mark
        the artifact as dataset profiling analysis.
        """
        self.put_artifact(src, name, [self.YDATA_PROFILING_TAG])

    def upload_folder(self, local_folder: str) -> None:
        """
        Uploads a folder to Trail. This path is relative to your working directory.
        :param local_folder:
        :return: None
        """
        uploads.upload_folder(local_folder)

    def put_hypothesis(self, hypothesis: str):
        self._hypothesis = hypothesis
