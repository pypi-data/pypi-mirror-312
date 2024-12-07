import pandas as pd
from parse import parse

# set display options
pd.options.display.max_columns = 40
pd.options.display.width = 120
pd.set_option("max_colwidth", 400)

# These variables exist here to avoid hardcoded values all over the project
event_data_column = "event_data"
event_type_column = "event_type"
parsed_info_column = "parsed_info"

other_type_column = "Other"
unparsed_text_column = "Unparsed_text"


def parse_function(event, template_dictionary):
    """Return a tuple of an event type and a dictionary of information parsed from a log file string based on matching template.

    :param event: String data, should ideally match a repeated format throughout a text file
    :type event: str
    :param template_dictionary: formatted as {search_string: [template, number_of_expected_values, event_type], ...}
    :type template_dictionary: dict

    :return: Tuple formatted as (event_type, {'value_1': 'some_value', 'value2': 'some_other_value', ...})
    :rtype: tup


    Examples:
        event_string = '2024-09-12 main_server connected to 10.10.10.102'

        template_one = '{date} {client_name} connected to {host_ip_address}'

        example_template_dictionary = {'connected to': [template_one, 3, 'host_connection_event'], ...}

        parsed_event = parse_function(event_string, example_template_dictionary)

        print(parsed_event)

        ('host_connection_event', {'date': '2024-09-12', 'client_name': 'main_server', 'host_ip_address': '10.10.10.102'})

    Note:
        If event string does not match a provided template, it will return ('Other', {'Unparsed_text': event})
    """
    # If nothing is found in the entire dictionary
    # Return generic results, unparsed text, new template will be needed
    valid_template = other_type_column
    result = {unparsed_text_column: event}

    # Using the dictionary of templates
    for search_string, attributes in template_dictionary.items():
        # Check if search string is present within event to ensure only appropriate templates are used
        # Multiple template search strings may be present within event, but checking a few templates is still faster
        # Than checking all templates
        if search_string in event:
            # template is located inside list of attributes, first position
            parsed_result = parse(attributes[0], event)
            # If a parsed_result is returned it means that the template matched so some degree
            if parsed_result is not None:
                # Check to make sure the number of values equals the expected number, list of attributes second position
                if len(parsed_result.named) == attributes[1]:
                    # If so, update the valid template (position 2), and return the dictionary of item_names: values
                    valid_template = attributes[2]
                    # result.named is the dictionary attribute of a Result object
                    result = parsed_result.named
                    break
            # If no parsed result is returned, use default values for "Other"
            elif parsed_result is None:
                valid_template = other_type_column
                result = {unparsed_text_column: event}

    return valid_template, result


def log_pre_process(file, template_dictionary):
    """Return a Pandas DataFrame from a log file with event_data, event_type, and parsed_info columns based on parsed event data text

    :param file: Path to file or filelike object, most commonly in the format of some_log_process.log
    :type file: str
    :param template_dictionary: formatted as {search_string: [template, number_of_expected_values, event_type], ...}
    :type template_dictionary: dict

    :return: DataFrame with columns 'event_data', 'event_type', 'parsed_info'
    :rtype: Pandas.DataFrame


    Note:
        event_data is the raw text from within the log file

        event_type is defined from the template dictionary that matched a line of text

        parsed_info is a dictionary within the column that contains key/value pairs based on the matching template

        See parse_function() for specific information on templates
    """
    # Read log file
    pre_df = pd.read_table(
        file, header=None, names=[event_data_column], on_bad_lines="warn"
    )

    # Parse event data, create event_type column to streamline the next process
    pre_df[[event_type_column, parsed_info_column]] = pre_df.apply(
        lambda row: parse_function(row[event_data_column], template_dictionary),
        axis="columns",
        result_type="expand",
    )

    return pre_df


def run_functions_on_columns(
    df,
    additional_column_functions=None,
    datetime_columns=None,
    localize_timezone_columns=None,
):
    """Return a tuple with a Pandas Dataframe (having newly created columns based on run functions)
    along with a list of columns that were processed

    :param df: DataFrame for processing
    :type df: Pandas.DataFrame
    :param additional_column_functions: (optional) {column: [function, [new_column(s)], kwargs], ...}
    :type additional_column_functions: dict
    :param datetime_columns: (optional) Columns to be converted using Pandas.to_datetime()
    :type datetime_columns: list
    :param localize_timezone_columns: (optional) Columns to drop timezone
    :type localize_timezone_columns: list

    :return: DataFrame with newly processed columns, list of columns that were processed
    :rtype: tup

    Examples:
        my_kwargs = dict(keyword_1='some_string', keyword_2=1000, keyword_3=[1,2,3])

        my_column_functions = {
            'column_to_run_function_on': [function, 'new_column_name'],
            'column_2_to_run_function_on': [create_two_columns, ['new_col_2, 'new_col_3']],
            'column_4_to_run_function_on': [function_with_kwargs, 'new_col_4', my_kwargs],
            }

    Note:
        This function (excepting datetime columns) is designed to create new columns and provide a list
        of columns to be dropped at a later stage.  One can create custom functions, or use the included functions.
        An example of this would be the calc_time() function which can convert strings such as '1h12m'
        to integer 72.

        Sometimes a function is designed to expand one column into two or more new columns.
        In this instance, one can provide a list of new column names. Please see example.

        If only df parameter is supplied, function will return the original df and an empty list
    """
    processed_columns = []
    # Dictionary should be in the format of: {existing_column: [function, new_column_name(s)]}
    # New column names can be list as well: {existing_column: [function, [list_of_new_columns]]}
    # if functions are supplied
    if additional_column_functions:
        for column, new_features in additional_column_functions.items():
            if column in df.columns:
                # Single column function application
                if type(new_features[1]) is str:
                    # If no kwargs are present, new features will have a length of 2
                    if len(new_features) == 2:
                        df[new_features[1]] = df.apply(
                            lambda row: new_features[0](row[column]), axis="columns"
                        )
                    # If kwargs are provided, new features will have a length of 3
                    elif len(new_features) == 3:
                        df[new_features[1]] = df.apply(
                            lambda row: new_features[0](row[column], **new_features[2]),
                            axis="columns",
                        )

                # Multi column function expansion
                elif type(new_features[1]) is list:
                    # If no kwargs are present, new features will have a length of 2
                    if len(new_features) == 2:
                        df[new_features[1]] = df.apply(
                            lambda row: new_features[0](row[column]),
                            axis="columns",
                            result_type="expand",
                        )
                    # If kwargs are provided, new features will have a length of 3
                    elif len(new_features) == 3:
                        df[new_features[1]] = df.apply(
                            lambda row: new_features[0](row[column], **new_features[2]),
                            axis="columns",
                            result_type="expand",
                        )

                processed_columns.append(column)

    # If datetime columns are present
    if datetime_columns:
        for datetime_column in datetime_columns:
            if datetime_column in df.columns:
                df[datetime_column] = pd.to_datetime(df[datetime_column])

    # If timezones need to be dropped from certain columns
    if localize_timezone_columns:
        for column in localize_timezone_columns:
            if column in df.columns:
                df[column] = df[column].dt.tz_localize(None)

    return df, processed_columns


def process_event_types(
    df,
    additional_column_functions=None,
    datetime_columns=None,
    localize_timezone_columns=None,
    drop_columns=True,
):
    """Return a dictionary of Pandas DataFrames whose keys are event types

    :param df: DataFrame for processing
    :type df: Pandas.DataFrame
    :param additional_column_functions: (optional) {column: [function, [new_column(s)], kwargs], ...}
    :type additional_column_functions: dict
    :param datetime_columns: (optional) Columns to be converted using Pandas.to_datetime()
    :type datetime_columns: list
    :param localize_timezone_columns: (optional) Columns to drop timezone
    :type localize_timezone_columns: list
    :param drop_columns: (optional) If True, 'parsed_info', 'event_data' will be dropped along with columns processed by additional_column_functions, True by default
    :type drop_columns: bool

    :return: DataFrame Dictionary formatted as {'event_type_1': df_1, 'event_type_2': df_2, ...}
    :rtype: dict
    """
    final_dict = {}
    # For every unique event_type, create a copy df
    for event_type in df[event_type_column].unique().tolist():
        temp_df = df[df[event_type_column] == event_type].copy()

        # Parsed info column has dictionary of columns: data, json_normalize will create new column for each key
        df_explode_events = pd.json_normalize(temp_df[parsed_info_column])
        # Create new df by concatenating the expanded values onto the original df
        event_df = pd.concat(
            [temp_df.reset_index(drop=True), df_explode_events.reset_index(drop=True)],
            axis=1,
        )

        # Default Columns to be dropped
        columns_to_drop = [parsed_info_column, event_data_column]

        # Process columns
        event_df, additional_drop_columns = run_functions_on_columns(
            df=event_df,
            additional_column_functions=additional_column_functions,
            datetime_columns=datetime_columns,
            localize_timezone_columns=localize_timezone_columns,
        )
        columns_to_drop.extend(additional_drop_columns)

        if drop_columns is True:
            event_df = event_df.drop(columns=columns_to_drop)
        # Add the df to the final dict with a key of its event type
        final_dict[event_type] = event_df

    return final_dict


def merge_event_type_dfs(df_dictionary, merge_dictionary):
    """Return a dictionary of Pandas DataFrames whose keys are the event types, after merging specified event_types and
    deleting the old DataFrames

    :param df_dictionary: Dictionary of DataFrames, formatted as {'event_type_1': df_1, 'event_type_2': df_2, ...}
    :type df_dictionary: dict
    :param merge_dictionary: Formatted as {'new_df_name', ['existing_df_1', 'existing_df_2', ...], ...}
    :type merge_dictionary: dict

    :return: Dictionary of DataFrames formatted as {'new_df_name': new_df, 'existing_event_type_3': existing_df_3, ...}
    :rtype: dict

    Note:
        Certain log events are categorically similar despite being parsed with different templates.
        For example, client wireless connections and client hardwired connections might be easier to analyze when
        grouped into the same DataFrame.

        This function performs that concatenation and deletes the old DataFrames.
    """
    # Merge_dictionary format {'new_df_name': ['existing_df_1', 'existing_df2', ...]}

    # Using new df_name, and a list of existing dfs
    for new_df_name, list_of_existing_dfs in merge_dictionary.items():
        # Empty list to be filled with dfs that will be merged under a new key name
        list_of_dfs_to_concatenate = []

        for old_name in list_of_existing_dfs:
            # Check to ensure that a key exists for each type of df to prevent an error
            if old_name in df_dictionary.keys():
                # If so add it to the list and remove it from the main dictionary
                list_of_dfs_to_concatenate.append(df_dictionary[old_name])
                del df_dictionary[old_name]
        # Assuming at least one df got appended
        if list_of_dfs_to_concatenate:
            # Create new concat df
            df_dictionary[new_df_name] = pd.concat(list_of_dfs_to_concatenate)

    return df_dictionary


def process_log(
    file,
    template_dictionary,
    additional_column_functions=None,
    merge_dictionary=None,
    datetime_columns=None,
    localize_timezone_columns=None,
    drop_columns=True,
    dict_format=True,
):
    """Return a single Pandas Dataframe or dictionary of DataFrames whose keys are the log file event types,
    utilizing templates.

    :param file: Path to file or filelike object, most commonly in the format of some_log_process.log
    :type file: str
    :param template_dictionary: formatted as {search_string: [template, number_of_expected_values, event_type], ...}
    :type template_dictionary: dict
    :param additional_column_functions: (optional) {column: [function, [new_column(s)], kwargs], ...}
    :type additional_column_functions: dict
    :param merge_dictionary: Formatted as {'new_df_name', ['existing_df_1', 'existing_df_2', ...], ...}
    :type merge_dictionary: dict
    :param datetime_columns: (optional) Columns to be converted using Pandas.to_datetime()
    :type datetime_columns: list, None
    :param localize_timezone_columns: (optional) Columns to drop timezone
    :type localize_timezone_columns: list, None
    :param drop_columns: (optional) If True, 'parsed_info', 'event_data' will be dropped along with processed columns, True by default
    :type drop_columns: bool
    :param dict_format: Return a dictionary of DataFrames when True, one large DataFrame when False, True by default
    :type dict_format: (optional) bool

    :return: Dict formatted as {'event_type_1': df_1, 'event_type_2': df_2, ...} or DataFrame with all event types and all columns
    :rtype: dict, Pandas.DataFrame

    Note:
        This function incorporates several smaller functions.
        For more specific information, please see help for individual functions:

        parse_function() \n
        log_pre_process() \n
        run_functions_on_columns() \n
        process_event_types() \n
        merge_event_types() \n
    """
    # Initial parsing
    pre_df = log_pre_process(file, template_dictionary)

    # Process each event type
    dict_of_dfs = process_event_types(
        pre_df,
        additional_column_functions=additional_column_functions,
        datetime_columns=datetime_columns,
        localize_timezone_columns=localize_timezone_columns,
        drop_columns=drop_columns,
    )

    # Merge event DataFrames for consolidation, if specified
    if merge_dictionary:
        dict_of_dfs = merge_event_type_dfs(dict_of_dfs, merge_dictionary)

    # If dictionary format is False, all dataframes will be concatenated into one, with many NaN columns
    if dict_format is False:
        dict_of_dfs = pd.concat([df for df in dict_of_dfs.values()])

    return dict_of_dfs
