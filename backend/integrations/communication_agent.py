import os
import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any

class CommunicationAgent:
    """Slack, Discord, Gmail, Notion integration agent."""

    def send_slack_message(self, webhook_url: str, message: str, blocks: List = None) -> bool:
        payload = {"text": message}
        if blocks:
            payload["blocks"] = blocks
        res = requests.post(webhook_url, json=payload)
        return res.status_code == 200

    def send_slack_file(self, token: str, channel: str, filename: str, content: str) -> bool:
        headers = {"Authorization": f"Bearer {token}"}
        res = requests.post(
            "https://slack.com/api/files.upload",
            headers=headers,
            data={"channels": channel, "filename": filename, "content": content}
        )
        return res.json().get("ok", False)

    def send_discord_message(self, webhook_url: str, content: str, embeds: List = None) -> bool:
        payload = {"content": content}
        if embeds:
            payload["embeds"] = embeds
        res = requests.post(webhook_url, json=payload)
        return res.status_code == 204

    def send_email_gmail(self, to: str, subject: str, body: str, html: bool = False) -> bool:
        user = os.environ.get("GMAIL_USER")
        pwd = os.environ.get("GMAIL_APP_PASSWORD")
        msg = MIMEMultipart()
        msg['From'] = user
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html' if html else 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, pwd)
        server.send_message(msg)
        server.quit()
        return True

    def create_notion_page(self, parent_id: str, title: str, content: str, token: str = None) -> Dict[str, Any]:
        token = token or os.environ.get("NOTION_TOKEN")
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}
        data = {
            "parent": {"page_id": parent_id},
            "properties": {"title": [{"text": {"content": title}}]},
            "children": [{"object": "block", "paragraph": {"rich_text": [{"text": {"content": content}}]}}]
        }
        res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
        res_data = res.json()
        return {"id": res_data.get("id"), "url": res_data.get("url")}

    def update_notion_page(self, page_id: str, content: str, token: str = None) -> bool:
        token = token or os.environ.get("NOTION_TOKEN")
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}
        data = {"children": [{"object": "block", "paragraph": {"rich_text": [{"text": {"content": content}}]}}]}
        res = requests.patch(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=headers, json=data)
        return res.status_code == 200

    def create_notion_database_entry(self, database_id: str, properties: Dict[str, Any], token: str = None) -> Dict[str, Any]:
        token = token or os.environ.get("NOTION_TOKEN")
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}
        data = {"parent": {"database_id": database_id}, "properties": properties}
        res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
        res_data = res.json()
        return {"id": res_data.get("id"), "url": res_data.get("url")}

def inject_communication_prompt(system_prompt: str) -> str:
    return system_prompt + "\nUse CommunicationAgent to send notifications."
