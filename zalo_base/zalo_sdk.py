import requests
from .credentials import ZALO_CRE

class ZaloSDK:

    def __init__(self, access_token):
        self.base_url = 'https://openapi.zalo.me/v2.0/oa'
        self.access_token = access_token
        self.headers = self.get_headers()

    def get_headers(self):
        return {
            'access_token': self.access_token,
            'Content-Type': 'application/json'
        }
    
    def _process_response(self, response):
        if response.ok:
            json_res = response.json()
            return {
                'success': 1 if json_res['error'] > 0 else 0,
                'message': json_res['message']
            }
        else:
            return {
                'status_code': response.status_code,
                'message': f"{response.text}",
                'success': 0
            }
    
    def post_message(self, user_id, message):
        url = f"{self.base_url}/message"

        body = {
            "recipient": {"user_id": user_id},
            "message": {"text": message }
        }
        response = requests.post(url, json=body, headers=self.headers)
        return self._process_response(response)

    def post_button_message(self, user_id, **kwargs):
        url = f"{self.base_url}/message"
        print(url)
        body = {
            "recipient": {
                "user_id": user_id
            },
            "message": {
                "text": kwargs.get('text', ' '),
                "attachment": {
                    "type": "template",
                    "payload": {
                        "buttons": kwargs.get('buttons') if kwargs.get('buttons') else 
                        [
                            {
                                "title": kwargs.get('title', "Mở đường dẫn"),
                                "payload": {
                                    "url": kwargs.get('url', ' ')
                                },
                                "type": "oa.open.url"
                            },
                        ]
                    }
                }
            }
        }

        response = requests.post(url, json=body, headers=self.headers)
        return self._process_response(response)

    def post_banner_message(self, user_id, **kwargs):
        url = f"{self.base_url}/message"
        body = {
            "recipient": {
                "user_id": user_id
            },
            "message": {
                "text": kwargs.get('text', ' '),
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "list",
                        "elements": [{
                            "title": kwargs.get('title', 'Chưa xác định'),
                            "subtitle": kwargs.get('subtitle', 'Chưa xác định'),
                            "image_url": kwargs.get('image_url', 'https://i.imgur.com/TVVyxKY.png'),
                            "default_action": {
                                "type": "oa.open.url",
                                "url": kwargs.get('url', f"https://kiemdich.binhphuoc.gov.vn/#/to-khai-y-te/0?zuser_id={user_id}")
                            }
                        }],
                    }
                }
            }
        }

        response = requests.post(url, json=body, headers=self.headers)
        return self._process_response(response)
    
    def request_user_info(self, user_id, **kwargs):
        url = f"{self.base_url}/message"
        body = {
            "recipient": {
                "user_id": user_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "request_user_info",
                        "elements": [{
                            "title": kwargs.get('title', 'Chưa xác định'),
                            "subtitle": "Đang yêu cầu thông tin từ bạn",
                            "image_url": kwargs.get('image_url', 'https://i.imgur.com/TVVyxKY.png'),
                        }]
                    }
                }
            }
        }

        response = requests.post(url, json=body, headers=self.headers)
        return self._process_response(response)

    def send_attachment_message(self, user_id, **kwargs):
        url = f"{self.base_url}/message"

        body = {
            "recipient": {
                "user_id": user_id
            },
            "message": {
                "text": kwargs.get('text',"QR Code thông tin cá nhân"),
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "media",
                        "elements": [{
                            "media_type": "image",
                            "url": kwargs.get('url', "https://4js.com/online_documentation/fjs-gst-2.50.02-manual-html/Images/grw_qr_code_example_width_3cm.jpg")
                        }]
                    }
                }
            }
        }

        response = requests.post(url, json=body, headers=self.headers)
        return self._process_response(response)
    