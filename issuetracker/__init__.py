default_app_config = 'issuetracker.apps.IssuetrackerAppConfig'
VERSION = ('16', '04', '0', 'dev', '0')


def get_version():
    """ Builds readable version from VERSION tuple.
    If the flag part evaluates to true it is added to the version.
    """
    if VERSION[3]:
        return '{year}.{month}.{flag}'.format(
            year=VERSION[0],
            month=VERSION[1],
            flag=VERSION[3]
        )
    return '{year}.{month}'.format(
        year=VERSION[0],
        month=VERSION[1]
    )


def get_release():
    """ Builds readable release from VERSION tuple.
    If the flag part evaluates to true it is added to the version with the
    suffix.
    """
    if VERSION[3]:
        return '{year}.{month}.{patch}.{flag}{suffix}'.format(
            year=VERSION[0],
            month=VERSION[1],
            patch=VERSION[2],
            flag=VERSION[3],
            suffix=VERSION[4],
        )
    return '{year}.{month}.{patch}'.format(
        year=VERSION[0],
        month=VERSION[1],
        patch=VERSION[2]
    )

