# Defines classes for built-in log file types
# This simplifies referencing built-ins for functions and testing
from template_log_parser.sample import (
    debian_sample_log,
    omada_sample_log,
    omv_debian_sample_log,
    pihole_debian_sample_log,
    synology_sample_log,
)

from template_log_parser.templates.debian_templates import debian_template_dict
from template_log_parser.templates.omada_templates import (
    omada_template_dict,
    omada_column_process_dict,
    omada_merge_events_dict,
)
from template_log_parser.templates.omv_templates import omv_template_dict
from template_log_parser.templates.pihole_templates import (
    pihole_template_dict,
    pihole_merge_events_dict,
)
from template_log_parser.templates.synology_templates import (
    synology_template_dict,
    synology_column_process_dict,
    synology_merge_events_dict,
)


class BuiltInLogFileType:
    """Built In Log File Type as a class

    :param name: Simple name to reference the type
    :type name: str
    :param sample_log_file: File containing an example line to account for each template
    :type sample_log_file: str
    :param templates: Templates for the type should be equal in length to number of lines in the sample log file
    :type templates: dict
    :param column_functions: Formatted as {column: [function, [new_column(s)], kwargs], ...}
    :type column_functions: dict, None
    :param merge_events: Formatted as {'new_df_name', ['existing_df_1', 'existing_df_2', ...], ...}
    :type merge_events: dict, None
    :param datetime_columns: Columns to be converted using Pandas.to_datetime()
    :type datetime_columns: list, None
    :param localize_datetime_columns: Columns to drop timezone
    :type localize_datetime_columns: list, None
    """

    def __init__(
        self,
        name,
        sample_log_file,
        templates,
        column_functions,
        merge_events,
        datetime_columns,
        localize_datetime_columns,
    ):
        self.name = name
        self.sample_log_file = sample_log_file
        self.templates = templates
        self.column_functions = column_functions
        self.merge_events = merge_events
        self.datetime_columns = datetime_columns
        self.localize_datetime_columns = localize_datetime_columns


# BuiltInLogFileType Instances
debian = BuiltInLogFileType(
    name="debian",
    sample_log_file=debian_sample_log,
    templates=debian_template_dict,
    column_functions=None,
    merge_events=None,
    datetime_columns=["time"],
    localize_datetime_columns=None,
)

omada = BuiltInLogFileType(
    name="omada",
    sample_log_file=omada_sample_log,
    templates=omada_template_dict,
    column_functions=omada_column_process_dict,
    merge_events=omada_merge_events_dict,
    datetime_columns=["time"],
    localize_datetime_columns=None,
)

omv = BuiltInLogFileType(
    name="omv",
    sample_log_file=omv_debian_sample_log,
    templates=omv_template_dict,
    column_functions=None,
    merge_events=None,
    datetime_columns=["time"],
    localize_datetime_columns=None,
)

pihole = BuiltInLogFileType(
    name="pihole",
    sample_log_file=pihole_debian_sample_log,
    templates=pihole_template_dict,
    column_functions=None,
    merge_events=pihole_merge_events_dict,
    datetime_columns=["time"],
    localize_datetime_columns=None,
)

synology = BuiltInLogFileType(
    name="synology",
    sample_log_file=synology_sample_log,
    templates=synology_template_dict,
    column_functions=synology_column_process_dict,
    merge_events=synology_merge_events_dict,
    datetime_columns=["time"],
    localize_datetime_columns=None,
)

built_in_log_file_types = [debian, omada, omv, pihole, synology]
