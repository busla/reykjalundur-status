import os
from datetime import datetime
from typing import List, Union
from reykjalundur.common.config import email_console
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from .models import EmailMessage, SocketResponse

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
    if not email_console:
        await fm.send_message(data)
    else:
        print(data.dict())
    return SocketResponse(
        **{
            "message": "email has been sent",
            "current_time": datetime.now(),
            "status": 2,
        }
    )
