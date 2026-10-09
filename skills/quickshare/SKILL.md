---
name: quickshare
description: Download the files of a Samsung Quick Share link (quickshare.samsungcloud.com/...). Use whenever a message contains such a link (videos, logs, screenshots the user shares from the phone), before anything else is done with it.
---

# Quick Share download

The user shares test material from the phone as `https://quickshare.samsungcloud.com/<code>` links.
WebFetch and plain curl do not work (CloudFront answers 403 without a browser user agent; the page
needs JavaScript; right after sharing the phone is often still uploading). The files are fine once
you wait a moment and try again, so never give up on the first failure.

## Steps

1. Pick the target folder: where the project keeps such material (e.g. `testdata/video/<date>/` in
   rubikki-solveri for videos), else the scratchpad. Logs and screenshots that only matter for this
   session go to the scratchpad.
2. Run the script (it retries every 20 s, up to 40 times, until the page loads and says the upload
   is complete, then downloads every file under its own name). Run it in the background
   (`run_in_background: true`) when it may have to wait; you are notified when it ends:

   ```
   python ~/.claude/skills/quickshare/qs_download.py "<link>" "<target folder>"
   ```

   Options: `--tries N`, `--wait S`.
3. Check what came: `ffprobe` for videos (duration, size, fps), `head` for logs. Tell the user in
   one line what was downloaded.

## If the script still fails

- `gave up`: the share may have expired (links last about 2 days) or the upload failed on the
  phone; ask the user to share again.
- As a last resort the Puppeteer MCP can open the page in a real browser
  (`mcp__puppeteer__puppeteer_navigate`), then the `contents/<hex>?signature=...` URLs can be read
  from `performance.getEntriesByType('resource')` and fetched with curl `-A "Mozilla/5.0"`.
