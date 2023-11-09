from db.repositories.absent_child_repository import AbsentChildRepository
from db.repositories.parent_repository import ParentRepository
from tests.utils import TestUtils
from utils.constants.messages import PPM_ZOOM_RECORDINGS_DISPATCHING
from utils.date_utils import DateUtil
from utils.string_utils import StringUtil


def send_recordings_after_recording_completed(json, bot):
    zoom_topic, host_email, start_time, share_url, password = _extract_zoom_info(json)
    moscow_date = DateUtil.utc_to_moscow(start_time)
    group_id = StringUtil.extract_number_in_brackets(zoom_topic)
    room_num = StringUtil.extract_number_from_email(host_email)
    absent_children = _find_absent_children(group_id, room_num, moscow_date)

    unique_parents_tg_id = set()
    absent_children_ids_for_remove = []

    for absent_child in absent_children:
        if _is_absent_child_time_match(absent_child, zoom_topic):
            _notify_parent_and_remove(absent_child, bot, unique_parents_tg_id, absent_children_ids_for_remove)


def _find_absent_children(group_id, room_num, moscow_date):
    return AbsentChildRepository.find_absent_children_by_group_id_and_room_num_and_date(group_id, room_num, moscow_date)


def _is_absent_child_time_match(absent_child, zoom_topic):
    return absent_child.start_time in zoom_topic


def _notify_parent_and_remove(absent_child, bot, unique_parents_tg_id, absent_children_ids_for_remove):
    child_parent = ParentRepository.find_parent_by_child_alfa_id(absent_child.child_alfa_id)
    parent_tg_id = child_parent.parent_telegram_id

    if parent_tg_id not in unique_parents_tg_id:
        msg = _create_notification_message(absent_child)
        bot.send_message(parent_tg_id, msg)
        unique_parents_tg_id.add(child_parent.parent_telegram_id)
        absent_children_ids_for_remove.append(absent_child.id)
        TestUtils.append_to_file("Отправлена:" + msg, "recordings.txt")
    _delete_absent_children(absent_children_ids_for_remove)


def _create_notification_message(absent_child):
    return PPM_ZOOM_RECORDINGS_DISPATCHING.RESULT_WITH_PASSWORD(
        absent_child.topic, absent_child.share_url, absent_child.password,
        absent_child.group_name, absent_child.start_date, absent_child.start_time
    )


def _delete_absent_children(absent_children_ids_for_remove):
    for id in absent_children_ids_for_remove:
        AbsentChildRepository.delete_absent_child_by_id(id)


def _extract_zoom_info(zoom_data):
    try:
        payload = zoom_data.get("payload", {})
        object_info = payload.get("object", {})

        topic = object_info.get("topic", "")
        host_email = object_info.get("host_email", "")
        start_time = object_info.get("start_time", "")
        share_url = object_info.get("share_url", "")
        password = object_info.get("password", "")
        return topic, host_email, start_time, share_url, password

    except Exception as e:
        print(f"Error extracting Zoom info: {str(e)}")
        return None, None, None, None, None
