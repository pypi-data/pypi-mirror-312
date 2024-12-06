"""Simple Telegram message sender."""
from __future__ import annotations

from typing import Final

from telegram import Bot
from telegram.error import TelegramError


TELEGRAM_ERROR_MSG: Final = "Failed to send Telegram message"


async def send_telegram_message(
    bot_token: str,
    chat_id: str | int,
    message: str,
) -> None:
    """Send a Telegram message using a bot token.

    Args:
        bot_token: The bot token from BotFather
        chat_id: The chat ID where to send the message
        message: The message to send

    Raises:
        ValueError: If the message sending fails
    """
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        raise ValueError(TELEGRAM_ERROR_MSG) from e


if __name__ == "__main__":
    import asyncio

    async def main():
        bot_token = "YOUR_BOT_TOKEN"
        chat_id = "YOUR_CHAT_ID"
        await send_telegram_message(bot_token, chat_id, "Hello from Python!")

    asyncio.run(main())
