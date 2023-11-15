from services.api.alfa.template import AlfaApiTemplate
from services.logger import Logger


class RoomFetcher:
    @staticmethod
    def all():
        url = "https://supra.s20.online/v2api/room/index"

        return AlfaApiTemplate.fetch_paginated_data(url=url)


class RoomDataService:
    @staticmethod
    def get_room_num_by_id(room_id):
        data = RoomFetcher.all()
        for room in data:
            if room.get("id") == room_id:
                return int(room.get("name")[1:])
        Logger.entity_not_found_error("Room (Room num)", alfa_room_id=room_id)
        return None
