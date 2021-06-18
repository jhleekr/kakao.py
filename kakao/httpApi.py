import json

import requests
import hashlib

from .config import APP_VERSION, OS_VERSION, AGENT, LANG

AUTH_HEADER = f"{AGENT}/{APP_VERSION}/{LANG}"
UTH_USER_AGENT = f"KT/{APP_VERSION} Wd/{OS_VERSION} {LANG}"

LOGIN_URL = "https://ac-sb-talk.kakao.com/win32/account/login.json"
REGISTER_DEVICE_URL = "https://ac-sb-talk.kakao.com/win32/account/register_device.json"
REQUEST_PASSCODE_URL = (
    "https://ac-sb-talk.kakao.com/win32/account/request_passcode.json"
)
MORE_SETTING_URL = (
    f"https://sb-talk.kakao.com/win32/account/more_settings.json?since={0}&lang={LANG}"
)
MEDIA_URL = "https://up-m.talk.kakao.com/upload"


def RequestPasscode(email, password, device_name, device_uuid):
    h = Header(email, device_uuid)
    d = Data(email, password, device_name, device_uuid)
    d["permanent"] = "true"
    d["once"] = "false"
    r = requests.post(REQUEST_PASSCODE_URL, headers=h, data=d)

    return r.content.decode()


def RegisterDevice(email, password, device_name, device_uuid, passcode):
    h = Header(email, device_uuid)
    d = Data(email, password, device_name, device_uuid)
    d["permanent"] = "true"
    d["once"] = "false"
    d["passcode"] = passcode
    r = requests.post(REGISTER_DEVICE_URL, headers=h, data=d)

    return r.content.decode()


def Login(email, password, device_name, device_uuid):
    h = Header(email, device_uuid)
    d = Data(email, password, device_name, device_uuid)
    d["permanent"] = True
    d["forced"] = True
    r = requests.post(LOGIN_URL, headers=h, data=d)

    return r.content.decode()


def Header(email, device_uuid):
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "A": AUTH_HEADER,
        "X-VC": getXVC(email, device_uuid),
        "User-Agent": UTH_USER_AGENT,
        "Accept": "*/*",
        "Accept-Language": LANG,
    }


def getXVC(email, device_uuid, isFull=False):
    string = f"HEATH|{UTH_USER_AGENT}|DEMIAN|{email}|{device_uuid}".encode("utf-8")
    hash = hashlib.sha512(string).hexdigest()
    if isFull:
        return hash
    return hash[0:16]


def Data(email, password, device_name, device_uuid):
    return {
        "email": email,
        "password": password,
        "device_name": device_name,
        "device_uuid": device_uuid,
        "os_version": OS_VERSION,
    }


def upload(data, dataType, userId):
    r = requests.post(
        MEDIA_URL,
        headers={
            "A": AUTH_HEADER,
        },
        data={
            "attachment_type": dataType,
            "user_id": userId,
        },
        files={
            "attachment": data,
        },
    )
    path = r.content.decode()
    key = path.replace("/talkm", "")
    url = "https://dn-m.talk.kakao.com" + path

    return path, key, url


def postText(chatId, li, text, notice, accessKey, deviceUUID):
    if li == 0:
        url = f"https://talkmoim-api.kakao.com/chats/{chatId}/posts"
    else:
        url = f"https://open.kakao.com/moim/chats/{chatId}/posts?link_id={li}"

    r = requests.post(
        url,
        headers={
            "A": AUTH_HEADER,
            "User-Agent": UTH_USER_AGENT,
            "Authorization": f"{accessKey}-{deviceUUID}",
            "Accept-Language": "ko",
        },
        data={
            "content": json.dumps([{"text": text, "type": "text"}]),
            "object_type": "TEXT",
            "notice": notice,
        },
    )

    print(r.content.decode())
