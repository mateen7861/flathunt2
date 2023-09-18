from typing import List, Dict

import requests

from flathunter.abstract_notifier import Notifier
from flathunter.abstract_processor import Processor
from flathunter.config import YamlConfig


class SenderWhatsapp(Processor, Notifier):
		def __init__(self, config: YamlConfig, receivers=None):
				self.config = config
				self.api_key = self.config.whatsapp_api_key()

				self.__text_message_url = "https://server.crewmate.co/flathunt/whatsapp/api/sendText"
				self.__send_seen_url = "https://server.crewmate.co/flathunt/whatsapp/api/sendSeen"
				self.__start_typing_url = "https://server.crewmate.co/flathunt/whatsapp/api/startTyping"
				self.__stop_typing_url = "https://server.crewmate.co/flathunt/whatsapp/api/stopTyping"

				if receivers is None:
						self.receiver_ids = self.config.whatsapp_receiver_ids()
				else:
						self.receiver_ids = receivers

		def process_expose(self, expose):
				self.__broadcast(
						receivers=self.receiver_ids,
						message=self.__get_text_message(expose),
				)
				return expose

		def __broadcast(self, receivers: List[int], message: str) -> None:
				for receiver in receivers:
						self.__send_text(receiver, message)

		def notify(self, message: str):
				self.__broadcast(self.receiver_ids, message, None)

		def __send_text(self, chat_id: int, message: str) -> Dict:
				payload = {
					"chatId": f"{chat_id}@c.us",
					"text": message,
					"session": "default"
				}

				presencePayload = {
					"chatId": f"{chat_id}@c.us",
					"session": "default"
				}
				
				headers={'X-API-KEY': self.api_key}


				requests.request("POST", self.__send_seen_url, data=presencePayload, timeout=30, headers=headers)
				requests.request("POST", self.__start_typing_url, data=presencePayload, timeout=30, headers=headers)
				requests.request("POST", self.__stop_typing_url, data=presencePayload, timeout=30, headers=headers)
				requests.request("POST", self.__text_message_url, data=payload, timeout=30, headers=headers)

				return {}

		def __get_text_message(self, expose: Dict) -> str:
				return self.config.message_format().format(
						title=expose.get('title', 'N/A'),
						rooms=expose.get('rooms', 'N/A'),
						size=expose.get('size', 'N/A'),
						price=expose.get('price', 'N/A'),
						url=expose.get('url', 'N/A'),
						address=expose.get('address', 'N/A'),
						durations=expose.get('durations', 'N/A')
				).strip()
