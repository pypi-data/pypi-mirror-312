from template_log_parser.templates.debian_templates import debian_template_dict

# Base templates for Pihole log analysis

# DNSMASQ
pihole_dnsmasq_cached = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: cached {query} is {cached_resolved_ip}"
pihole_dnsmasq_compile = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: compile time options: {message}"
pihole_dnsmasq_config = (
    "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: config {host} is {result}"
)
pihole_dnsmasq_domain = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: {type} domain {query} is {result}"
pihole_dnsmasq_exactly_blacklisted = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: exactly blacklisted {query} is {result}"
pihole_dnsmasq_forward = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: forwarded {query} to {dns_server}"
pihole_dnsmasq_gravity_blocked = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: gravity blocked {query} is {result}"
pihole_dnsmasq_host_name_resolution = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: /etc/hosts {host_ip} is {host_name}"
pihole_dnsmasq_host_name = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: Pi-hole hostname {host_name} is {host_ip}"
pihole_dnsmasq_locally_known = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: using only locally-known addresses for {result}"
pihole_dnsmasq_query = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: query[{query_type}] {destination} from {client}"
pihole_dnsmasq_rate_limiting = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: Rate-limiting {query} is REFUSED (EDE: {result})"
pihole_dnsmasq_read = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: read {path} - {names} names"
pihole_dnsmasq_reply = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: reply {query} is {resolved_ip}"
pihole_dnsmasq_reply_truncated = (
    "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: reply is truncated"
)
pihole_dnsmasq_started = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: started, version {version} cachesize {cachesize}"
pihole_dnsmasq_using_nameserver = "{time} {server_name} pihole {pihole_time} dnsmasq[{id}]: using nameserver {nameserver_ip}#53"

# FTL
pihole_ftl_blocking_status = (
    "{time} {server_name} piFTL [{timestamp} {ids}] Blocking status {blocking_status}"
)
pihole_ftl_cache_resizing = '{time} {server_name} piFTL [{timestamp} {ids}] Resizing "{cache}" from {initial_size} to ({calculation}) == {new_size} ({message})'
pihole_ftl_compiled = "{time} {server_name} piFTL [{timestamp} {ids}] Compiled {whitelist} whitelist and {blacklist} blacklist regex filters for {clients} clients in {processing_time}"
pihole_ftl_reloading_dns_cache = (
    "{time} {server_name} piFTL [{timestamp} {ids}] Reloading DNS cache"
)
pihole_ftl_stats = (
    "{time} {server_name} piFTL [{timestamp} {ids}]  -> {category}: {number}"
)
pihole_ftl_sqlite_renamed = "{time} {server_name} piFTL [{timestamp} {ids}] SQLite3 message: file renamed while open: {file} ({number})"

# FTL general messages
pi_ftl_general_message = "{time} {server_name} piFTL [{timestamp} {ids}] {message}"
pi_ftl_general_message_with_category = (
    "{time} {server_name} piFTL [{timestamp} {ids}]    {category}: {message}"
)
pihole_ftl_general_message = (
    "{time} {server_name} pihole-FTL[{id}]: [{timestamp} {ids}] {message}"
)
pihole_ftl_general_message_with_category = "{time} {server_name} pihole-FTL[{id}]: [{timestamp} {ids}]    {category}: {message}"

# Dictionary of templates 'search_string' : [template, number_of_expected_values, event name]
# Some notes: use of the search string increases the speed of the parsing function
# Search string must be present in the event data for the parsing function to even attempt using a template
# Some search strings (ie: disconnected from SSID, connected to) will be present in multiple log event types
# In order to confirm that the correct template was used, its results will be tested for correct number of values
# The event name will be that value that populates the event_type column as the search string isn't terrific

pihole_dnsmasq = {
    "cached": [pihole_dnsmasq_cached, 6, "dnsmasq_cached"],
    "config": [pihole_dnsmasq_config, 6, "dnsmasq_config"],
    "compile time options": [pihole_dnsmasq_compile, 5, "dnsmasq_compile_time_options"],
    "domain": [pihole_dnsmasq_domain, 7, "dnsmasq_domain"],
    "exactly blacklisted": [
        pihole_dnsmasq_exactly_blacklisted,
        6,
        "pihole_exact_blacklist",
    ],
    "forwarded": [pihole_dnsmasq_forward, 6, "dnsmasq_forward"],
    "gravity blocked": [pihole_dnsmasq_gravity_blocked, 6, "dnsmasq_gravity_blocked"],
    "hosts": [pihole_dnsmasq_host_name_resolution, 6, "dnsmasq_hostname_resolution"],
    "hostname": [pihole_dnsmasq_host_name, 6, "dnsmasq_hostname_resolution"],
    "locally-known": [pihole_dnsmasq_locally_known, 5, "dnsmasq_locally_known"],
    "query": [pihole_dnsmasq_query, 7, "dnsmasq_query"],
    "Rate-limiting": [pihole_dnsmasq_rate_limiting, 6, "dnsmasq_rate_limiting"],
    "read ": [pihole_dnsmasq_read, 6, "dnsmasq_read"],
    "reply": [pihole_dnsmasq_reply, 6, "dnsmasq_reply"],
    "reply is truncated": [
        pihole_dnsmasq_reply_truncated,
        4,
        "dnsmasq_reply_truncated",
    ],
    "started": [pihole_dnsmasq_started, 6, "dnsmasq_started"],
    "using nameserver": [
        pihole_dnsmasq_using_nameserver,
        5,
        "dnsmasq_using_nameserver",
    ],
}

pihole_ftl = {
    "Blocking status": [pihole_ftl_blocking_status, 5, "ftl_blocking_status"],
    "Resizing": [pihole_ftl_cache_resizing, 9, "ftl_cache_resizing"],
    "Compiled": [pihole_ftl_compiled, 8, "ftl_compiled"],
    "Reloading DNS cache": [
        pihole_ftl_reloading_dns_cache,
        4,
        "ftl_reloading_dns_cache",
    ],
    "->": [pihole_ftl_stats, 6, "ftl_stats"],
    "SQLite3 message": [pihole_ftl_sqlite_renamed, 6, "ftl_sqlite_rename"],
    # General messages that are not accounted for with other templates
    " pihole-FTL": [
        pihole_ftl_general_message_with_category,
        7,
        "ftl_general_category_message",
    ],
    " piFTL": [
        pi_ftl_general_message_with_category,
        6,
        "pi_ftl_general_category_message",
    ],
    "pihole-FTL": [pihole_ftl_general_message, 6, "ftl_general_message"],
    "piFTL": [pi_ftl_general_message, 5, "pi_ftl_general_message"],
}


pihole_events_dict = {**pihole_dnsmasq, **pihole_ftl}


# Pihole often runs on debian, so it makes sense to use templates from that dictionary rather than create new ones
pihole_template_dict = {**debian_template_dict, **pihole_events_dict}

# Additional Dictionaries
# Merging events for consolidation
pihole_merge_events_dict = {
    "dnsmasq": [value[2] for value in pihole_dnsmasq.values()],
    "ftl": [value[2] for value in pihole_ftl.values()],
}
