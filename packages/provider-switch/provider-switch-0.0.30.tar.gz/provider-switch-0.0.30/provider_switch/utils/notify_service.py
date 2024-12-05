from datetime import datetime
from json import dumps

import requests


class NotifyService(object):
    def __init__(
        self,
        channels: list = None,
        timestamp: bool = True,
        debug=False,
        silent=False,
        env="development",
    ):
        self.debug = debug
        self.channels = channels
        self.timestamp = timestamp
        self.env = env
        self.silent = silent

    def error(self, name: str, type: str, event: str, channels=None):
        if channels is None:
            channels = ["webhook"]
        self.push(
            message="\n".join(
                [
                    f"🚨 Service name *{name}*",
                    f"- *Provider*: {type}",
                    f"- *Trace*: \n```{event}```",
                ]
            ),
            channels=channels,
        )

    def push(self, message: str, channels: list = None):
        if self.silent or not channels or len(self.channels) == 0:
            return
        for channel in self.channels:
            if channels is None or (
                channels is not None and channel.get("type", None) in channels
            ):
                if isinstance(message, list):
                    message = "\n".join(message)
                message = self._parse_message(
                    message=message, parse_mode=channel.get("parse_mode")
                )
                if (
                    channel.get("type") == "webhook"
                    and channel.get("webhook_url") is not None
                ):
                    self._send_webhook(url=channel.get("webhook_url"), message=message)
                elif (
                    channel.get("type") == "telegram"
                    and "access_token" in channel
                    and "chat_id" in channel
                ):
                    self._send_telegram_message(
                        message=message,
                        access_token=channel.get("access_token"),
                        chat_id=channel.get("chat_id"),
                    )

    def send_webhook(self, url: str, message: str, parse_mode: str = "google"):
        parsed_message = self._parse_message(message=message, parse_mode=parse_mode)
        self._send_webhook(url=url, message=parsed_message)

    @staticmethod
    def _send_telegram_message(
        message: str, access_token: str, chat_id: str, parse_mode="Markdown"
    ):
        url_tpl = f"https://api.telegram.org/bot{access_token}/sendMessage?chat_id={chat_id}&parse_mode={parse_mode}&text={message}"
        response = requests.post(
            url_tpl.format(
                {
                    "access_token": access_token,
                    "chat_id": chat_id,
                    "parse_mode": parse_mode,
                    "message": message,
                }
            )
        )
        if response.status_code == 200:
            print("📣 [telegram] sent!")

    def _parse_message(self, message: str, parse_mode: str):
        parsed_message = message

        # 1. Convert link
        if message.find("<") != -1 or message.find(">") != -1:
            custom_data = message[message.find("<") + 1 : message.find(">")]
            if (
                custom_data
                and custom_data.startswith("https://")
                and parse_mode != "google"
            ):
                url_list = custom_data.split("|")
                if len(url_list) == 2:
                    if parse_mode == "markdown":
                        parsed_message = message.replace(
                            f"<{custom_data}>", f"[{url_list[1]}]({url_list[0]})"
                        )

        timestamp = ""
        if self.timestamp:
            timestamp = f"[{datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')}]"

        return f"{timestamp} {parsed_message}"

    @staticmethod
    def _send_webhook(**kwargs):
        response = requests.post(
            kwargs.get("url", None),
            headers={"Content-Type": "application/json; charset=UTF-8"},
            json={
                "formattedText": kwargs.get("message"),
                "text": kwargs.get("message"),
            },
        )

        if response.status_code == 200:
            print("📣 Webhook - sent!")
