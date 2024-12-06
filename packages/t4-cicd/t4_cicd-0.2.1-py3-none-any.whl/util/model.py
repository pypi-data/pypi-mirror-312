"""
Common model class based on pydantic for easier validation and formating. 
"""
import time
from collections import OrderedDict
from typing import (Dict, Optional, Union)
from pydantic import (BaseModel, Field, field_validator)
import util.constant as c

class DockerConfig(BaseModel):
    """ class to hold configuration for a docker section 
    with registry and image

    Args:
        BaseModel (BaseModel): Base Pydantic Class
    """
    registry: str
    image: str

class ArtifactConfig(BaseModel):
    """ class to hold configuration for an artifact section

    Args:
        BaseModel (BaseModel): Base Pydantic Class
    """
    on_success_only: bool
    paths: list[str]

class JobConfig(BaseModel):
    """ class to hold configuration for a job

    Args:
        BaseModel (BaseModel): Base Pydantic Class
    """
    stage: str
    allow_failure: bool
    needs: list[str]
    docker: DockerConfig
    artifact_upload_path: Optional[str]
    scripts: list[str]
    artifacts: Optional[ArtifactConfig] = None

class JobLog(BaseModel):
    """ class to hold information for a single job

    Args:
        BaseModel (BaseModel): Base Pydantic Class
    """
    job_name: str
    job_status: Optional[str] = c.STATUS_FAILED
    allow_failure: bool
    start_time: str
    completion_time: Optional[str] = time.asctime()
    job_logs: Optional[str] = ""

class SessionDetail(BaseModel):
    """ class to hold information to identify a repo for pipeline run

    Args:
        BaseModel (BaseModel): Base Pydantic Class
    """
    user_id: str
    repo_name: str
    repo_url: str
    branch: str
    commit_hash: str
    is_remote: bool
    time: Optional[str] = time.asctime()

class GlobalConfig(BaseModel):
    """ class to hold information for a validated global section

    Args:
        BaseModel (BaseModel): Base Pydantic Class
    """
    pipeline_name: str
    docker: DockerConfig
    artifact_upload_path: str

class ValidatedStage(BaseModel):
    """ class to hold information for a Validated Stage in Stages Section

    Args:
        BaseModel (BaseModel): Base Pydantic Class
    """
    job_graph: dict
    job_groups: list[list]

class PipelineConfig(BaseModel):
    """ class to hold information for a valid pipeline configuration. 
    Note one of the keyword global is reserved in Python, thus we need 
    to load by alias='global', when output to dict / json, need to specify
    model_dump(byalias=True)

    Args:
        BaseModel (BaseModel): Base Pydantic Class
    """
    global_: GlobalConfig = Field(alias=c.KEY_GLOBAL)
    stages : OrderedDict
    jobs: dict

class RawPipelineInfo(BaseModel):
    """ class to hold information for a single pipeline 
    before pipeline config validations
    
    Args:
        BaseModel (BaseModel): Base Pydantic Class
    """
    pipeline_name: str
    pipeline_file_name: str
    pipeline_config: dict

class PipelineInfo(BaseModel):
    """ class to hold information for a single pipeline 
    Args:
        BaseModel (BaseModel): Base Pydantic Class
    """
    pipeline_name: str
    pipeline_file_name: str
    pipeline_config: PipelineConfig
    job_run_history: Optional[list] = []
    active: Optional[bool] = False
    running: Optional[bool] = False
    last_commit_hash: Optional[str] = ""

    @field_validator(c.FIELD_JOB_RUN_HISTORY)
    @classmethod
    def set_job_run_history(cls, job_run_history):
        """ validate the job_run_history field dynamically, 
        so if None value is supplied, or no value is supplied, 
        it will set to empty list

        Args:
            job_run_history (list): existing job_run_history

        Returns:
            list: existing list or new list
        """
        return job_run_history or []

class RepoConfig(BaseModel):
    """ Class to hold information correspond to one record 
    in repo_configs table

    Args:
        BaseModel (BaseModel): Base Pydantic Class
    """
    _id: Optional[any] = None
    repo_name: str
    repo_url: str
    branch: str
    pipelines: Optional[Dict[str,PipelineInfo]] = {}

class PipelineHist(BaseModel):
    """class to hold data to retrieve pipeline history

    Args:
        BaseModel (BaseModel): Base Pydantic Class
    """
    repo_name:str
    repo_url:str
    pipeline_name: Optional[str] = None
    branch: Optional[str] = c.DEFAULT_BRANCH
    stage: Optional[str] = None
    job: Optional[str] = None
    run: Optional[int] = None
    is_remote: Optional[bool] = False

class ValidationResult(BaseModel):
    """ class to hold validation result for a single pipeline 
    Args:
        BaseModel (BaseModel): Base Pydantic Class
    """
    valid: bool
    error_msg: str
    pipeline_config: Union[PipelineConfig, dict]
