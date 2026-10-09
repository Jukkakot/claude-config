"""Download every file of a Samsung Quick Share link.

Usage: python qs_download.py <https://quickshare.samsungcloud.com/XXXX> <out dir> [--tries N] [--wait S]

The share page is fetched with a browser user agent (plain curl gets 403 from CloudFront). It is
retried until it loads and says the upload is complete (the phone may still be uploading, or
CloudFront may block for a while): a 403, a page without files or "uploadCompleted = 'false'" all
wait --wait seconds and try again, at most --tries times. Each file is then downloaded from its
`/ls/public/v1/links/<id>/contents/<hex>?signature=...&storageType=file` address, named from the
Content-Disposition header (else the name found on the page near its id, else file<N> plus a guessed
extension). Prints one line per file: size and path.
"""
import html
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def get(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*", "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, dict(r.headers), r.read()


def page(url, tries, wait):
    for i in range(1, tries + 1):
        try:
            status, _, body = get(url)
            text = html.unescape(body.decode("utf-8", "replace"))
            done = re.search(r"uploadCompleted\s*=\s*'(\w+)'", text)
            links = file_links(text)
            if links and (done is None or done.group(1) == "true"):
                return text, links
            why = "upload not complete" if done and done.group(1) != "true" else "no files on the page yet"
        except urllib.error.HTTPError as e:
            why = f"HTTP {e.code}"
        except Exception as e:  # network hiccup
            why = str(e)
        print(f"try {i}/{tries}: {why}; waiting {wait} s", file=sys.stderr)
        time.sleep(wait)
    sys.exit(f"gave up after {tries} tries")


def file_links(text):
    found = re.findall(r"https://quickshare\.samsungcloud\.com/ls/public/v1/links/[^/\"'\s]+/contents/[0-9a-f]{32}\?signature=[^\"'\s&]+&storageType=file", text)
    return list(dict.fromkeys(found))


def name_on_page(text, cid):
    # The page's JSON lists each file as {..."thumbnail":".../contents/<id>/resized/...","size":N,"name":"<name>"...}.
    for m in re.finditer(r'"name":"([^"]+)"', text):
        ids = re.findall(r"contents/([0-9a-f]{32})", text[max(0, m.start() - 1500): m.start()])
        if ids and ids[-1] == cid:
            return m.group(1)
    i = text.find(cid)
    if i < 0:
        return None
    ctx = text[max(0, i - 800): i + 800]
    names = re.findall(r"[\w .()-]+\.(?:mp4|mov|txt|log|png|jpg|jpeg|zip|json|csv)", ctx)
    names = [n.strip() for n in names if "icon" not in n.lower() and "_ic" not in n]
    return names[0] if names else None


def guess_ext(data):
    if data[:4] == b"\x89PNG":
        return ".png"
    if data[4:8] == b"ftyp":
        return ".mp4"
    if data[:2] == b"PK":
        return ".zip"
    if data[:3] == b"\xff\xd8\xff":
        return ".jpg"
    return ".txt"


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    url, out = args[0], args[1]
    tries = int(args[args.index("--tries") + 1]) if "--tries" in args else 40
    wait = int(args[args.index("--wait") + 1]) if "--wait" in args else 20
    os.makedirs(out, exist_ok=True)
    text, links = page(url, tries, wait)
    for n, link in enumerate(links, 1):
        cid = re.search(r"contents/([0-9a-f]{32})", link).group(1)
        for i in range(1, tries + 1):
            try:
                _, headers, data = get(link, timeout=600)
                break
            except Exception as e:
                print(f"file {n} try {i}: {e}; waiting {wait} s", file=sys.stderr)
                time.sleep(wait)
        else:
            sys.exit(f"could not download file {n}")
        # The page's own name first: the Content-Disposition name is often a hash.
        cd = headers.get("Content-Disposition", "")
        m = re.search(r"filename\*=UTF-8''([^;]+)", cd) or re.search(r'filename="?([^";]+)', cd)
        name = name_on_page(text, cid) or (urllib.parse.unquote(m.group(1)) if m else f"file{n}{guess_ext(data)}")
        path = os.path.join(out, os.path.basename(name))
        with open(path, "wb") as f:
            f.write(data)
        print(f"{len(data):>12} {path}")


if __name__ == "__main__":
    main()
