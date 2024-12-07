from enum import Enum

class SyslogLevel(Enum):
    """
    SYSLOG Levels Codes (0 to 7):

    0 - **Emergency**: The system is unusable. This is the most severe log level, indicating a catastrophic failure (e.g., system crash).

    1 - **Alert**: Action must be taken immediately. Critical conditions that require urgent attention.

    2 - **Critical**: Critical conditions that may affect the operation of the system, but not as dire as an alert.

    3 - **Error**: Error conditions that indicate problems, but may not necessarily stop the system from functioning.

    4 - **Warning**: Warning conditions that may or may not affect the normal operation of the system.

    5 - **Notice**: Normal but significant conditions that are informative and may require monitoring.

    6 - **Informational**: Informational messages that provide general system operation details.

    7 - **Debug**: Detailed debugging messages used for troubleshooting.
    """
    EMERGENCY       : dict = { "keyword": "EMERG",  "severity": "Emergency" , "level": 0 }
    ALERT           : dict = { "keyword": "ALERT",  "severity": "Alert"     , "level": 1 }
    CRITICAL        : dict = { "keyword": "CRIT",   "severity": "Critical"  , "level": 2 }
    ERROR           : dict = { "keyword": "ERR",    "severity": "Error"     , "level": 3 }
    WARNING         : dict = { "keyword": "WARN",   "severity": "Warning"   , "level": 4 }
    NOTICE          : dict = { "keyword": "NOTICE", "severity": "Notice"    , "level": 5 }
    INFORMATIONAL   : dict = { "keyword": "INFO",   "severity": "Informational", "level": 6 }
    DEBUG           : dict = { "keyword": "DEBUG",  "severity": "Debug"     , "level": 7 }

class Classification(Enum):
    RUN_OK:     tuple[str, str, SyslogLevel] = ("Run", "✅Success", SyslogLevel.INFORMATIONAL)
    RUN_FAIL:   tuple[str, str, SyslogLevel] = ("Run", "❌Failed", SyslogLevel.ERROR)

    REMINDER_RUN:   tuple[str, str, SyslogLevel] = ("Reminder", "Reminder cycle executed", SyslogLevel.INFORMATIONAL)
    REMINDER_ALERT: tuple[str, str, SyslogLevel] = ("Reminder", "⭐Reminder Sent", SyslogLevel.NOTICE)

    DATABASE_CONNECTION_OK:     tuple[str, str, SyslogLevel] = ("Database", "✅Connection Success", SyslogLevel.INFORMATIONAL)
    DATABASE_CONNECTION_FAIL:   tuple[str, str, SyslogLevel] = ("Database", "❌Connection Failed", SyslogLevel.ERROR)

    SQL_INSERT_OK:      tuple[str, str, SyslogLevel] = ("SQL", "✅Database INSERT Success", SyslogLevel.DEBUG)
    SQL_INSERT_FAIL:    tuple[str, str, SyslogLevel] = ("SQL", "❌Database INSERT Failed", SyslogLevel.ERROR)
    SQL_DELETE_OK:      tuple[str, str, SyslogLevel] = ("SQL", "✅Database DELETE Success", SyslogLevel.DEBUG)
    SQL_DELETE_FAIL:    tuple[str, str, SyslogLevel] = ("SQL", "❌Database DELETE Failed", SyslogLevel.ERROR)
    SQL_UPDATE_OK:      tuple[str, str, SyslogLevel] = ("SQL", "✅Database UPDATE Success", SyslogLevel.DEBUG)
    SQL_UPDATE_FAIL:    tuple[str, str, SyslogLevel] = ("SQL", "❌Database UPDATE Failed", SyslogLevel.ERROR)
    SQL_SELECT_OK:      tuple[str, str, SyslogLevel] = ("SQL", "✅Database SELECT Success", SyslogLevel.DEBUG)
    SQL_SELECT_FAIL:    tuple[str, str, SyslogLevel] = ("SQL", "❌Database SELECT Failed", SyslogLevel.ERROR)

    WEB_SCRAPING_OK:    tuple[str, str, SyslogLevel] = ("Web Scraping", "✅Scraping Finished", SyslogLevel.INFORMATIONAL)
    WEB_SCRAPING_FAIL:  tuple[str, str, SyslogLevel] = ("Web Scraping", "❌Scraping Failed", SyslogLevel.ERROR)

    API_COMMAND_OK:     tuple[str, str, SyslogLevel] = ("API", "✅API Command Executed", SyslogLevel.INFORMATIONAL)
    API_COMMAND_FAIL:   tuple[str, str, SyslogLevel] = ("API", "❌API Command Failed", SyslogLevel.ERROR)

    CONTENT_CHANGES_VERIFIED: tuple[str, str, SyslogLevel] = ("Content", "Verified for Changes", SyslogLevel.INFORMATIONAL)
    CONTENT_UPDATED:        tuple[str, str, SyslogLevel] = ("Content", "⭐New Content Detected", SyslogLevel.NOTICE)
    CONTENT_UNCHANGED:      tuple[str, str, SyslogLevel] = ("Content", "Content Unchanged", SyslogLevel.INFORMATIONAL)
