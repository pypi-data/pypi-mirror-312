#!/usr/bin/env python3
import argparse

from fovus.constants.cli_constants import (
    ALLOW_PREEMPTIBLE,
    AUTO_DELETE_DAYS,
    BENCHMARKING_PROFILE_NAME,
    BOOLEAN_ARGS,
    CLI_ARGUMENTS,
    COMPUTING_DEVICE,
    CPU,
    CREATE_JOB_WITH_UPLOAD,
    DEBUG_MODE,
    DELETE_JOB,
    DOWNLOAD_JOB_FILES,
    ENABLE_HYPERTHREADING,
    EXCLUDE_INPUT,
    EXCLUDE_OUTPUT,
    FOVUS_PATH,
    GET_JOB_CURRENT_STATUS,
    GOV,
    GPU,
    INCLUDE_INPUT,
    INCLUDE_OUTPUT,
    IS_RESUMABLE_WORKLOAD,
    IS_SINGLE_THREADED_TASK,
    IS_SUBJECT_TO_AVAILABLE_RESOURCES,
    JOB_CONFIG_FILE_PATH,
    JOB_FILE_ROOT_DIRECTORY,
    JOB_ID,
    JOB_ID_LIST,
    JOB_MAX_CLUSTER_SIZE_VCPU,
    JOB_NAME,
    LICENSE_CONSUMPTION_PROFILE,
    LICENSE_TIMEOUT_HOURS,
    LIST_PROJECTS,
    LIVE_TAIL_FILE,
    LOCAL_PATH,
    LOGIN,
    LOGOUT,
    MAX_GPU,
    MAX_VCPU,
    MIN_GPU,
    MIN_GPU_MEM_GIB,
    MIN_VCPU,
    MIN_VCPU_MEM_GIB,
    MONOLITHIC_OVERRIDE,
    MONOLITHIC_OVERRIDE_ADDITIONAL_ARGUMENTS,
    MOUNT_STORAGE,
    MOUNT_STORAGE_PATH,
    OPEN_CONFIG_FOLDER,
    OUTPUT_FILE_LIST,
    OUTPUT_FILE_OPTION,
    PARALLELISM_CONFIG_FILES,
    PARALLELISM_OPTIMIZATION,
    POST_PROCESSING_RUN_COMMAND,
    POST_PROCESSING_STORAGE_GIB,
    POST_PROCESSING_TASK_NAME,
    POST_PROCESSING_WALLTIME_HOURS,
    PROJECT_NAME,
    REMOTE_INPUTS,
    RUN_COMMAND,
    SCALABLE_PARALLELISM,
    SCHEDULED_AT,
    SILENCE,
    SKIP_CREATE_JOB_INFO_FOLDER,
    STORAGE_GIB,
    SUPPORTED_CPU_ARCHITECTURES,
    SYNC_JOB_FILES,
    TIME_TO_COST_PRIORITY_RATIO,
    UNMOUNT_STORAGE,
    UPLOAD_FILES,
    USER,
    WALLTIME_HOURS,
    WINDOWS_DRIVE,
)
from fovus.util.cli_action_runner_util import CliActionRunnerUtil
from fovus.util.fovus_cli_argument_parser_util import FovusCliArgumentParserUtil

OK_RETURN_STATUS = 0

ANY_NUMBER_OF_EXPRESSIONS = "Any number of space-separated values can be provided."
FOR_DEVELOPMENT_USE_ONLY = "For development use only."
IF_IS_SINGLE_THREADED_NOTE = "(or multiple single-threaded tasks on each compute node if isSingleThreadedTask is true)"
JOB_DIRECTORY_REQUIRES_FOVUS_FOLDER_NOTE_WITH_DIRECTORY_AND_JOB_ID_EXPLANATION = (
    "(Note: If the job file directory is provided, the directory must contain a .fovus "
    "folder, which is automatically generated when a job is created with the Fovus CLI. "
    "If both a job file directory and job ID are provided, the job ID will be used.)"
)
PREFERRED_SCHEDULED_AT_FORMATS = (
    "The default time zone is your local time zone. Acceptable formats include the following. "
    '1) ISO 8601 format: "YYYY-MM-DDThh:mm:ss[.mmm]TZD" (e.g., "2020-01-01T18:30:00-05:00"). '
    '2) Date only (defaults to upcoming 12AM your local time zone): "YYYY-MM-DD" (e.g., "2020-01-01"). '
    '3) Time only (defaults to next upcoming time your local time zone): "hh:mmTZD" or "hh:mm" or "hh:mm AM/PM/am/pm" '
    '(e.g., "18:30-05:00" or "18:30" or "6:30 PM"). '
    '4) Natural language time: "DD month YYYY HH:MM AM/PM/am/pm timezone" (e.g., "21 July 2013 10:15 pm PDT").'
)
USED_FOR_OVERRIDING_JOB_CONFIG_VALUES = (
    "(Note: Used for overriding job config values. If this value is provided in the job "
    "config file, this argument is optional.)"
)
USED_FOR_OVERRIDING_USER_CONFIG_VALUES = (
    "(Note: Used for overriding user config values. If this value is provided in the user "
    "config file, this argument is optional.)"
)
WILDCARD_EXAMPLE = (
    "Wildcard characters (*, ?) can be "
    "used to specify file and directory patterns (e.g., out?/*.txt specifies all .txt files in out1, "
    "out2, and out3 folders under the working directory of each task). "
)
WILDCARD_EXPLANATION = WILDCARD_EXAMPLE + (
    "Supported wildcards: * (matches any number of characters), ? (matches any single character). "
    "Note: if a wildcard is used in an input, the input must be surrounded by quotes "
    '(e.g., "folder?/input*"). '
)
SYNC_FILES_NOTE = (
    f"Optional parameter({CliActionRunnerUtil.get_argument_string_list_from_keys([SYNC_JOB_FILES])})"
    " to instant trigger file sync for running job."
)


class FovusCliArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self._add_parser_arguments()
        self.args_dict = {}

    def _add_parser_arguments(self):  # pylint: disable=too-many-statements
        # Core functionality.
        self.parser.add_argument(
            *CLI_ARGUMENTS[CREATE_JOB_WITH_UPLOAD],
            action="store_true",
            help="Upload files to Fovus and create a new job. Creates .fovus folder inside the provided job file root "
            + "directory, which contains data about the job and enables checking job status and downloading job files "
            + "using the job file root directory. Required additional parameters: "
            + ", ".join(
                CliActionRunnerUtil.get_argument_string_list_from_keys([JOB_CONFIG_FILE_PATH, JOB_FILE_ROOT_DIRECTORY])
            )
            + ".",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[DELETE_JOB],
            action="store_true",
            help="Delete job records and job files from Fovus for a job or list of jobs. "
            + "Requires one of the following parameter: "
            + ", ".join(CliActionRunnerUtil.get_argument_string_list_from_keys([JOB_ID, JOB_ID_LIST]))
            + ". ",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[DOWNLOAD_JOB_FILES],
            action="store_true",
            help="Download job files from Fovus storage for a specified job. In case the "
            + " job is running, job files will be first synced to Fovus storage and  then downloaded. "
            + " Requires one of the following parameters: "
            + ", ".join(CliActionRunnerUtil.get_argument_string_list_from_keys([JOB_ID, JOB_FILE_ROOT_DIRECTORY]))
            + JOB_DIRECTORY_REQUIRES_FOVUS_FOLDER_NOTE_WITH_DIRECTORY_AND_JOB_ID_EXPLANATION,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[LIVE_TAIL_FILE],
            default=None,
            type=str,
            help="Live tail a text file of a running task for a given job. "
            + "Please specify the path of the file you want to monitor that start from the task. "
            + "For example, taskName/path/to/file. "
            + "Requires one of the following parameters: "
            + ", ".join(CliActionRunnerUtil.get_argument_string_list_from_keys([JOB_ID]))
            + ". ",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[OPEN_CONFIG_FOLDER],
            action="store_true",
            help="Open the Fovus CLI config folder, located at ~/.fovus. Also adds Fovus-provided config "
            + "file templates and examples to the folder for reference.",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[GET_JOB_CURRENT_STATUS],
            action="store_true",
            help="Get job status. Requires one of the following parameters: "
            + ", ".join(CliActionRunnerUtil.get_argument_string_list_from_keys([JOB_ID, JOB_FILE_ROOT_DIRECTORY]))
            + ". "
            + JOB_DIRECTORY_REQUIRES_FOVUS_FOLDER_NOTE_WITH_DIRECTORY_AND_JOB_ID_EXPLANATION,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[SILENCE],
            dest=SILENCE,
            default=False,
            action="store_true",
            help="Disable interactive CLI prompts and automatically dismiss warnings.",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[UPLOAD_FILES],
            action="store_true",
            help="Upload a file or folder to Fovus Storage (My Files). Requires the following parameters: "
            + ", ".join(CliActionRunnerUtil.get_argument_string_list_from_keys([LOCAL_PATH]))
            + ". ",
        )
        self.parser.add_argument(*CLI_ARGUMENTS[LOGIN], action="store_true", help="Login to the Fovus CLI.")
        self.parser.add_argument(
            *CLI_ARGUMENTS[GOV], action="store_true", help="An option to add to --login when login to Fovus Gov CLI."
        )
        self.parser.add_argument(*CLI_ARGUMENTS[LOGOUT], action="store_true", help="Logout the current user.")
        self.parser.add_argument(*CLI_ARGUMENTS[USER], action="store_true", help="View the current user's information.")
        self.parser.add_argument(
            *CLI_ARGUMENTS[MOUNT_STORAGE],
            action="store_true",
            help="Mount Fovus storage on your local computer under the path of /fovus-storage/ (for Linux) or "
            + r"<WindowsDrive>:\\fovus-storage\\ (for Windows) as a network file system. Job files are read-only. "
            + "The mounted network file system is optimized for high throughput read to large files by multiple clients"
            + " in parallel and sequential write to new files by one client at a time subject to your network speed. "
            + "Supported operating systems include Windows, Ubuntu, CentOS, and Redhat. "
            + "On Windows operating systems, by default, Fovus storage will be mounted to the M: drive, however, "
            + "you can add the --windows-drive option to specify a different drive to mount to instead. "
            + "(e.g, fovus --mount-storage --windows-drive Z). On both Linux and Windows operating systems, "
            + "you can add the --mount-storage-path option to specify a custom path to mount Fovus storage to "
            + "instead of the default path.",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[WINDOWS_DRIVE],
            dest=WINDOWS_DRIVE,
            default=None,
            type=str,
            choices=[chr(ord("A") + i) for i in range(26)],
            help="For Windows operating systems only. Specify the drive to which to mount Fovus storage."
            + ' Default value is "M". ',
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[MOUNT_STORAGE_PATH],
            dest=MOUNT_STORAGE_PATH,
            default=None,
            type=str,
            help="Optional. Specify the path to mount Fovus storage to. The default path is /fovus-storage/. "
            + "The specified path can be non-existing or an empty folder. For example, an user specified path "
            + 'of "/path/to/your/directory" or "/path/to/your/directory/" will mount Fovus storage to the path of '
            + "/path/to/your/directory/ in the case of Linux operating systems or "
            + r"<WindowsDrive>:\\path\\to\\your\\directory\\ in the case of Windows operating systems.",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[UNMOUNT_STORAGE], action="store_true", help="Unmount Fovus storage from your local computer."
        )

        # File paths.
        self.parser.add_argument(
            *CLI_ARGUMENTS[JOB_CONFIG_FILE_PATH],
            default=None,
            type=str,
            help="Absolute file path to a Fovus job config JSON. Values given in this file will be used unless they "
            + "are overridden by CLI input. The job config JSON must follow the structure given in the provided job "
            + "config templates, which are generated when the --open-config-folder command is used and will be located "
            + "in ~/.fovus/job_configs"
            + ".",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[JOB_FILE_ROOT_DIRECTORY],
            default=None,
            type=str,
            help="Root directory of job folder. A job folder contains one or multiple task folders. Each folder "
            + "uploaded under the job folder will be considered a task of the job. Each task folder is a "
            + "self-contained folder containing the necessary input files and scripts to run the task. For a job "
            + "that has N tasks (e.g. a DOE job with N simulation tasks), N task folders must exist under the job "
            + "folder and be uploaded.",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[LOCAL_PATH],
            default=None,
            type=str,
            help="Relative path with respect to the working directory or absolute path to a local file or folder to be"
            + " uploaded to Fovus Storage.",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[FOVUS_PATH],
            default=None,
            type=str,
            help=" Relative path to the Fovus Storage directory into which the local file or folder is to be uploaded."
            + " The relative path is with respect to the root directory of My Files. This argument is optional. If not"
            + " specified, the file or folder will be uploaded to the root directory of My Files",
        )

        # CLI behavior options
        self.parser.add_argument(
            *CLI_ARGUMENTS[DEBUG_MODE],
            dest=DEBUG_MODE,
            default=False,
            action="store_true",
            help="Enabling debug mode will keep compute nodes alive after each task execution until the task "
            + "walltimeHours is reached to allow additional time for interactive debugging via SSH.",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[AUTO_DELETE_DAYS],
            dest=AUTO_DELETE_DAYS,
            default=0,
            type=int,
            metavar="AUTO_DELETE_DAYS",
            help="Used with create job to set the auto-delete timer. The timer starts to tick upon job "
            + "completion or termination. The job will be permanently deleted when this timer expires.",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[EXCLUDE_INPUT],
            dest=EXCLUDE_INPUT,
            default=None,
            type=str,
            nargs="+",
            help="Used with create job for uploading job files."
            + "Exclude input file or folder path(s) (relative to the job root directory) that match"
            + " the expression. If a file or folder path "
            + "matches any expression, it will not be uploaded. "
            + " ".join((WILDCARD_EXPLANATION, ANY_NUMBER_OF_EXPRESSIONS)),
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[EXCLUDE_OUTPUT],
            dest=EXCLUDE_OUTPUT,
            default=None,
            type=str,
            nargs="+",
            help="Used with download job files. "
            "Exclude output file or folder path(s) (relative to the job root directory) that match the expression."
            + " If a file or folder path matches "
            + "any expression, it will not be downloaded. "
            + " ".join((WILDCARD_EXPLANATION, ANY_NUMBER_OF_EXPRESSIONS)),
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[INCLUDE_INPUT],
            dest=INCLUDE_INPUT,
            default=None,
            type=str,
            nargs="+",
            help="Used with create job for uploading job files. "
            + "Include input file or folder path(s) (relative to the job root directory) that match the expression."
            + " If a file or folder path does "
            + "not match any expression, it will not be uploaded. "
            + " ".join((WILDCARD_EXPLANATION, ANY_NUMBER_OF_EXPRESSIONS)),
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[INCLUDE_OUTPUT],
            dest=INCLUDE_OUTPUT,
            default=None,
            type=str,
            nargs="+",
            help="Used with download job files. "
            "Include output file or folder path(s) (relative to the job root directory) that match the expression."
            + " If a file or folder path does "
            + "not match any expression, it will not be downloaded. "
            + " ".join((WILDCARD_EXPLANATION, ANY_NUMBER_OF_EXPRESSIONS)),
        )

        # Job config.
        self.parser.add_argument(
            *CLI_ARGUMENTS[BENCHMARKING_PROFILE_NAME],
            dest=BENCHMARKING_PROFILE_NAME,
            default=None,
            type=str,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(BENCHMARKING_PROFILE_NAME).upper(),
            help="Fovus will optimize the cloud strategies for your job execution, including determining the "
            + "optimal choices of virtual HPC infrastructure and computation parallelism, if applicable, based "
            + "upon the selected benchmarking profile. For the best optimization results, select the benchmarking "
            + "profile whose characteristics best resemble the workload under submission. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[COMPUTING_DEVICE],
            dest=COMPUTING_DEVICE,
            default=None,
            type=str,
            choices=[CPU, GPU],
            help=f"The target computing device(s) for running your workload. {USED_FOR_OVERRIDING_JOB_CONFIG_VALUES}",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[JOB_NAME],
            dest=JOB_NAME,
            default=None,
            type=str,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(JOB_NAME).upper(),
            help="Job name. If not provided, a job name will be automatically generated using the current timestamp. "
            + "If a job name is not provided, the job ID will be used.",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[JOB_ID],
            dest=JOB_ID,
            default=None,
            type=str,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(JOB_ID).upper(),
            help="Job ID. Used for checking job status and downloading job files if the root file directory is not "
            + "provided.",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[SYNC_JOB_FILES],
            dest=SYNC_JOB_FILES,
            default=False,
            action="store_true",
            help="Sync the current job files of a running job to Fovus storage. This can be "
            + "only applied to a job in running status. Requires one of the following parameters: "
            + ", ".join(CliActionRunnerUtil.get_argument_string_list_from_keys([JOB_ID])),
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[JOB_ID_LIST],
            dest=JOB_ID_LIST,
            default=None,
            type=str,
            nargs="+",
            metavar=FovusCliArgumentParserUtil.camel_to_snake(JOB_ID_LIST).upper(),
            help="A list of Job IDs. Used for deleting jobs in batch.",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[IS_SINGLE_THREADED_TASK],
            dest=IS_SINGLE_THREADED_TASK,
            default=None,
            type=str,
            choices=["true", "false"],
            metavar=FovusCliArgumentParserUtil.camel_to_snake(IS_SINGLE_THREADED_TASK).upper(),
            help="Set true if and only if each task uses only a single CPU thread (vCPU) at a maximum. "
            + "Setting it true allows multiple tasks to be deployed onto the same compute node to maximize the "
            + "task-level parallelism and the utilization of all CPU threads (vCPUs).",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[LICENSE_TIMEOUT_HOURS],
            dest=LICENSE_TIMEOUT_HOURS,
            default=None,
            type=float,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(LICENSE_TIMEOUT_HOURS).upper(),
            help="For license-required jobs, the maximum time the job is allowed to be waiting in a queue for "
            + "deployment when no license is available. A job will be terminated once the timeout timer expires. "
            + "Not applicable to license-free jobs. Format: Real (e.g., 1.5). Range: ≥1. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[MONOLITHIC_OVERRIDE],
            dest=MONOLITHIC_OVERRIDE,
            **MONOLITHIC_OVERRIDE_ADDITIONAL_ARGUMENTS,
            help="Override a monolithic software environment. All four values are required to reference a monolithic "
            + "software and its license usage constraint. Currently, the only supported override for a monolithic "
            + "software environment is the license count, and as a result, only the "
            + f"license count is overridden. {USED_FOR_OVERRIDING_JOB_CONFIG_VALUES}",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[MIN_GPU],
            dest=MIN_GPU,
            default=None,
            type=int,
            metavar="MIN_GPU",
            help="The minimum number of GPUs required to parallelize the execution of each task. Only values "
            + f"supported by the selected BP are allowed. {USED_FOR_OVERRIDING_JOB_CONFIG_VALUES}",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[MAX_GPU],
            dest=MAX_GPU,
            default=None,
            type=int,
            metavar="MAX_GPU",
            help="The maximum number of GPUs allowed to parallelize the execution of each task. Only values "
            + f"supported by the selected BP are allowed. {USED_FOR_OVERRIDING_JOB_CONFIG_VALUES}",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[MIN_GPU_MEM_GIB],
            dest=MIN_GPU_MEM_GIB,
            default=None,
            type=float,
            metavar="MIN_GPU_MEM_GIB",
            help="The minimum total size of GPU memory required to support the execution of each task, summing "
            + "the required memory size for each GPU. Format: Real (e.g., 10.5). Only values supported by the "
            + "selected BP are allowed. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[MIN_VCPU],
            dest=MIN_VCPU,
            default=None,
            type=int,
            metavar="MIN_VCPU",
            help="The minimum number of vCPUs required to parallelize the execution of each task "
            f"{IF_IS_SINGLE_THREADED_NOTE}. A vCPU refers to a thread "
            "of a CPU core. Only values supported by the selected BP are allowed. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[JOB_MAX_CLUSTER_SIZE_VCPU],
            dest=JOB_MAX_CLUSTER_SIZE_VCPU,
            default=None,
            type=int,
            metavar="JOB_MAX_CLUSTER_SIZE_VCPU",
            help="The maximum cluster size in terms of the total number of vCPUs allowed for parallelizing task runs "
            + "in the job, which only takes into effect when isSingleThreadedTask is true. A default value of 0 means "
            + "no limit. ",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[MAX_VCPU],
            dest=MAX_VCPU,
            default=None,
            type=int,
            metavar="MAX_VCPU",
            help="The maximum number of vCPUs allowed to parallelize the execution of each task "
            f"{IF_IS_SINGLE_THREADED_NOTE}. A vCPU refers to a thread "
            "of a CPU core. Only values supported by the selected BP are allowed. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[MIN_VCPU_MEM_GIB],
            dest=MIN_VCPU_MEM_GIB,
            default=None,
            type=float,
            metavar="MIN_VCPU_MEM_GIB",
            help="The minimum total size of system memory required to support the execution of each task "
            f"{IF_IS_SINGLE_THREADED_NOTE}, summing the "
            "required memory size for each vCPU. Format: Real (e.g., 10.5). Only values supported by the selected "
            "BP are allowed. " + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[OUTPUT_FILE_LIST],
            dest=OUTPUT_FILE_LIST,
            default=None,
            type=str,
            nargs="+",
            metavar=FovusCliArgumentParserUtil.camel_to_snake(OUTPUT_FILE_LIST)[: -len("_List")].upper(),
            help="Specify the output files to include or exclude from transferring back to the cloud storage "
            + "using relative paths from the working directory of each task. "
            + " ".join((WILDCARD_EXPLANATION, ANY_NUMBER_OF_EXPRESSIONS, USED_FOR_OVERRIDING_JOB_CONFIG_VALUES)),
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[OUTPUT_FILE_OPTION],
            dest=OUTPUT_FILE_OPTION,
            default=None,
            type=str,
            choices=["include", "exclude"],
            help="Specify whether the output files in outputFileList should be included or excluded from "
            + "transferring back to the cloud storage after the job is completed. See outputFileList for more "
            + "information. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[REMOTE_INPUTS],
            dest=REMOTE_INPUTS,
            default=None,
            type=str,
            nargs="+",
            metavar=FovusCliArgumentParserUtil.camel_to_snake(REMOTE_INPUTS)[:-1].upper(),
            help="Provide the URL of or path to any file or folder in Fovus storage. The files and folders specified "
            + "will be included under the working directory of each task as inputs for all tasks and will be excluded "
            + "from syncing back to Fovus storage as job files. If the file or folder is from My Files of Fovus "
            + 'Storage, a short relative path works the same as the URL. The path to a folder must end with "/". '
            + " ".join((ANY_NUMBER_OF_EXPRESSIONS, USED_FOR_OVERRIDING_JOB_CONFIG_VALUES))
            + "Examples:"
            + '"folderName/fileName.txt" works the same as "https://app.fovus.co/files?path=folderName/fileName.txt"'
            + '"folderName/" works the same as  "https://app.fovus.co/folders?path=folderName""',
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[PARALLELISM_CONFIG_FILES],
            dest=PARALLELISM_CONFIG_FILES,
            default=None,
            type=str,
            nargs="+",
            metavar=FovusCliArgumentParserUtil.camel_to_snake(PARALLELISM_CONFIG_FILES)[:-1].upper(),
            help="Specify the configuration files that contain Fovus Environment Tokens, if any, using "
            + "relative paths from the working directory of each task. All Fovus Environment Tokens in the "
            + "configuration files specified will be resolved to values prior to task execution. "
            + " ".join((WILDCARD_EXPLANATION, ANY_NUMBER_OF_EXPRESSIONS, USED_FOR_OVERRIDING_JOB_CONFIG_VALUES)),
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[PARALLELISM_OPTIMIZATION],
            dest=PARALLELISM_OPTIMIZATION,
            default=None,
            type=str,
            choices=["true", "false"],
            help="If enabled, Fovus will determine the optimal parallelism for parallelizing the computation of "
            + "each task to minimize the total runtime and cost based on the time-to-cost priority ratio (TCPR) "
            + "specified. To pass in the optimal parallelism to your software program, you can directly use the Fovus "
            + "environment tokens, e.g., $FovusOptVcpu, $FovusOptGpu, in your command lines or or in the input "
            + "configuration files specified by the parallelismConfigFiles job config field. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[RUN_COMMAND],
            dest=RUN_COMMAND,
            default=None,
            type=str,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(RUN_COMMAND).upper(),
            help="Specify the command lines to launch each task. The same command lines will be executed under the "
            + f"working directory of each task. {USED_FOR_OVERRIDING_JOB_CONFIG_VALUES}",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[SCALABLE_PARALLELISM],
            dest=SCALABLE_PARALLELISM,
            default=None,
            type=str,
            choices=["true", "false"],
            help="A software program exhibits scalable parallelism if it can make use of more computing devices "
            + "(e.g., vCPUs and/or GPUs) to parallelize a larger computation task. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[SCHEDULED_AT],
            dest=SCHEDULED_AT,
            default=None,
            type=str,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(SCHEDULED_AT).upper(),
            help=f"The time at which the job is scheduled to be submitted. {PREFERRED_SCHEDULED_AT_FORMATS}",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[STORAGE_GIB],
            dest=STORAGE_GIB,
            default=None,
            type=int,
            metavar="STORAGE_GIB",
            help="The total size of local SSD storage required to support the execution of each task "
            f"{IF_IS_SINGLE_THREADED_NOTE}. No need to include any storage space for the operating system. This is "
            + "only for task storage. Format: Integer. Range: [1, 65536]. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[IS_SUBJECT_TO_AVAILABLE_RESOURCES],
            dest=IS_SUBJECT_TO_AVAILABLE_RESOURCES,
            default=None,
            type=str,
            choices=["true", "false"],
            help="If true, the cloud strategy optimization will be performed subject to only the cloud resources "
            + "that are currently available for provisioning, so does the optimal time-cost tradeoff resulting from "
            + "the optimization. If false, the cloud strategy optimization will be performed regardless of the "
            + "current availability of cloud resources. If case the optimal virtual HPC infrastructure is "
            + "unavailable at the time, infrastructure provisioning will be attempted until it becomes available. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )

        self.parser.add_argument(
            *CLI_ARGUMENTS[ALLOW_PREEMPTIBLE],
            dest=ALLOW_PREEMPTIBLE,
            default=None,
            type=str,
            choices=["true", "false"],
            help="Enabling preemptible resources will restrict the maximum task Walltime allowed to 6 hours if "
            + "the workload under submission is resumable, otherwise, 3 hours if not resumable. Preemptible"
            + " resources are subject to reclaim by cloud service providers, resulting in the possibility of "
            + "interruption to task run. Enabling preemptible resources will allow cloud strategy optimization to "
            + "estimate, based on the interruption probability, the expected cost saving that can be statistically "
            + "achieved by leveraging preemptible resources. In case the expected saving is meaningful, preemptible "
            + "resources will be prioritized for use during the infrastructure provisioning. Any interrupted tasks due "
            + "to the reclaim of preemptible resources will be re-queued for re-execution to ensure job completion. "
            + "PLEASE NOTE that the expected cost saving is estimated in the statistical sense. So there is a chance "
            + "that such savings may not be realized at the individual task or job level. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )

        self.parser.add_argument(
            *CLI_ARGUMENTS[IS_RESUMABLE_WORKLOAD],
            dest=IS_RESUMABLE_WORKLOAD,
            default=None,
            type=str,
            choices=["true", "false"],
            help="To indicate if the workload under submission supports saving work in progress and reloading the "
            + "saved session to resume running from where it left off.  The cloud strategy optimization will take "
            + "into account if the workload is resumable to more accurately analyze the expected runtime and cost "
            + "for the cloud strategies leveraging preemptible resources."
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )

        self.parser.add_argument(
            *CLI_ARGUMENTS[ENABLE_HYPERTHREADING],
            dest=ENABLE_HYPERTHREADING,
            default=None,
            type=str,
            choices=["true", "false"],
            help="For the CPUs that support hyperthreading, enabling hyperthreading allows two threads (vCPUs) to run "
            + "concurrently on a single CPU core. For HPC workloads, disabling hyperthreading may potentially result "
            + "in performance benifits with respect to the same CPU cores (e.g., 32 threads - 32 cores with "
            + "hyperthreading disabled v.s. 64 threads - 32 cores with hyperthreading enabled), whereas enabling "
            + "hyperthreading may potentially result in cost benifits with respect to the same parallelism (e.g., 64 "
            + "threads - 32 cores with hyperthreading enabled v.s. 64 threads - 64 cores with hyperthreading disabled)."
            + " "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[SUPPORTED_CPU_ARCHITECTURES],
            dest=SUPPORTED_CPU_ARCHITECTURES,
            default=None,
            type=str,
            nargs="+",
            metavar=FovusCliArgumentParserUtil.camel_to_snake(SUPPORTED_CPU_ARCHITECTURES)[:-1].upper(),
            help="The CPU architecture(s) compatible with your workload. Running your workload on an incompatible "
            + "CPU architecture may result in a failed job. "
            + f"{ANY_NUMBER_OF_EXPRESSIONS} {USED_FOR_OVERRIDING_JOB_CONFIG_VALUES}",
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[TIME_TO_COST_PRIORITY_RATIO],
            dest=TIME_TO_COST_PRIORITY_RATIO,
            default=None,
            type=str,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(TIME_TO_COST_PRIORITY_RATIO).upper(),
            help="Fovus will optimize the cloud strategies for your job execution to minimize the total runtime "
            + "and cost based on the time-to-cost priority ratio (TCPR) specified below. TCPR defines the weights "
            + "(amount of importance) to be placed on time minimization over cost minimization on a relative scale. "
            + "In particular, a ratio of 1/0 or 0/1 will enforce cloud strategies to pursue the minimum achievable "
            + 'runtime or cost without consideration of cost or runtime, respectively. Format must be "num1/num2" '
            + "where num1 + num2 = 1, 0 <= num1 <= 1, and 0 <= num2 <= 1. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[LICENSE_CONSUMPTION_PROFILE],
            dest=LICENSE_CONSUMPTION_PROFILE,
            default=None,
            type=str,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(LICENSE_CONSUMPTION_PROFILE).upper(),
            help="licenseConsumptionProfile defines the pattern of license draw based on running conditions, "
            + "such as vCPU or GPU parallelism. When an LCP is specified, the license consumption constraints "
            + "for queue and auto-scaling will be automatically extracted based on the running conditions defined by "
            + "the optimal cloud strategy. licenseConsumptionProfile has a higher precedence than licenseCountPerTask."
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[WALLTIME_HOURS],
            dest=WALLTIME_HOURS,
            default=None,
            type=float,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(WALLTIME_HOURS).upper(),
            help="The maximum time each task is allowed to run. A task will be terminated without a condition "
            + "once the walltime timer expires. Format: Real (e.g., 1.5). Range: >0. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )
        self.parser.add_argument(
            *CLI_ARGUMENTS[POST_PROCESSING_WALLTIME_HOURS],
            dest=POST_PROCESSING_WALLTIME_HOURS,
            default=None,
            type=float,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(POST_PROCESSING_WALLTIME_HOURS).upper(),
            help="The maximum time each task is allowed to run Post Processing Task. "
            + "A task will be terminated without a condition "
            + "once the walltime timer expires. Format: Real (e.g., 1.5). Range: >0. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )

        self.parser.add_argument(
            *CLI_ARGUMENTS[POST_PROCESSING_STORAGE_GIB],
            dest=POST_PROCESSING_STORAGE_GIB,
            default=None,
            type=int,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(POST_PROCESSING_STORAGE_GIB).upper(),
            help="The total size of local SSD storage required to support the execution of post processing task. "
            + "No need to include any storage space for the operating system. This is "
            + "only for task storage. Format: Integer. Range: [1, 65536]. "
            + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )

        self.parser.add_argument(
            *CLI_ARGUMENTS[POST_PROCESSING_RUN_COMMAND],
            dest=POST_PROCESSING_RUN_COMMAND,
            default=None,
            type=str,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(POST_PROCESSING_RUN_COMMAND).upper(),
            help="Specify the command lines to launch post processing task. "
            + "The same command lines will be executed under the "
            + f"working directory of post processing task. {USED_FOR_OVERRIDING_JOB_CONFIG_VALUES}",
        )

        self.parser.add_argument(
            *CLI_ARGUMENTS[POST_PROCESSING_TASK_NAME],
            dest=POST_PROCESSING_TASK_NAME,
            default=None,
            type=str,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(POST_PROCESSING_TASK_NAME).upper(),
            help="Specify the folder name of post processing task. " + USED_FOR_OVERRIDING_JOB_CONFIG_VALUES,
        )

        self.parser.add_argument(
            *CLI_ARGUMENTS[LIST_PROJECTS],
            action="store_true",
            help="List all valid project names of your cost center.",
        )

        self.parser.add_argument(
            *CLI_ARGUMENTS[PROJECT_NAME],
            dest=PROJECT_NAME,
            default=None,
            type=str,
            metavar=FovusCliArgumentParserUtil.camel_to_snake(PROJECT_NAME).upper(),
            help="The project name associated with your job. "
            + "If omitted, the default project will be used. Use 'None' to specify no project.",
        )

        # Development overrides
        self.parser.add_argument(
            *CLI_ARGUMENTS[SKIP_CREATE_JOB_INFO_FOLDER],
            dest=SKIP_CREATE_JOB_INFO_FOLDER,
            action="store_true",
            help="Skip creating the job info folder. " + FOR_DEVELOPMENT_USE_ONLY,
        )

    def parse_args(self):
        args = self.parser.parse_args()
        self.args_dict = vars(args)
        self._convert_boolean_args_to_bool()
        FovusCliArgumentParserUtil.set_timestamp(self.args_dict)

    def _convert_boolean_args_to_bool(self):
        for key in self.args_dict:
            if key in BOOLEAN_ARGS:
                if self.args_dict[key] == "true":
                    self.args_dict[key] = True
                elif self.args_dict[key] == "false":
                    self.args_dict[key] = False

    def get_args_dict(self):
        return self.args_dict
