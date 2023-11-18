from controllers.bot.parent.study_results_handler_template import register_study_results_handlers
from services.api.alfa.customer import CustomerDataService
from services.bot.performance_service import PerformanceService
from utils.constants.callback_names import CPP_PERFORMANCE, CPP_MENU
from utils.constants.messages import PPM_PERFORMANCE


def register_performance_handlers(bot):
    register_study_results_handlers(bot,
                                    CPP_MENU.PERFORMANCE,
                                    CPP_PERFORMANCE,
                                    PPM_PERFORMANCE,
                                    PerformanceService.get_performance,
                                          "performance")
