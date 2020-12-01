import os
import logging
from datetime import datetime
from typing import List, Union
from reykjalundur import settings
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from .models import EmailMessage, SocketResponse

logger = logging.getLogger(__name__)
conf = ConnectionConfig(
    MAIL_USERNAME=os.environ["MAIL_USER"],
    MAIL_PASSWORD=os.environ["MAIL_PASSWORD"],
    MAIL_FROM=os.environ["MAIL_FROM"],
    MAIL_PORT=587,
    MAIL_SERVER=os.environ["MAIL_SERVER"],
    MAIL_TLS=True,
    MAIL_SSL=False,
)


async def send_mail(message: EmailMessage) -> SocketResponse:

    data = MessageSchema(
        subject=message.subject,
        recipients=message.recipients.dict().get("email"),
        body=message.body,
        subtype="html",
    )

    fm = FastMail(conf)
    if settings.email_enabled:
        await fm.send_message(data)
    logger.debug(data.dict())
    return SocketResponse(
        **{
            "message": "email has been sent",
            "current_time": datetime.now(),
            "status": 2,
        }
    )
