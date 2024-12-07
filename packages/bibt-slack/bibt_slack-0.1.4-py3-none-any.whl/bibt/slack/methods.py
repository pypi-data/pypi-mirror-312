import logging

import requests

from .params import DEFAULT_SLACK_ATTACHMENT_COLOR
from .params import SLACK_MAX_BLOCK_COUNT
from .params import SLACK_MAX_TEXT_LENGTH

_LOGGER = logging.getLogger(__name__)


def _check_len(text, trim_end):
    if len(text) > SLACK_MAX_TEXT_LENGTH:
        offset = SLACK_MAX_TEXT_LENGTH - 4
        if trim_end:
            text = text[:offset] + "\n..."
        else:
            text = "...\n" + text[-offset:]
    elif len(text) < 1:
        _LOGGER.warning("Not adding empty string to message.")
        return None
    return text


def post_message(
    webhook,
    title,
    text=None,
    color=None,
    blocks=None,
    buttons=None,
    dividers=False,
    raise_for_status=True,
    trim_end=True,
):
    """Posts a message to Slack.

    .. code:: python

        from bibt.slack import post_message
        post_message(
            "https://hooks.slack.com/....",
            "My Message Title",
            color="#ffffff",
            blocks=[
                "My first block",
                "My second block"
            ],
            buttons=[
                ("Button Text", "action_id", "value", "style")
            ]
        )
        ...


    :param webhook: a slack webhook in the standard format:
        ``'https://hooks.slack.com/services/{app_id}/{channel_id}/{hash}'``
    :type webhook: str

    :param title: the title of the message. This will appear above the attachment.
        Can be Slack-compatible markdown.
    :type title: str

    :param text: the text to be included in the attachment. Can be
        Slack-compatible markdown, defaults to ``None``. You must
        supply either ``text`` or ``blocks``.
    :type text: str, optional

    :param color: the color to use for the Slack attachment border, defaults to
        ``None``. You must supply either ``text`` or ``blocks``.
    :type color: str, optional

    :param blocks: A list of strings, each to be put in its own attachment
        block, defaults to ``None``. You must supply either ``text`` or ``blocks``.
    :type blocks: str, optional

    :param buttons: A list of string 4-tuples describing each button to be added.
        Each tuple should be of the form ``(text, action_id, value, style)``.
        See here for more information: https://api.slack.com/reference/block-kit/block-elements#button
    :type buttons: list, optional

    :param dividers: When generating multiple blocks, whether or not to
        include dividers between them, defaults to ``False``.
    :type dividers: bool, optional

    :param raise_for_status: whether or not to check for HTTP errors
        and raise an exception, defaults to ``True``.
    :type raise_for_status: bool, optional

    :param trim_end: Whether or not to trim the *end* of messages that are too
        long for the API (>3000 characters). If set to ``False``, it will trim
        the beginning instead of the end of the message. Regardless, trimmed
        characters will not be included in the message to Slack. Defaults to
        ``True`` (will cut off the end of messages).
    :type trim_end: bool, optional

    :raises Exception: if ``raise_for_status==True`` and an HTTP error was raised.

    :return: the requests.Response object returned by the API call.
    :rtype: `requests.Response`
    """
    if not color:
        _LOGGER.warning(
            "No attachment color provided, using "
            f"default: [{DEFAULT_SLACK_ATTACHMENT_COLOR}]"
        )
        color = DEFAULT_SLACK_ATTACHMENT_COLOR
    if text and blocks:
        _LOGGER.warning(
            "Both text and blocks provided; prepending the text to the blocks."
        )
        blocks = [text].extend(blocks)
        text = None
    if text:
        text = _check_len(text, trim_end)
        if not text:
            raise Exception("Cannot pass empty string as text.")
        msg = {
            "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": title}}],
            "attachments": [
                {
                    "color": color,
                    "blocks": [
                        {"type": "section", "text": {"type": "mrkdwn", "text": text}}
                    ],
                }
            ],
        }
    elif blocks:
        msg = {
            "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": title}}],
            "attachments": [
                {
                    "color": color,
                    "blocks": [],
                }
            ],
        }
        added_block = False
        for block in blocks:
            block = _check_len(block, trim_end)
            if not block:
                continue
            msg["attachments"][0]["blocks"].append(
                {"type": "section", "text": {"type": "mrkdwn", "text": block}}
            )
            added_block = True
            if dividers:
                msg["attachments"][0]["blocks"].append({"type": "divider"})
        if not added_block:
            raise Exception("No valid text blocks passed (must have len < 0)")

    else:
        raise Exception("Either text or blocks must be passed.")

    block_count = len(msg["attachments"][0]["blocks"])
    max_blocks = SLACK_MAX_BLOCK_COUNT - 1
    if block_count > max_blocks:
        trim_len = max_blocks - 1
        logging.warning(
            f"Too many blocks passed ({block_count}), only sending first {trim_len}."
        )
        msg["attachments"][0]["blocks"] = msg["attachments"][0]["blocks"][:trim_len]
        msg["attachments"][0]["blocks"].append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"_{block_count-trim_len} additional blocks were "
                        "trimmed from this message._"
                    ),
                },
            }
        )

    if buttons:
        button_config = {
            "type": "actions",
            "elements": [],
        }
        for button in buttons:
            try:
                text = button[0]
                action_id = button[1]
                value = button[2]
                style = button[3]
                button_config["elements"].append(
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "emoji": True, "text": text},
                        "action_id": action_id,
                        "value": value,
                        "style": style,
                    }
                )
            except IndexError:
                logging.error(
                    "Invalid button configuration: should be a string 4-tuple, "
                    "i.e. `(text, action_id, value, style)`. You passed: "
                    f"`{button}`"
                )
                break
        if len(button_config["elements"]) > 0:
            msg["attachments"][0]["blocks"].append(button_config)

    r = requests.post(webhook, json=msg)
    if raise_for_status:
        try:
            r.raise_for_status()
        except Exception:
            _LOGGER.error(f"[HTTP Status: {r.status_code}] {r.text}")
            raise
    return r
