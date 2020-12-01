from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, root_validator
from reykjalundur import settings

datetime_fmt = "%A %d. %b %H:%M:%S"
datetime_encoder = {
    datetime: lambda v: datetime.strftime(v, datetime_fmt),
}


class EmailSchema(BaseModel):
    email: List[EmailStr]


class EmailMessage(BaseModel):
    subject: str
    body: str
    current_time: Optional[datetime]
    recipients: EmailSchema = EmailSchema(email=settings.recipients)

    class Config:
        json_encoders = datetime_encoder

    @root_validator(pre=True)
    def check_current_time(cls, values):
        if not "current_time" in values:
            values["current_time"] = datetime.now()
        return values

    @root_validator
    def concat_datetime(cls, values):
        print(values)
        values["body"] = "<p>{} {}</p>".format(
            values["body"], datetime.strftime(values["current_time"], datetime_fmt)
        )
        return values


class SocketResponse(BaseModel):
    message: str
    current_time: datetime
    status: int

    class Config:
        json_encoders = datetime_encoder
