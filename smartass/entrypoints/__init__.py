




def _get_not_configured_usage_tracker_path():
    """Returns path of special file where we store latest shell pid."""
    return Path(gettempdir()).joinpath(u'thefuck.last_not_configured_run_{}'.format(
        getpass.getuser(),
    ))


def _record_first_run():
    """Records shell pid to tracker file."""
    info = {'pid': _get_shell_pid(),
            'time': time.time()}

    mode = 'wb' if six.PY2 else 'w'
    with _get_not_configured_usage_tracker_path().open(mode) as tracker:
        json.dump(info, tracker)


def main():
    """Shows useful information about how-to configure alias on a first run
    and configure automatically on a second.

    It'll be only visible when user type fuck and when alias isn't configured.

    """
    settings.init()
    configuration_details = shell.how_to_configure()
    if (
        configuration_details and
        configuration_details.can_configure_automatically
    ):
        if _is_already_configured(configuration_details):
            logs.already_configured(configuration_details)
            return
        elif _is_second_run():
            _configure(configuration_details)
            logs.configured_successfully(configuration_details)
            return
        else:
            _record_first_run()

    logs.how_to_configure_alias(configuration_details)