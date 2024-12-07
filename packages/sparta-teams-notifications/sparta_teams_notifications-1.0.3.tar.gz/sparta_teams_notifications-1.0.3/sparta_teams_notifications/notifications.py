from airflow.models import Variable
from airflow.utils.state import State
from requests import post

FAIL_MSG = "Task Failed"


def teams_notification(ctx, channels: list[str], webhooks_dict_variable: str = "TEAMS_WEBHOOKS", airflow_host_variable: str = "AIRFLOW_HOST"):
    ti = ctx.get("task_instance")
    _url = ti.log_url.replace("localhost:8080", Variable.get(airflow_host_variable))

    if ti.state != State.FAILED:
        return None

    card_content = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.3",
        "body": [
            {
                "type": "TextBlock",
                "text": FAIL_MSG,
                "color": "attention",
                "weight": "bolder",
                "size": "large",
            },
            {
                "type": "FactSet",
                "facts": [
                    {"title": "Task:", "value": ti.task_id},
                    {"title": "Dag:", "value": ti.dag_id},
                    {
                        "title": "Ref Date:",
                        "value": ctx.get("logical_date").strftime("%Y-%m-%d"),
                    },
                ],
            },
        ],
        "actions": [
            {
                "type": "Action.OpenUrl",
                "title": "View Log",
                "url": _url,
            }
        ],
    }

    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": card_content,
            }
        ],
    }
    webhooks_dict: dict = Variable.get(webhooks_dict_variable, deserialize_json=True)

    for channel in channels:
        r = post(
            webhooks_dict.get(channel, "URL_NOT_FOUND"),
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        r.raise_for_status()
