class FN:
    MR_BALANCE = "balance.json"
    MR_RECORDINGS = "recordings.json"
    MR_REPORTS = "reports.json"
    MR_TEMP_ON_PAYMENT = "temp_on_payment.json"
    MR_TEMP_ON_PARTICIPATION = "temp_on_participation.json"

    LOG_INFO = "info.txt"
    LOG_INFO_RECORDINGS_COMPLETE = "info_recording_complete.txt"
    LOG_HANDLED_ERRORS = "handled_errors.txt"
    LOG_UNHANDLED_ERRORS = "unhandled_errors.txt"

    LIST_LOG_FILES = [LOG_HANDLED_ERRORS, LOG_UNHANDLED_ERRORS, LOG_INFO, LOG_INFO_RECORDINGS_COMPLETE]
    LIST_MAILING_RESULTS_FILES = [MR_BALANCE, MR_RECORDINGS, MR_REPORTS, MR_TEMP_ON_PAYMENT,
                                  MR_TEMP_ON_PARTICIPATION]
