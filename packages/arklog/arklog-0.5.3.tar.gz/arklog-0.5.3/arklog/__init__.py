"""Custom python logging formatter with color output."""
__version__ = "0.5.3"
__version_info__ = tuple((int(num) if num.isdigit() else num for num in __version__.replace("-", ".", 1).split(".")))


from arklog.logging import (
    CRITICAL,
    ERROR,
    WARNING,
    INFO,
    EXTRA,
    DEBUG,
    NOTSET,

    ColorFormatter,
    create_logger,
    set_defaults,
    set_from_file,
    log,
    success,
    extra,
    set_config_logging,
    set_path_logging
)

from logging import (
    debug,
    info,
    warning,
    error,
    critical,
    exception,
)
