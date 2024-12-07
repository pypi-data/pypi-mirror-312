from template_log_parser.column_functions import (
    calc_data_usage,
    isolate_ip_from_parentheses,
)
# Base templates for Synology log analysis

# Tasks
backup_task = "{time} {server_name} {package_name} {system_user}:#011[{type}][{task_name}] {message}"
backup_version_rotation = "{time} {server_name} {package_name} {system_user}:#011[{task_name}] Trigger version rotation."
scheduled_task_message = "{time} {server_name} System {system_user}:#011Scheduled Task [{task_name}] {message}"
hyper_backup_task_message = "{time} {server_name} Hyper_Backup: {system_user}:#011Backup task [{task_name}] {message}"
task_setting = (
    "{time} {server_name} {package_name}: {system_user}:#011Setting of {message}"
)
credentials_changed = "{time} {server_name} {package_name} {system_user}:#011[{type}] Credentials changed on the destination."

# General System
auto_install = "{time} {server_name} System {system_user}:#011Start install [{package}] automatically."
back_online = "{time} {server_name} System {system_user}:#011Server back online."
countdown_reboot = "{time} {server_name} System {system_user}:#011System started counting down to reboot."
download_task = (
    "{time} {server_name} System {system_user}:#011Download task for [{task}] {result}."
)
link_state = "{time} {server_name} System {system_user}:#011[{interface}] link {state}."
on_battery = "{time} {server_name} System {system_user}:#011Server is on battery."
package_change = "{time} {server_name} System {system_user}:#011Package [{package}] has been successfully {state}."
process_start_or_stop = (
    "{time} {server_name} System: System successfully {result} [{process}]."
)
scrubbing = "{time} {server_name} System {system_user}:#011System {state} {type} scrubbing on [{location}]."
service_started_or_stopped = (
    "{time} {server_name} System {system_user}:#011[{service}] service was {state}."
)
restarted_service = "{time} {server_name} System {system_user}:#011System successfully restarted {service} service."
shared_folder = "{time} {server_name} System {system_user}:#011{kind} shared folder [{shared_folder}] {message}"
setting_enabled = (
    "{time} {server_name} System {system_user}:#011[{setting}] was enabled."
)
update = "{time} {server_name} System {system_user}:#011Update was {result}."

# User Activity
blocked = "{time} {server_name} System {user}:#011Host [{client_ip}] was blocked via [{service}]."
unblock = "{time} {server_name} System {system_user}:#011Delete host IP [{client_ip}] from Block List."
login = "{time} {server_name} Connection: User [{user}] from [{client_ip}] logged in successfully via [{method}]."
failed_login = "{time} {server_name} Connection: User [{user}] from [{client_ip}] failed to log in via [{method}] due to authorization failure."
failed_host_connection = "{time} {server_name} Connection: Host [{client_ip}] failed to connect via [{service}] due to [{message}]."
logout = "{time} {server_name} Connection: User [{user}] from [{client_ip}] logged out the server via [{method}] with totally [{data_uploaded}] uploaded and [{data_downloaded}] downloaded."
sign_in = "{time} {server_name} Connection: User [{user}] from [{client_ip}] signed in to [{service}] successfully via [{auth_method}]."
failed_sign_in = "{time} {server_name} Connection: User [{user}] from [{client_ip}] failed to sign in to [{service}] via [{auth_method}] due to authorization failure."
folder_access = "{time} {server_name} Connection: User [{user}] from [{client_ip}] via [{method}] accessed shared folder [{folder}]."
cleared_notifications = "{time} {server_name} System {system_user}:#011Cleared [{user}] all notifications successfully."
new_user = (
    "{time} {server_name} System {system_user}:#011User [{created_user}] was created."
)
user_app_privilege = "{time} {server_name} System {system_user}:#011The app privilege on app [{app}] for user [{user}] was set to [{privilege}] from [{client_ip}]."
user_group = "{time} {server_name} System {system_user}:#011User [{user}] was {action} the group [{group}]."
win_file_service_event = "{time} {server_name} WinFileService Event: {event}, Path: {path}, File/Folder: {file_or_folder}, Size: {size}, User: {user}, IP: {client_ip}"

# Dictionary of templates 'search_string' : [template, number_of_expected_values, event name]
# Some notes: use of the search string greatly increases the speed of the parsing function
# Search string must be present in the event data for the parsing function to even attempt using a template
# Some search strings will be present in multiple log event types
# In order to confirm that the correct template was used, its results will be tested for correct number of values
# The event name will be that value that populates the event_type column as the search string isn't terrific

tasks_dict = {
    "Backup": [backup_task, 7, "backup_task"],
    "version rotation": [backup_version_rotation, 5, "backup_version_rotation"],
    "Backup task": [hyper_backup_task_message, 5, "task_message"],
    "Scheduled Task": [scheduled_task_message, 5, "task_message"],
    "Setting": [task_setting, 5, "task_setting"],
    "Credentials changed": [credentials_changed, 5, "credentials_changed"],
}

general_system_dict = {
    "automatically": [auto_install, 4, "auto_install"],
    "back online": [back_online, 3, "back_online"],
    "counting down": [countdown_reboot, 3, "countdown_reboot"],
    "Download task": [download_task, 5, "download_task"],
    "link": [link_state, 5, "link_state"],
    "Package": [package_change, 5, "package_change"],
    "scrubbing": [scrubbing, 6, "scrubbing"],
    "System successfully": [process_start_or_stop, 4, "process_start_or_stop"],
    "service was": [service_started_or_stopped, 5, "service_start_or_stop"],
    "successfully restarted": [restarted_service, 4, "restarted_service"],
    "on battery": [on_battery, 3, "on_battery"],
    "Update": [update, 4, "update"],
    "shared folder": [shared_folder, 6, "shared_folder"],
    "was enabled": [setting_enabled, 4, "setting_enabled"],
}

user_activity_dict = {
    "blocked": [blocked, 5, "host_blocked"],
    "from Block List": [unblock, 4, "host_unblocked"],
    "Cleared": [cleared_notifications, 4, "cleared_notifications"],
    "failed to connect": [failed_host_connection, 5, "failed_host_connection"],
    "failed to log in": [failed_login, 5, "failed_login"],
    "failed to sign in": [failed_sign_in, 6, "failed_sign_in"],
    "accessed shared folder": [folder_access, 6, "folder_access"],
    "logged in successfully via": [login, 5, "login"],
    "logged out the server": [logout, 7, "logout"],
    "signed in to": [sign_in, 6, "sign_in"],
    "was created": [new_user, 4, "new_user"],
    "app privilege": [user_app_privilege, 7, "user_app_privilege"],
    "group": [user_group, 6, "user_group"],
    "WinFileService Event": [win_file_service_event, 8, "win_file_service_event"],
}

synology_template_dict = {**tasks_dict, **general_system_dict, **user_activity_dict}


# Additional Dictionaries

synology_column_process_dict = {
    "data_uploaded": [calc_data_usage, "data_uploaded_MB"],
    "data_downloaded": [calc_data_usage, "data_download_MB"],
    "client_ip": [isolate_ip_from_parentheses, "client_ip_address"],
}

# Merging events for consolidation
synology_merge_events_dict = {
    "tasks": [value[2] for value in tasks_dict.values()],
    "general_system": [value[2] for value in general_system_dict.values()],
    "user_activity": [value[2] for value in user_activity_dict.values()],
}
