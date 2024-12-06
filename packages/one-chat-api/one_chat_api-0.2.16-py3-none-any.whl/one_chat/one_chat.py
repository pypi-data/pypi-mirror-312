# one_chat/one_chat.py

from .message_sender import MessageSender
from .broadcast_sender import BroadcastSender
from .location_sender import LocationSender
from .sticker_sender import StickerSender
from .get_friends_and_groups import FriendAndGroupManager


class OneChat:
    def __init__(self, authorization_token: str):
        self.message_sender = MessageSender(authorization_token)
        self.broadcast_sender = BroadcastSender(authorization_token)
        self.location_sender = LocationSender(authorization_token)
        self.sticker_sender = StickerSender(authorization_token)
        self.friends_and_groups = FriendAndGroupManager(authorization_token)

    def send_message(
        self, to: str, bot_id: str, message: str, custom_notification: str = None
    ):
        return self.message_sender.send_message(
            to, bot_id, message, custom_notification
        )

    def send_file(
        self, to: str, bot_id: str, file_path: str, custom_notification: str = None
    ):
        return self.message_sender.send_file(to, bot_id, file_path, custom_notification)

    def send_webview(
        self, to: str, bot_id: str, url: str, custom_notification: str = None
    ):
        return self.message_sender.send_webview(to, bot_id, url, custom_notification)

    def broadcast_message(self, bot_id: str, to: str, message: str):
        return self.broadcast_sender.broadcast_message(bot_id, to, message)

    def send_location(
        self,
        to: str,
        bot_id: str,
        latitude: str,
        longitude: str,
        address: str,
        custom_notification: str = None,
    ):
        return self.location_sender.send_location(
            to, bot_id, latitude, longitude, address, custom_notification
        )

    def send_sticker(
        self, to: str, bot_id: str, sticker_id: str, custom_notification: str = None
    ):
        return self.sticker_sender.send_sticker(
            to, bot_id, sticker_id, custom_notification
        )

    def fetch_friends_and_groups(self, bot_id: str):
        return self.friends_and_groups.fetch_friends_and_groups(bot_id)

    def list_all_friends(self, bot_id: str):
        return self.friends_and_groups.list_all_friends(bot_id)

    def list_friend_ids(self, bot_id: str):
        return self.friends_and_groups.list_friend_ids(bot_id)

    def list_all_groups(self, bot_id: str):
        return self.friends_and_groups.list_all_groups(bot_id)

    def list_group_ids(self, bot_id: str):
        return self.friends_and_groups.list_group_ids(bot_id)
