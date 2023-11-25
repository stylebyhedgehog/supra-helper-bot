from controllers.bot.parent.study_results_handler_template import StudyResultsHandler
from services.bot.attendance_service import AttendanceService
from utils.constants.callback_names import CPP_ATTENDANCE, CPP_MENU
from utils.constants.messages import PPM_ATTENDANCE


class AttendanceHandler(StudyResultsHandler):
    def __init__(self, bot):
        super().__init__(bot, CPP_MENU.ATTENDANCE, CPP_ATTENDANCE, PPM_ATTENDANCE, AttendanceService.get_attendance, "attendance")
