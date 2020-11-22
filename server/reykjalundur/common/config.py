import os

message_disconnect: dict = {
    "subject": "Some subject",
    "body": "Some body",
}

message_reconnect: dict = {
    "subject": "Some subject",
    "body": "Some body",
}

recipients = [os.environ["RECIPIENT"]]
email_console: bool = True