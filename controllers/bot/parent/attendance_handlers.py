from controllers.bot.parent.study_results_handler_template import register_study_results_handlers
from services.bot.attendance_service import AttendanceService
from utils.constants.callback_names import CPP_ATTENDANCE, CPP_MENU
from utils.constants.messages import PPM_ATTENDANCE


def register_attendance_handlers(bot):
    register_study_results_handlers(bot,
                                    CPP_MENU.ATTENDANCE,
                                    CPP_ATTENDANCE,
                                    PPM_ATTENDANCE,
                                    AttendanceService.get_attendance,
                                    "attendance")

