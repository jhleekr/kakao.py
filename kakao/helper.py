import requests


def get_appv() -> str | None:
    """
    Get latest version from kakaotalk notice page

    Parameters:

    Returns: latest version

    Remarks:
    """
    r = requests.get("https://pc.kakao.com/talk/notices/ko")
    a = r.text.index(r'<ul class="list_notice">')
    r = r.text[a:]
    b = r.index(r"</ul>")
    s = r[:b].split(r"<li>")[1:]
    for ss in s:
        a = ss.index(r'<strong class="tit_item">') + len(r'<strong class="tit_item">')
        b = ss.index(r"</strong>")
        x = ss[a:b]
        if x[5:] == " 버전 업데이트 안내" and x[1] == x[3] == ".":
            return x[:5]
    return None
