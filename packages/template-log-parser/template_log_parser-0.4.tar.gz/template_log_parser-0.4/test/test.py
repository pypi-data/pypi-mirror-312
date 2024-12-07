import unittest

import pandas as pd
from parse import parse

from template_log_parser.column_functions import (
    split_name_and_mac,
    calc_time,
    calc_data_usage,
    isolate_ip_from_parentheses,
)

from template_log_parser.log_functions import (
    parse_function,
    log_pre_process,
    run_functions_on_columns,
    process_event_types,
    merge_event_type_dfs,
    process_log,
)

from template_log_parser.log_functions import (
    event_type_column,
    event_data_column,
    parsed_info_column,
    other_type_column,
    unparsed_text_column,
)

from template_log_parser.sample import sample_df

from template_log_parser.log_type_classes import built_in_log_file_types


class TestColumnFunctions(unittest.TestCase):
    """Defines a class to test functions that are run on columns"""

    def test_split_name_and_mac(self):
        """Test function to determine name:mac returns two strings, unnamed if client name not included"""
        client_name = "client_device"

        mac_without_name = "10-F7-D6-07-BD-8A"
        with_name = client_name + ":" + mac_without_name

        # In any case a tuple should be returned
        self.assertIsInstance(split_name_and_mac(mac_without_name), tuple)
        self.assertIsInstance(split_name_and_mac(with_name), tuple)

        no_name, no_name_mac = split_name_and_mac(mac_without_name)
        name, mac = split_name_and_mac(with_name)

        # All items within tuples should be strings
        for item in [no_name, no_name_mac, name, mac]:
            self.assertIsInstance(item, str)

        # Assert correct values for each variable
        self.assertEqual(no_name, "unnamed")
        self.assertEqual(no_name_mac, mac_without_name)
        self.assertEqual(name, client_name)
        self.assertEqual(mac, mac_without_name)

    def test_calc_time(self):
        """Test function to ensure correct float values are returned from generic time counts"""
        time_with_hours = "1h30m"
        time_minutes = "15m"
        # times below one minute will get rounded up to one for simplicity
        time_seconds = "60s"

        time_from_hours_to_seconds = calc_time(time_with_hours, increment="seconds")
        time_from_hours_to_minutes = calc_time(time_with_hours, increment="minutes")
        time_from_hours_to_hours = calc_time(time_with_hours, increment="hours")

        time_from_minutes_to_seconds = calc_time(time_minutes, increment="seconds")
        time_from_minutes_to_minutes = calc_time(time_minutes, increment="minutes")
        time_from_minutes_to_hours = calc_time(time_minutes, increment="hours")

        time_from_seconds_to_seconds = calc_time(time_seconds, increment="seconds")
        time_from_seconds_to_minutes = calc_time(time_seconds, increment="minutes")
        time_from_seconds_to_hours = calc_time(time_seconds, increment="hours")

        all_conversions = [
            time_from_hours_to_seconds,
            time_from_hours_to_minutes,
            time_from_hours_to_hours,
            time_from_minutes_to_seconds,
            time_from_minutes_to_minutes,
            time_from_minutes_to_hours,
            time_from_seconds_to_seconds,
            time_from_seconds_to_minutes,
            time_from_seconds_to_hours,
        ]

        # Assert function returns floats in all instances
        for conversion in all_conversions:
            self.assertIsInstance(conversion, float)

        correct_values = [5400, 90, 1.5, 900, 15, 0.25, 60, 1, (1 / 60)]

        for tup in zip(all_conversions, correct_values):
            self.assertEqual(tup[0], tup[1])

    # noinspection PyPep8Naming
    def test_calc_data_usage(self):
        """Defines a test function to ensure correct MB float values are return from generic data usage strings"""
        bytes_amount = "100 bytes"
        kilobytes = "500KB"
        megabytes = "250 MB"
        gigabytes = "10GB"

        data_from_bytes_to_KB = calc_data_usage(bytes_amount, "KB")
        data_from_bytes_to_MB = calc_data_usage(bytes_amount, "MB")
        data_from_bytes_to_GB = calc_data_usage(bytes_amount, "GB")

        data_from_kilobytes_to_KB = calc_data_usage(kilobytes, "KB")
        data_from_kilobytes_to_MB = calc_data_usage(kilobytes, "MB")
        data_from_kilobytes_to_GB = calc_data_usage(kilobytes, "GB")

        data_from_megabytes_to_KB = calc_data_usage(megabytes, "KB")
        data_from_megabytes_to_MB = calc_data_usage(megabytes, "MB")
        data_from_megabytes_to_GB = calc_data_usage(megabytes, "GB")

        data_from_gigabytes_to_KB = calc_data_usage(gigabytes, "KB")
        data_from_gigabytes_to_MB = calc_data_usage(gigabytes, "MB")
        data_from_gigabytes_to_GB = calc_data_usage(gigabytes, "GB")

        all_conversions = [
            data_from_bytes_to_KB,
            data_from_bytes_to_MB,
            data_from_bytes_to_GB,
            data_from_kilobytes_to_KB,
            data_from_kilobytes_to_MB,
            data_from_kilobytes_to_GB,
            data_from_megabytes_to_KB,
            data_from_megabytes_to_MB,
            data_from_megabytes_to_GB,
            data_from_gigabytes_to_KB,
            data_from_gigabytes_to_MB,
            data_from_gigabytes_to_GB,
        ]

        for conversion in all_conversions:
            # Assert functions returns float values
            self.assertIsInstance(conversion, float)

        correct_values = [
            0.1,
            1e-4,
            1e-7,
            500,
            0.5,
            0.0005,
            250000,
            250,
            0.25,
            1e7,
            10000,
            10,
        ]

        for tup in zip(all_conversions, correct_values):
            self.assertEqual(tup[0], tup[1])

    def test_isolate_ip_from_parentheses(self):
        """Defines a test function to ensure ip addresses are being correctly extracted from string data"""
        ip_with_workgroup = "WORKGROUP(10.20.10.39)"
        ip_in_parentheses = "(10.45.1.32)"
        ipv6_with_client = "client1(fb71::8520:aa9e:dad4:62f3)"
        ipv4_with_client = "client2(10.0.0.101)"
        clean_ip = "127.0.0.1"

        ip_with_workgroup_isolated = isolate_ip_from_parentheses(ip_with_workgroup)
        ip_in_parentheses_isolated = isolate_ip_from_parentheses(ip_in_parentheses)
        ipv6_with_client_isolated = isolate_ip_from_parentheses(ipv6_with_client)
        ipv4_with_client_isolated = isolate_ip_from_parentheses(ipv4_with_client)
        clean_ip_isolated = isolate_ip_from_parentheses(clean_ip)

        self.assertEqual(ip_with_workgroup_isolated, "10.20.10.39")
        self.assertEqual(ip_in_parentheses_isolated, "10.45.1.32")
        self.assertEqual(ipv6_with_client_isolated, "fb71::8520:aa9e:dad4:62f3")
        self.assertEqual(ipv4_with_client_isolated, "10.0.0.101")
        self.assertEqual(clean_ip_isolated, clean_ip)


class TestLogFunctions(unittest.TestCase):
    """Defines a class to test functions that process overall log files"""

    def test_parse_function(self):
        """Test function to assert that parse function is returning a string event type and a dictionary of results"""
        # Known event type with a verified template
        # Should return tuple of string and dict respectively
        simple_event = (
            "2024-09-12T00:28:49.037352+01:00 gen_controller  2024-09-11 16:28:44 Controller - - - "
            "user logged in to the controller from 172.0.0.1."
        )

        simple_template = (
            "{timestamp} {controller_name}  {local_time} Controller - - - "
            "{username} logged in to the controller from {ip}."
        )

        simple_template_dict = {"logged in": [simple_template, 5, "login"]}

        self.assertIsInstance(parse_function(simple_event, simple_template_dict), tuple)
        event_type, results = parse_function(simple_event, simple_template_dict)
        self.assertIsInstance(event_type, str)
        self.assertIsInstance(results, dict)
        self.assertEqual(event_type, "login")

        # Should return tuple, then string and dict respectively
        anomalous_event = "This event does not match any template."
        self.assertIsInstance(
            parse_function(anomalous_event, simple_template_dict), tuple
        )
        # Unknown event type should also pass without error, return str, dict
        event_type_2, results_2 = parse_function(anomalous_event, simple_template_dict)
        self.assertIsInstance(event_type_2, str)
        self.assertIsInstance(results_2, dict)
        # Should return other event type
        self.assertEqual(event_type_2, other_type_column)
        # The key to its dict should be unparsed_text_column
        self.assertEqual(list(results_2.keys()), [unparsed_text_column])

    def test_log_pre_process(self):
        """Test function to assert that log_pre_process returns a Pandas DataFrame with the correct three columns"""
        # Check against all built-in log file types
        for built_in in built_in_log_file_types:
            print(built_in.name, " test log_pre_process")
            # Generate pre_process df using built_in sample_log_file and templates
            df = log_pre_process(built_in.sample_log_file, built_in.templates)
            # Assert df instance, and the existence of correct three columns
            self.assertIsInstance(df, pd.DataFrame)
            self.assertTrue(
                (
                    [event_data_column, event_type_column, parsed_info_column]
                    == df.columns
                ).all()
            )

            # Assert all columns hold correct data structures
            for index, row in df.iterrows():
                self.assertIsInstance(row[event_data_column], str)
                self.assertIsInstance(row[event_type_column], str)
                # parsed_info should be a column of dictionaries
                self.assertIsInstance(row[parsed_info_column], dict)

            # Assert df has the same number of lines as the original log file
            print("checking log file length against Dataframe shape")
            with open(built_in.sample_log_file, "r") as raw_log:
                lines = len(raw_log.readlines())
                print("lines in logfile: ", lines)
                self.assertEqual(lines, df.shape[0])
                print("rows in dataframe: ", df.shape[0])
                # Assert template dictionary has the same number of items as the log file has lines
                self.assertEqual(len(built_in.templates), lines)
                print("length of template dictionary: ", len(built_in.templates))
            if other_type_column in df[event_type_column].tolist():
                print(df[df[event_type_column] == other_type_column])

            # Assert no "Other" event types
            self.assertTrue(other_type_column not in df[event_type_column].tolist())

            # Assert all event types are present in the df, equal to the template dictionary values, third item
            self.assertEqual(
                sorted(list([event[2] for event in built_in.templates.values()])),
                sorted(df[event_type_column].tolist()),
            )
            print("    log_pre_process ok")

    def test_run_functions_on_columns(self):
        """Defines a test function to ensure run functions on columns is operating correctly"""

        df = sample_df.copy()

        # In order to pass arguments to column functions, kwargs dictionary is created
        data_usage_kwargs = dict(increment="GB")

        # Using all built-in column functions, add in one column that doesn't exist to ensure no error
        function_dict = {
            "column_that_does_not_exist": [len, "fake_column_name"],
            "data": [calc_data_usage, "data_MB", data_usage_kwargs],
            "client_name_and_mac": [split_name_and_mac, ["client_name", "client_mac"]],
            "time_elapsed": [calc_time, "time_min"],
            "ip_address_raw": [isolate_ip_from_parentheses, "ip_address_fixed"],
        }

        # Assert function returns a tuple
        self.assertIsInstance(
            run_functions_on_columns(
                df.copy(),
                additional_column_functions=function_dict,
                datetime_columns=["utc_time", "time"],
                localize_timezone_columns=["time"],
            ),
            tuple,
        )

        df, list_of_columns = run_functions_on_columns(
            df.copy(),
            additional_column_functions=function_dict,
            datetime_columns=["utc_time", "time"],
            localize_timezone_columns=["time"],
        )

        # Assert variables are df and list respectively
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIsInstance(list_of_columns, list)

        # Assert the expected columns are present
        self.assertTrue(
            (
                [column for column in sample_df.columns]
                + [
                    "data_MB",
                    "client_name",
                    "client_mac",
                    "time_min",
                    "ip_address_fixed",
                ]
                == df.columns
            ).all()
        )

        # Assert newly created columns have the correct data types
        for index, row in df.iterrows():
            self.assertIsInstance(row["data_MB"], float)
            self.assertIsInstance(row["client_name"], str)
            self.assertIsInstance(row["client_mac"], str)
            self.assertIsInstance(row["time_min"], float)
            self.assertIsInstance(row["ip_address_fixed"], str)

        # Assert timezone and no timezone for applicable datetime columns
        self.assertTrue(df["utc_time"].dt.tz is not None)
        self.assertTrue(df["time"].dt.tz is None)

        # Assert return list of columns is equal to the keys from the column function dict EXCEPT 'column_that_does_not_exist'
        self.assertEqual(
            list_of_columns,
            [
                column
                for column in function_dict.keys()
                if column != "column_that_does_not_exist"
            ],
        )

        # If a df is passed without any arguments, the same df should return along with an empty list
        no_changes_df, empty_list = run_functions_on_columns(df.copy())
        # Return df should equal the original df
        self.assertTrue(no_changes_df.equals(df))
        self.assertTrue(len(empty_list) == 0)

    def test_process_event_types(self):
        """Defines a function to assert that process_event_types returns a dictionary of dfs correctly"""

        # Using all built ins
        for built_in in built_in_log_file_types:
            print(built_in.name, " test process_event_types")
            # Create sample df with correct three columns
            df = log_pre_process(built_in.sample_log_file, built_in.templates)

            # First run, using drop columns, and setting datetime columns
            print("    Using drop columns")
            dict_of_df = process_event_types(
                df.copy(),
                built_in.column_functions,
                datetime_columns=built_in.datetime_columns,
                localize_timezone_columns=built_in.localize_datetime_columns,
                drop_columns=True,
            )

            # Assert a dictionary was returned
            self.assertIsInstance(dict_of_df, dict)
            # Assert list of dictionaries matches a list of unique event types from the original df
            self.assertEqual(
                (list(dict_of_df.keys())), df[event_type_column].unique().tolist()
            )

            # Set of columns that were processed
            if built_in.column_functions:
                drop_columns_list = list(built_in.column_functions.keys())
                drop_columns = set(drop_columns_list)
            else:
                drop_columns_list = []
                drop_columns = set(drop_columns_list)

            # Loop over all dfs
            for df in dict_of_df.values():
                # Assert each value is a pandas DataFrame
                self.assertIsInstance(df, pd.DataFrame)
                # Assert that the intersection of the two sets (drop_columns and df.columns) is empty, having len 0
                # Meaning columns were dropped correctly
                self.assertTrue(len(drop_columns.intersection(set(df.columns))) == 0)
                # Assert timezone and no timezone for applicable datetime columns, "Other" df wouldn't have these columns
                if built_in.datetime_columns:
                    for column in built_in.datetime_columns:
                        if column in df.columns:
                            # Assert column is ANY form of pandas datetime, accounting for all formats
                            self.assertTrue(
                                pd.api.types.is_datetime64_any_dtype(df[column])
                            )
                if built_in.localize_datetime_columns:
                    for column in built_in.localize_datetime_columns:
                        if column in df.columns:
                            self.assertTrue(df[column].dt.tz is None)
            print("    ok")
            # New df
            print("    Not using drop columns")
            new_df = log_pre_process(built_in.sample_log_file, built_in.templates)
            # Do not drop columns on this run
            non_drop_dict_of_df = process_event_types(
                new_df.copy(), built_in.column_functions, drop_columns=False
            )
            # Not all processed columns would be present in every df, so this step creates one large df
            concat_df = pd.concat([df for df in non_drop_dict_of_df.values()])
            # Verify that every column is still present within the large df, meaning not dropped
            for column in drop_columns_list:
                self.assertTrue(column in concat_df.columns)
            print("    ok")
            print("    process_event_types ok")

    def test_merge_event_type_dfs(self):
        """Defines a test function to assert that dfs specified to be merged are done so correctly"""
        # Using all built_ins
        for built_in in built_in_log_file_types:
            # First create dictionary of dfs:
            pre_df = log_pre_process(built_in.sample_log_file, built_in.templates)
            # No column manipulation or dropping for this test as it is addressed in other test functions
            dict_of_dfs = process_event_types(pre_df.copy())

            # Merge events, if dictionary is present
            if built_in.merge_events:
                dict_of_dfs = merge_event_type_dfs(dict_of_dfs, built_in.merge_events)
                # After the procedure assert the new_df name is present as a key
                for new_df, old_dfs in built_in.merge_events.items():
                    self.assertTrue(new_df in dict_of_dfs.keys())
                    # Assert old df names are no longer present as keys
                    for old_df in old_dfs:
                        self.assertTrue(old_df not in dict_of_dfs.keys())

    def test_process_log(self):
        """Defines a function to determine that process_log() return proper keys/columns in every scenario"""

        # This is a really nasty way of testing all the output combinations, but it works for now

        # All built in log template classes
        for built_in in built_in_log_file_types:
            print(built_in.name, " test process_log")
            # Opting to type 8 configurations visually for ease of viewing instead of using itertools
            funcs_merges_drop = [built_in.column_functions, built_in.merge_events, True]
            funcs_no_merges_drop = [built_in.column_functions, None, True]
            funcs_merges_no_drop = [
                built_in.column_functions,
                built_in.merge_events,
                False,
            ]
            funcs_no_merge_no_drop = [built_in.column_functions, None, False]
            no_funcs_merges_no_drop = [None, built_in.merge_events, False]
            no_funcs_merges_drop = [None, built_in.merge_events, True]
            no_funcs_no_merges_drop = [None, None, True]
            no_funcs_no_merges_no_drop = [None, None, False]

            base_list = [
                funcs_merges_drop,
                funcs_no_merges_drop,
                funcs_merges_no_drop,
                funcs_no_merge_no_drop,
                no_funcs_merges_no_drop,
                no_funcs_merges_drop,
                no_funcs_no_merges_drop,
                no_funcs_no_merges_no_drop,
            ]

            # All base configuration with False appended to the end (dict_format=False)
            df_configurations = [configuration + [False] for configuration in base_list]

            # All base configuration with True append to the end (dict_format=True)
            dict_configurations = [
                configuration + [True] for configuration in base_list
            ]

            # Each configuration is a list:
            # [additional_column_functions (or None), merge_dictionary (or None), drop_columns True/False, dict_format True/False]
            def test_correct_dict_keys(merge_events=None):
                """Defines a function to determine expected keys for a given dictionary"""
                # Using the template dict, the event_type is the third item [2] in the list
                expected_keys = [value[2] for value in built_in.templates.values()]

                if merge_events:
                    # The keys to the merge_events dict are added to the main dict
                    new_merge_events = [key for key in built_in.merge_events.keys()]
                    columns_to_delete = []
                    # The values of the merge_event dict is a list of event_types that were merged (and deleted)
                    for deleted_column_list in merge_events.values():
                        columns_to_delete.extend(deleted_column_list)
                    expected_keys = [
                        column
                        for column in expected_keys
                        if column not in columns_to_delete
                    ]
                    expected_keys.extend(new_merge_events)

                # Set to remove duplicates, then back to list
                # Sort the resulting list for easier assertion evaluation
                expected_keys = sorted(list(set(expected_keys)))
                return expected_keys

            def test_correct_mini_df_columns(
                event_type_key, additional_column_functions, merge_events, drop_columns
            ):
                """Defines a function to determine correct columns for an event_type df present within larger dict"""

                # Running parse on individual templates against template dictionary in a comprehension
                # to return {'event_type': [column1, column2,...], ...}
                # Every event_type now has a list of columns associated with it, adding 'event_type' at the end
                expected_columns_by_template = {
                    value[2]: list(parse(value[0], value[0]).named.keys())
                    + [event_type_column]
                    for value in built_in.templates.values()
                }

                # Expected columns are empty to avoid pre-assignment error
                expected_columns = []

                # If there are no merge events, the expected columns by template covers the situation
                if merge_events is None:
                    expected_columns = expected_columns_by_template[event_type_key]

                elif merge_events:
                    # Look for event in merge_events dictionary keys
                    if event_type_key in merge_events.keys():
                        # These are all the columns from 2+ event types that were merged, creates list of lists
                        merged_column_lists = [
                            expected_columns_by_template[old_column]
                            for old_column in merge_events[event_type_key]
                        ]
                        # Comprehension to unpack all items from their lists into one large list, list of a set to remove duplicates
                        merged_columns = list(
                            set(
                                [
                                    column
                                    for column_list in merged_column_lists
                                    for column in column_list
                                ]
                            )
                        )
                        expected_columns = merged_columns
                    # Otherwise use expected_columns_by_template if event isn't in merge_events
                    else:
                        expected_columns = expected_columns_by_template[event_type_key]

                # By default, there are no columns to add or delete
                columns_to_add = []
                columns_to_delete = []

                # If column functions are present
                if additional_column_functions:
                    # Check to see if column is present in the functions dictionary
                    for column in expected_columns:
                        # Column functions can create a single new column or multiple columns
                        # Once determined single or multiple, append/extend to columns_to_add
                        if column in additional_column_functions.keys():
                            if type(additional_column_functions[column][1]) is str:
                                columns_to_add.append(
                                    additional_column_functions[column][1]
                                )
                            if type(additional_column_functions[column][1]) is list:
                                columns_to_add.extend(
                                    additional_column_functions[column][1]
                                )
                            # Original column that was used to provide data for the function appended to delete columns
                            columns_to_delete.append(column)

                # event_data and parsed_info are the only two dropped columns by default
                standard_drop_columns = [event_data_column, parsed_info_column]
                all_columns_to_drop = []

                if drop_columns is True:
                    all_columns_to_drop = standard_drop_columns + columns_to_delete

                elif drop_columns is False:
                    columns_to_add.extend(standard_drop_columns)

                expected_columns.extend(columns_to_add)

                expected_columns = sorted(
                    [
                        column
                        for column in expected_columns
                        if column not in all_columns_to_drop
                    ]
                )
                expected_columns = sorted(list(set(expected_columns)))

                return expected_columns

            def test_correct_big_df_columns(additional_column_functions, drop_columns):
                """Defines a function to determine the correct columns for a large log file df"""
                columns_accounted_for_by_templates = [
                    list(parse(value[0], value[0]).named.keys())
                    for value in built_in.templates.values()
                ]

                # Remove duplicates, this is a list of all possible columns
                columns_accounted_for_by_templates = list(
                    set(
                        [
                            column
                            for column_list in columns_accounted_for_by_templates
                            for column in column_list
                        ]
                        + [event_type_column]
                    )
                )

                standard_drop_columns = [event_data_column, parsed_info_column]
                columns_to_add = []
                columns_to_delete = []

                # New column or columns created by functions, add/extend accordingly
                # Second item in the function_info list will be either a string or list for new column(s)
                if additional_column_functions:
                    for (
                        old_column,
                        function_info,
                    ) in additional_column_functions.items():
                        columns_to_delete.append(old_column)
                        if type(function_info[1]) is str:
                            columns_to_add.append(function_info[1])
                        if type(function_info[1]) is list:
                            columns_to_add.extend(function_info[1])

                if drop_columns is True:
                    columns_to_delete = columns_to_delete + standard_drop_columns

                elif drop_columns is False:
                    columns_to_add.extend(standard_drop_columns)
                    # If drop columns is False, re-define columns to delete as en empty list
                    columns_to_delete = []

                columns_accounted_for_by_templates.extend(columns_to_add)

                # Remove duplicates once again just to be safe and sort
                expected_columns = sorted(
                    list(
                        set(
                            [
                                column
                                for column in columns_accounted_for_by_templates
                                if column not in columns_to_delete
                            ]
                        )
                    )
                )

                return expected_columns

            # Using the sample log for this test
            with open(built_in.sample_log_file, "r") as raw_log:
                lines_in_log_file = len(raw_log.readlines())

            # 8 total configurations for dictionary output
            for config in dict_configurations:
                print("    Dictionary Output")
                print("    Configuration: ", config)
                big_dict = process_log(
                    file=built_in.sample_log_file,
                    template_dictionary=built_in.templates,
                    additional_column_functions=config[0],
                    merge_dictionary=config[1],
                    drop_columns=config[2],
                    dict_format=config[3],
                )

                expected_correct_keys = test_correct_dict_keys(config[1])

                self.assertTrue(expected_correct_keys == sorted(list(big_dict.keys())))
                print("    Matching Keys ok")

                total_log_lines_accounted_for = 0

                # Check each df within the dictionary
                for event_type, df in big_dict.items():
                    print("       ", event_type)
                    self.assertIsInstance(event_type, str)
                    self.assertIsInstance(df, pd.DataFrame)

                    expected_correct_columns = test_correct_mini_df_columns(
                        event_type_key=event_type,
                        additional_column_functions=config[0],
                        merge_events=config[1],
                        drop_columns=config[2],
                    )

                    self.assertTrue(
                        expected_correct_columns == sorted(df.columns.tolist())
                    )
                    print("        Mini DF Matching Columns ok")

                    total_log_lines_accounted_for = (
                        total_log_lines_accounted_for + df.shape[0]
                    )

                self.assertEqual(total_log_lines_accounted_for, lines_in_log_file)
                print("    All log file lines accounted for")
            print("    Dictionary Outputs ok")

            # 8 Total configurations for DF output
            for config in df_configurations:
                print("    DF Output")
                print("    Configuration: ", config)
                big_df = process_log(
                    file=built_in.sample_log_file,
                    template_dictionary=built_in.templates,
                    additional_column_functions=config[0],
                    merge_dictionary=config[1],
                    drop_columns=config[2],
                    dict_format=config[3],
                )

                self.assertIsInstance(big_df, pd.DataFrame)

                correct_df_columns = test_correct_big_df_columns(
                    additional_column_functions=config[0],
                    drop_columns=config[2],
                )

                self.assertTrue(correct_df_columns == sorted(big_df.columns.tolist()))
                print("    Matching Columns ok")

                self.assertEqual(big_df.shape[0], lines_in_log_file)
                print("    All log file lines accounted for")

                self.assertEqual(lines_in_log_file, big_df.shape[0])
            print("    process_log ok")
