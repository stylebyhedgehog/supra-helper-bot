from controllers.bot.parent.study_results_handler_template import  StudyResultsHandler
from services.bot.performance_service import PerformanceService
from utils.constants.callback_names import CPP_PERFORMANCE, CPP_MENU
from utils.constants.messages import PPM_PERFORMANCE


class PerformanceHandler(StudyResultsHandler):
    def __init__(self, bot):
        super().__init__(bot, CPP_MENU.PERFORMANCE, CPP_PERFORMANCE, PPM_PERFORMANCE, PerformanceService.get_performance, "performance")