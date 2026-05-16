"""Notification tasks: email, SMS, WeChat Work webhooks."""
from __future__ import annotations

import logging

from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.notification_tasks.send_alert_notification")
def send_alert_notification(
    user_id: str,
    alert_name: str,
    metric: str,
    value: float,
    channels: list[str],
) -> dict:
    """Send alert notification through configured channels."""
    message = f"⚠️ 预警提醒：{alert_name}\n指标：{metric} 当前值：{value:.2f}"
    results: dict[str, str] = {}
    for ch in channels:
        try:
            if ch == "email":
                _send_email(user_id, "[AI自媒体平台] 数据预警", message)
                results["email"] = "sent"
            elif ch == "wechat":
                _send_wechat_work(message)
                results["wechat"] = "sent"
            else:
                logger.warning("Unknown notification channel: %s", ch)
        except Exception as exc:
            results[ch] = f"failed: {exc}"
            logger.exception("Failed to send %s notification", ch)
    return results


def _send_email(user_id: str, subject: str, body: str) -> None:
    """Send email notification (stub — real: use SMTP or SendGrid)."""
    from app.config import get_settings
    s = get_settings()
    if not s.smtp_host:
        logger.debug("SMTP not configured; email not sent: %s", subject)
        return
    import smtplib
    from email.message import EmailMessage
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = s.smtp_user
    msg["To"] = s.smtp_user  # In production: look up user email
    msg.set_content(body)
    with smtplib.SMTP(s.smtp_host, s.smtp_port) as smtp:
        smtp.starttls()
        smtp.login(s.smtp_user, s.smtp_password)
        smtp.send_message(msg)


def _send_wechat_work(text: str) -> None:
    """Send WeChat Work webhook notification (stub)."""
    import httpx
    from app.config import get_settings
    s = get_settings()
    if not s.wechat_work_webhook:
        logger.debug("WeChat Work webhook not configured")
        return
    payload = {"msgtype": "text", "text": {"content": text}}
    httpx.post(s.wechat_work_webhook, json=payload, timeout=5)
