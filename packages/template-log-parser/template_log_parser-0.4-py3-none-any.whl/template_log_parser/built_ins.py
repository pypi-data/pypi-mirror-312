from template_log_parser.log_functions import process_log

from template_log_parser.log_type_classes import built_in_log_file_types


def built_in_process_log(built_in, file, dict_format=True):
    """Return a single Pandas Dataframe or dictionary of DataFrames whose keys are the log file event types,
    utilizing predefined templates.  This function is tailored to Built-In log file types using Built-In templates.

    :param built_in: built in log file parameter
    :type built_in: str {'debian', 'omada', 'omv', 'pihole', 'synology'}
    :param file: Path to file or filelike object, most commonly in the format of some_log_process.log
    :type file: str
    :param dict_format: (optional) Return a dictionary of DataFrames when True, one large DataFrame when False, True by default
    :type dict_format: bool

    :return: dict formatted as {'event_type_1': df_1, 'event_type_2': df_2, ...}, Pandas Dataframe will include all event types and all columns
    :rtype: dict, Pandas.DataFrame

    Note:
        This function utilizes process_log()
    """
    # Determine built_in based on name attribute
    built_in_type = [item for item in built_in_log_file_types if item.name == built_in][
        0
    ]

    output = process_log(
        file=file,
        template_dictionary=built_in_type.templates,
        additional_column_functions=built_in_type.column_functions,
        merge_dictionary=built_in_type.merge_events,
        datetime_columns=built_in_type.datetime_columns,
        localize_timezone_columns=built_in_type.localize_datetime_columns,
        drop_columns=True,
        dict_format=dict_format,
    )

    return output
