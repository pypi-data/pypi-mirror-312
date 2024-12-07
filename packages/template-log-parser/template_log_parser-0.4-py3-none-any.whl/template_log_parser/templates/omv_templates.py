from template_log_parser.templates.debian_templates import debian_template_dict

# Base templates for Open Media Vault log analysis

openmediavault_process = "{time} {server_name} openmediavault-{process} {message}"
omv_process = "{time} {server_name} omv-{process}: {message}"

# Dictionary of templates 'search_string' : [template, number_of_expected_values, event name]
# Some notes: use of the search string increases the speed of the parsing function
# Search string must be present in the event data for the parsing function to even attempt using a template
# Some search strings (ie: disconnected from SSID, connected to) will be present in multiple log event types
# In order to confirm that the correct template was used, its results will be tested for correct number of values
# The event name will be that value that populates the event_type column as the search string isn't terrific

omv_template_dict_events = {
    "openmediavault-": [openmediavault_process, 4, "openmediavault_process"],
    "omv-": [omv_process, 4, "omv_process"],
}

# OMV often runs on debian, so it makes sense to use templates from that dictionary rather than create new ones
omv_template_dict = {**debian_template_dict, **omv_template_dict_events}
