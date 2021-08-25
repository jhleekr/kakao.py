import json

from .httpApi import upload

import hashlib
import requests


class Message:
    """
    Represents a single message.

    Parameters:
        channel, body

    Returns:

    Remarks:
    """

    def __init__(self, channel, body):
        self.channel = channel
        self.rawBody = body
        self.logId = self.rawBody["chatLog"]["logId"]
        self.type = self.rawBody["chatLog"]["type"]
        self.message = self.rawBody["chatLog"]["message"]
        self.id = self.rawBody["chatLog"]["msgId"]
        self.author = self.rawBody["chatLog"]["authorId"]

        try:
            if "attachment" in self.rawBody["chatLog"]:
                self.attachment = json.loads(self.rawBody["chatLog"]["attachment"])
            else:
                self.attachment = {}
        except:
            pass

        self.nickName = self.author

    def __repr__(self):
        return "<Message id={0.id} channel={0.channel!r} type={0.type!r} author={0.author!r}>".format(
            self
        )

    async def reply(self, msg, t=1):
        """
        Reply to this chat.

        Parameters:
            msg: message to send [type str]
            t: attach_type [type int, optional]

        Returns:
            raw data of result

        Remarks:
            This function REPLIES to this chat.
            If you want to SEND A MESSAGE to channel, you need to use sendText
        """
        return await self.channel.sendChat(
            msg,
            json.dumps(
                {
                    "attach_only": False,
                    "attach_type": t,
                    "mentions": [],
                    "src_linkId": self.channel.li,
                    "src_logId": self.logId,
                    "src_mentions": [],
                    "src_message": self.message,
                    "src_type": self.type,
                    "src_userId": self.author,
                }
            ),
            26,
        )

    async def sendChat(self, msg, extra, t):
        """
        Send a message to the channel of this chat.

        Parameters:
            msg: message to send [type str]
            extra: attach_type [type dict]
            t: attach_type [type int]

        Returns:
            raw data of result

        Remarks:
            If you want to send just text message, you need to use sendText
        """
        return await self.channel.sendChat(msg, extra, t)

    async def sendText(self, msg):
        """
        Send a text message to the channel of this chat.

        Parameters:
            msg: message to send [type str]

        Returns:
            raw data of result

        Remarks:
        """
        return await self.channel.sendText(msg)

    async def read(self):
        """
        Mark this message as read IF POSSIBLE.
        This only affects on unread message.

        Parameters:

        Returns:
            raw data of result

        Remarks:
        """
        return await self.channel.notiRead(self.logId)

    async def delete(self):
        """
        Delete this message IF POSSIBLE.

        Parameters:

        Returns:
            raw data of result

        Remarks:
        """
        return await self.channel.deleteMessage(self.logId)

    async def hide(self):
        """
        Hide this message IF POSSIBLE.

        Parameters:

        Returns:
            raw data of result

        Remarks:
        """
        return await self.channel.hideMessage(self.logId, self.type)

    async def kick(self):
        """
        Kick author of this message IF POSSIBLE.

        Parameters:

        Returns:
            raw data of result

        Remarks:
        """
        return await self.channel.kickMember(self.authorId)

    async def sendPhoto(self, data, w, h):
        """
        Send photo to the channel of this chat.

        Parameters:
            data: image data in BYTES [type bytes]
            w: width [type int]
            h: height [type int]

        Returns:
            raw data of result

        Remarks:
            you can send photo by path using sendPhotoPath
        """
        path, key, url = upload(data, "image/jpeg", self.authorId)
        return await self.channel.forwardChat(
            "",
            json.dumps(
                {
                    "thumbnailUrl": url,
                    "thumbnailHeight": w,
                    "thumbnailWidth": h,
                    "url": url,
                    "k": key,
                    "cs": hashlib.sha1(data).hexdigest().upper(),
                    "s": len(data),
                    "w": w,
                    "h": h,
                    "mt": "image/jpeg",
                }
            ),
            2,
        )

    async def sendPhotoPath(self, path, w, h):
        """
        Send photo to the channel of this chat.

        Parameters:
            path: path to photo [type str]
            w: width [type int]
            h: height [type int]

        Returns:
            raw data of result

        Remarks:
        """
        with open(path, "rb") as f:
            data = f.read()

        return await self.sendPhoto(data, w, h)

    async def sendPhotoUrl(self, url, w, h):
        """
        Send online photo by url.

        Parameters:
            url: url to photo [type str]
            w: width [type int]
            h: height [type int]

        Returns:
            raw data of result

        Remarks:
        """
        r = requests.get(url)
        r.raise_for_status()

        return await self.sendPhoto(r.content, w, h)

    async def sendLongText(self, title, content):
        path, key, url = upload(content.encode("utf-8"), "image/jpeg", self.authorId)

        return await self.channel.forwardChat(
            title,
            json.dumps(
                {"path": path, "k": key, "s": len(content), "cs": "", "sd": True}
            ),
            1,
        )
