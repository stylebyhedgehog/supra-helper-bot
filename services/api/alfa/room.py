from services.api.alfa.template import AlfaApiTemplate


class FetchRoom:
    @staticmethod
    def all():
        url = "https://supra.s20.online/v2api/room/index"

        data = AlfaApiTemplate.fetch_paginated_data(url=url)
        return data


class RoomService:
    @staticmethod
    def get_room_num_by_id(room_id):
        data = FetchRoom.all()
        for room in data:
            if room.get("id") == room_id:
                return int(room.get("name")[1:])
