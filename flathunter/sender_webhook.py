from typing import List, Dict

import requests

from flathunter.abstract_notifier import Notifier
from flathunter.abstract_processor import Processor
from flathunter.config import YamlConfig


class SenderWebhook(Processor, Notifier):
		def __init__(self, config: YamlConfig, receivers=None):
				self.config = config
				self.api_key = self.config.webhook_api_key()
				self.__webhook_url = "https://5773-39-40-178-230.ngrok.io/webhook"

		
		def notify(self, message: str):
				payload = {
					"text": message,
					"session": "default"
				}

				
				headers={'X-API-KEY': self.api_key}

				requests.request("POST", self.__webhook_url, data=payload, timeout=30, headers=headers)

				return {}
				

	
