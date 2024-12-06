import os

# Parsed argument keys
CREATE_JOB_WITH_UPLOAD = "create_job_with_upload"
DOWNLOAD_JOB_FILES = "download_job_files"
EXCLUDE_INPUT = "exclude_input"
EXCLUDE_OUTPUT = "exclude_output"
GET_JOB_CURRENT_STATUS = "get_job_current_status"
SILENCE = "silence"
INCLUDE_INPUT = "include_input"
INCLUDE_OUTPUT = "include_output"
JOB_CONFIG_FILE_PATH = "job_config_file_path"
JOB_FILE_ROOT_DIRECTORY = "job_file_root_directory"
JOB_ID = "job_id"
SYNC_JOB_FILES = "sync_job_files"
JOB_ID_LIST = "job_id_list"
JOB_NAME = "job_name"
OPEN_CONFIG_FOLDER = "open_config_folder"
TIMESTAMP = "timestamp"
DEBUG_MODE = "debug_mode"
UPLOAD_FILES = "upload_files"
FOVUS_PATH = "fovus_path"
LOCAL_PATH = "local_path"
LOGIN = "login"
GOV = "gov"
LOGOUT = "logout"
USER = "user"
DELETE_JOB = "delete_job"
MOUNT_STORAGE = "mount_storage"
WINDOWS_DRIVE = "windows_drive"
MOUNT_STORAGE_PATH = "mount_storage_path"
UNMOUNT_STORAGE = "unmount_storage"
LIVE_TAIL_FILE = "live_tail_file"
LIST_PROJECTS = "list_projects"
PROJECT_NAME = "project_name"

# Job config overrides
BENCHMARKING_PROFILE_ID = "benchmarkingProfileId"
BENCHMARKING_PROFILE_NAME = "benchmarkingProfileName"
COMPUTING_DEVICE = "computingDevice"
IS_SINGLE_THREADED_TASK = "isSingleThreadedTask"
LICENSE_TIMEOUT_HOURS = "licenseTimeoutHours"
MONOLITHIC_OVERRIDE = "monolithicOverride"
MIN_GPU = "minGpu"
MAX_GPU = "maxGpu"
AUTO_DELETE_DAYS = "autoDeleteDays"
MIN_GPU_MEM_GIB = "minGpuMemGiB"
JOB_MAX_CLUSTER_SIZE_VCPU = "jobMaxClusterSizevCpu"
MIN_VCPU = "minvCpu"
MAX_VCPU = "maxvCpu"
MIN_VCPU_MEM_GIB = "minvCpuMemGiB"
OUTPUT_FILE_LIST = "outputFileList"
OUTPUT_FILE_OPTION = "outputFileOption"
REMOTE_INPUTS = "remoteInputsForAllTasks"
PARALLELISM_CONFIG_FILES = "parallelismConfigFiles"
PARALLELISM_OPTIMIZATION = "parallelismOptimization"
RUN_COMMAND = "runCommand"
SCALABLE_PARALLELISM = "scalableParallelism"
SCALING_OUT = "scalingOut"
SCHEDULED_AT = "scheduledAt"
STORAGE_GIB = "storageGiB"
IS_SUBJECT_TO_AVAILABLE_RESOURCES = "isSubjectToAvailableResources"
ENABLE_HYPERTHREADING = "enableHyperthreading"
SUPPORTED_CPU_ARCHITECTURES = "supportedCpuArchitectures"
TIME_TO_COST_PRIORITY_RATIO = "timeToCostPriorityRatio"
WALLTIME_HOURS = "walltimeHours"
LICENSE_CONSUMPTION_PROFILE = "licenseConsumptionProfile"
POST_PROCESSING_WALLTIME_HOURS = "PostProcessingWalltimeHours"
POST_PROCESSING_STORAGE_GIB = "PostProcessingStorageGiB"
POST_PROCESSING_RUN_COMMAND = "PostProcessingRunCommand"
POST_PROCESSING_TASK_NAME = "PostProcessingTaskName"
EMPTY_FOLDER_LIST = "emptyFolderList"
ALLOW_PREEMPTIBLE = "allowPreemptible"
IS_RESUMABLE_WORKLOAD = "isResumableWorkload"
PROJECT_ID = "projectId"

# Development overrides
CLIENT_ID = "clientId"
DOMAIN_NAME = "domainName"
SKIP_CREATE_JOB_INFO_FOLDER = "skipCreateJobInfoFolder"
USER_POOL_ID = "userPoolId"
SSO_USER_POOL_ID = "ssoUserPoolId"
WORKSPACE_SSO_CLIENT_ID = "workspaceSsoClientId"
API_DOMAIN_NAME = "apiDomainName"
AUTH_WS_API_URL = "authWsApiUrl"
AWS_REGION = "awsRegion"

# Additional arguments (if required)
MONOLITHIC_OVERRIDE_ADDITIONAL_ARGUMENTS = {
    "default": [],
    "action": "append",
    "nargs": 4,
    "metavar": ("VENDOR_NAME", "SOFTWARE_NAME", "LICENSE_FEATURE", "NEW_LICENSE_COUNT"),
}

# Argument groups
BOOLEAN_ARGS = (
    SCALABLE_PARALLELISM,
    PARALLELISM_OPTIMIZATION,
    SCALING_OUT,
    IS_SUBJECT_TO_AVAILABLE_RESOURCES,
    ENABLE_HYPERTHREADING,
    IS_SINGLE_THREADED_TASK,
    ALLOW_PREEMPTIBLE,
    IS_RESUMABLE_WORKLOAD,
    GOV,
)

# CLI arguments
CLI_ARGUMENTS = {
    # Parsed argument keys
    DELETE_JOB: ("--delete-job", "--deleteJob", "-dj"),
    CREATE_JOB_WITH_UPLOAD: ("--create-job-with-upload", "--createJobWithUpload", "-cjwu"),
    DOWNLOAD_JOB_FILES: ("--download-job-files", "--downloadJobFiles", "-djf"),
    EXCLUDE_INPUT: ("--exclude-input", "--excludeInput", "-ei"),
    EXCLUDE_OUTPUT: ("--exclude-output", "--excludeOutput", "-eo"),
    GET_JOB_CURRENT_STATUS: ("--get-job-current-status", "--getJobCurrentStatus", "-gjcs"),
    SILENCE: ("--silence", "-s"),
    INCLUDE_INPUT: ("--include-input", "--includeInput", "-ii"),
    INCLUDE_OUTPUT: ("--include-output", "--includeOutput", "-io"),
    JOB_CONFIG_FILE_PATH: ("--job-config-file-path", "--jobConfigFilePath", "-jcfp"),
    JOB_FILE_ROOT_DIRECTORY: ("--job-file-root-directory", "--jobFileRootDirectory", "-jfrd"),
    OPEN_CONFIG_FOLDER: ("--open-config-folder", "--openConfigFolder", "-ocf"),
    DEBUG_MODE: ("--debug-mode", "--debugMode", "-dm"),
    UPLOAD_FILES: ("--upload-files", "--uploadFiles", "-uf"),
    FOVUS_PATH: ("--fovus-path", "--fovusPath", "-fp"),
    LOCAL_PATH: ("--local-path", "--localPath", "-lp"),
    LOGIN: ("--login", "-l"),
    GOV: ("--gov", "-g"),
    LOGOUT: ("--logout", "-lo"),
    USER: ("--user", "-u"),
    MOUNT_STORAGE: ("--mount-storage", "--mountStorage", "-ms"),
    WINDOWS_DRIVE: ("--windows-drive", "--windowsDrive", "-wd"),
    MOUNT_STORAGE_PATH: ("--mount-storage-path", "--mountStoragePath", "-msp"),
    UNMOUNT_STORAGE: ("--unmount-storage", "--unmountStorage", "-us"),
    LIVE_TAIL_FILE: ("--live-tail-file", "--liveTailFile", "-ltf"),
    # Job config overrides
    BENCHMARKING_PROFILE_ID: ("--benchmarking-profile-id", "--benchmarkingProfileId", "-bpi"),
    BENCHMARKING_PROFILE_NAME: ("--benchmarking-profile-name", "--benchmarkingProfileName", "-bpn"),
    COMPUTING_DEVICE: ("--computing-device", "--computingDevice", "-cd"),
    JOB_NAME: ("--job-name", "--jobName", "-jn"),
    JOB_ID: ("--job-id", "--jobId", "-jid"),
    JOB_ID_LIST: ("--job-id-list", "--jobIdList", "-jidl"),
    IS_SINGLE_THREADED_TASK: ("--is-single-threaded-task", "--isSingleThreadedTask", "-istt"),
    LICENSE_TIMEOUT_HOURS: ("--license-timeout-hours", "--licenseTimeoutHours", "-lth"),
    MONOLITHIC_OVERRIDE: ("--monolithic-override", "--monolithicOverride", "-mo"),
    MIN_GPU: ("--min-gpu", "--minGpu"),
    MAX_GPU: ("--max-gpu", "--maxGpu"),
    MIN_GPU_MEM_GIB: ("--min-gpu-mem-gib", "--minGpuMemGiB", "-mgpuMemGiB"),
    AUTO_DELETE_DAYS: ("--auto-delete-days", "--autoDeleteDays", "-add"),
    JOB_MAX_CLUSTER_SIZE_VCPU: ("--job-max-cluster-size-vcpu", "--jobMaxClusterSizevCpu", "-jmcs"),
    MIN_VCPU: ("--min-vcpu", "--minvCpu", "--min-cpu"),
    MAX_VCPU: ("--max-vcpu", "--maxvCpu", "--max-cpu"),
    MIN_VCPU_MEM_GIB: ("--min-vcpu-mem-gib", "--minvCpuMemGiB", "-mvcpuMemGiB"),
    OUTPUT_FILE_LIST: ("--output-file-list", "--outputFileList", "-ofl"),
    OUTPUT_FILE_OPTION: ("--output-file-option", "--outputFileOption", "-ofo"),
    REMOTE_INPUTS: ("--remote-inputs-for-all-tasks", "--remoteInputsForAllTasks", "--remote-inputs", "-ri"),
    PARALLELISM_CONFIG_FILES: ("--parallelism-config-files", "--parallelismConfigFiles", "-pcf"),
    PARALLELISM_OPTIMIZATION: ("--parallelism-optimization", "--parallelismOptimization", "-po"),
    RUN_COMMAND: ("--run-command", "--runCommand", "-rc"),
    SCALABLE_PARALLELISM: ("--scalable-parallelism", "--scalableParallelism", "-sp"),
    SCALING_OUT: ("--scaling-out", "--scalingOut", "-so"),
    SCHEDULED_AT: ("--scheduled-at", "--scheduledAt", "-sa"),
    STORAGE_GIB: ("--storage-gib", "--storageGiB", "-sgib"),
    IS_SUBJECT_TO_AVAILABLE_RESOURCES: (
        "--is-subject-to-available-resources",
        "--isSubjectToAvailableResources",
        "-istar",
    ),
    ALLOW_PREEMPTIBLE: ("--allow-preemptible", "--allowPreemptible", "-ap"),
    IS_RESUMABLE_WORKLOAD: ("--is-resumable-workload", "--isResumableWorkload", "-irw"),
    ENABLE_HYPERTHREADING: ("--enable-hyperthreading", "--enableHyperthreading", "--hyperthreading", "-ht"),
    SUPPORTED_CPU_ARCHITECTURES: ("--supported-cpu-architectures", "--supportedCpuArchitectures", "-sca"),
    TIME_TO_COST_PRIORITY_RATIO: ("--time-to-cost-priority-ratio", "--timeToCostPriorityRatio", "-tcpr"),
    WALLTIME_HOURS: ("--walltime-hours", "--walltimeHours", "-wh"),
    LICENSE_CONSUMPTION_PROFILE: ("--license-consuption-profile", "--licenseConsumptionProfile", "-lcp"),
    POST_PROCESSING_WALLTIME_HOURS: ("--post-processing-walltime-hours", "--postProcessingWalltimeHours", "-ppwh"),
    POST_PROCESSING_STORAGE_GIB: ("--post-processing-storage-gib", "--postProcessingStorageGiB", "-ppsgib"),
    POST_PROCESSING_RUN_COMMAND: ("--post-processing-run-command", "--postProcessingRunCommand", "-pprc"),
    POST_PROCESSING_TASK_NAME: ("--post-processing-task-name", "--postProcessingTaskName", "-pptn"),
    SYNC_JOB_FILES: ("--sync-job-files", "--syncJobFiles", "-sjf"),
    LIST_PROJECTS: ("--list-projects", "--listProjects", "-lpr"),
    PROJECT_NAME: ("--project-name", "--projectName", "-pn"),
    # Development overrides
    SKIP_CREATE_JOB_INFO_FOLDER: ("--skip-create-job-info-folder", "--skipCreateJobInfoFolder", "-scjif"),
}

CONFLICTING_CLI_ARGUMENT_SETS = [
    (
        OPEN_CONFIG_FOLDER,
        CREATE_JOB_WITH_UPLOAD,
        DOWNLOAD_JOB_FILES,
        GET_JOB_CURRENT_STATUS,
    ),
    (INCLUDE_INPUT, EXCLUDE_INPUT),
    (INCLUDE_OUTPUT, EXCLUDE_OUTPUT),
]

# Job types
CPU = "cpu"
GPU = "cpu+gpu"
GPU_INTERNAL_REPRESENTATION = "gpu"

PATH_TO_CONFIG_ROOT = os.path.join(os.path.expanduser("~"), ".fovus")
PATH_TO_JOB_CONFIGS = os.path.join(PATH_TO_CONFIG_ROOT, "job_configs")
PATH_TO_USER_CONFIGS = os.path.join(PATH_TO_CONFIG_ROOT, "user_configs")
PATH_TO_JOB_LOGS = os.path.join(PATH_TO_CONFIG_ROOT, "job_logs")
PATH_TO_LOGS = os.path.join(PATH_TO_CONFIG_ROOT, "logs")
PATH_TO_CREDENTIALS_FILE = os.path.join(PATH_TO_CONFIG_ROOT, ".credentials")
PATH_TO_WORKSPACE_SSO_TOKENS_FILE = os.path.join(PATH_TO_CONFIG_ROOT, ".workspace_sso_tokens")
PATH_TO_DEVICE_INFORMATION_FILE = os.path.join(PATH_TO_CONFIG_ROOT, ".device_information")
UNIX_OPEN = "open"
WINDOWS_EXPLORER = "explorer"

FOVUS_PROVIDED_CONFIGS_FOLDER_REPO = "fovus_provided_configs"
JOB_CONFIG_CONTAINERIZED_TEMPLATE_FILE_NAME = "FOVUS_job_template_containerized.json"
JOB_CONFIG_MONOLITHIC_TEMPLATE_FILE_NAME = "FOVUS_job_template_monolithic.json"
EXAMPLE_JOB_CONFIG_CONTAINERIZED_FILE_NAME = "FOVUS_example_job_config_containerized.json"
EXAMPLE_JOB_CONFIG_MONOLITHIC_LIST_FILE_NAME = "FOVUS_example_job_config_monolithic.json"

FILE_NAME = "FILE_NAME"
PATH_TO_CONFIG_FILE_IN_REPO = "PATH_TO_CONFIG_FILE_IN_REPO"
PATH_TO_CONFIG_FILE_LOCAL = "PATH_TO_CONFIG_FILE_LOCAL"

JOB_CONFIG_CONTAINERIZED_TEMPLATE = "JOB_CONFIG_CONTAINERIZED"
JOB_CONFIG_MONOLITHIC_TEMPLATE = "JOB_CONFIG_MONOLITHIC"
EXAMPLE_JOB_CONFIG_CONTAINERIZED = "EXAMPLE_JOB_CONFIG_CONTAINERIZED"
EXAMPLE_JOB_CONFIG_MONOLITHIC = "EXAMPLE_JOB_CONFIG_MONOLITHIC"
USER_CONFIG = "USER_CONFIG"
FOVUS_PROVIDED_CONFIGS = {
    JOB_CONFIG_CONTAINERIZED_TEMPLATE: {
        PATH_TO_CONFIG_FILE_IN_REPO: os.path.join(
            FOVUS_PROVIDED_CONFIGS_FOLDER_REPO, JOB_CONFIG_CONTAINERIZED_TEMPLATE_FILE_NAME
        ),
        PATH_TO_CONFIG_FILE_LOCAL: os.path.join(PATH_TO_JOB_CONFIGS, JOB_CONFIG_CONTAINERIZED_TEMPLATE_FILE_NAME),
    },
    JOB_CONFIG_MONOLITHIC_TEMPLATE: {
        PATH_TO_CONFIG_FILE_IN_REPO: os.path.join(
            FOVUS_PROVIDED_CONFIGS_FOLDER_REPO, JOB_CONFIG_MONOLITHIC_TEMPLATE_FILE_NAME
        ),
        PATH_TO_CONFIG_FILE_LOCAL: os.path.join(PATH_TO_JOB_CONFIGS, JOB_CONFIG_MONOLITHIC_TEMPLATE_FILE_NAME),
    },
    EXAMPLE_JOB_CONFIG_CONTAINERIZED: {
        PATH_TO_CONFIG_FILE_IN_REPO: os.path.join(
            FOVUS_PROVIDED_CONFIGS_FOLDER_REPO, EXAMPLE_JOB_CONFIG_CONTAINERIZED_FILE_NAME
        ),
        PATH_TO_CONFIG_FILE_LOCAL: os.path.join(PATH_TO_JOB_CONFIGS, EXAMPLE_JOB_CONFIG_CONTAINERIZED_FILE_NAME),
    },
    EXAMPLE_JOB_CONFIG_MONOLITHIC: {
        PATH_TO_CONFIG_FILE_IN_REPO: os.path.join(
            FOVUS_PROVIDED_CONFIGS_FOLDER_REPO, EXAMPLE_JOB_CONFIG_MONOLITHIC_LIST_FILE_NAME
        ),
        PATH_TO_CONFIG_FILE_LOCAL: os.path.join(PATH_TO_JOB_CONFIGS, EXAMPLE_JOB_CONFIG_MONOLITHIC_LIST_FILE_NAME),
    },
}
