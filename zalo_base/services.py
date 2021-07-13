import requests
from .credentials import ZALO_CRE
from .models import ZaloUser

class ZaloService:

    def get_headers(self, content_type=False):
        headers = {
            'access_token': ZALO_CRE['access_token']
        }
        if content_type: headers.update({'Content-Type': 'application/json'})
        return headers

    def request_get_user_info(self, user_id):
        headers = self.get_headers(True)
        url = f"{ZALO_CRE['base_url']}message"

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
                            "title": "BCĐ PHÒNG CHỐNG DỊCH COVID19 BÌNH PHƯỚC",
                            "subtitle": "Đang yêu cầu thông tin từ bạn",
                            "image_url": "https://i.imgur.com/TVVyxKY.png"
                        }]
                    }
                }
            }
        }

        response = requests.post(url, json=body, headers=headers)
        if response.ok:
            json_res = response.json()
            return {
                'success': 1 if json_res['error'] > 0 else 0,
                'message': json_res['message']
            }
        else:
            return {
                'message': f"{response.status_code} - {response.text}",
                'success': 0
            }

    def send_buttons_message(self, user_id):
        headers = self.get_headers(True)
        url = f"{ZALO_CRE['base_url']}message"

        body = {
            "recipient": {
                "user_id": user_id
            },
            "message": {
                "text": "BCĐ PHÒNG CHỐNG DỊCH COVID19 BÌNH PHƯỚC",
                "attachment": {
                    "type": "template",
                    "payload": {
                        "buttons": [
                            {
                                "title": "Tờ khai y tế Online",
                                "payload": {
                                    "url": f"https://kiemdich.binhphuoc.gov.vn/#/to-khai-y-te/0?zuser_id={user_id}"
                                },
                                "type": "oa.open.url"
                            }
                        ]
                    }
                }
            }
        }

        response = requests.post(url, json=body, headers=headers)
        if response.ok:
            json_res = response.json()
            return {
                'success': 1 if json_res['error'] > 0 else 0,
                'message': json_res['message']
            }
        else:
            return {
                'message': f"{response.status_code} - {response.text}",
                'success': 0
            }


    
    def post_message(self, user_id, message):
        url = f"{ZALO_CRE['base_url']}message"
        body = {
            "recipient": {"user_id": user_id},
            "message": {"text": message }
        }
        response = requests.post(url, body, headers=self.get_header())
        if response.ok:
            return {
                'success': 1 if response.error > 0 else 0,
                'message': response.message
            }
        else:
            return {
                'message': f"{response.status_code} - {response.text}",
                'success': 0
            }

    def get_user_infor(self, user_id):
        url = f"{ZALO_CRE['base_url']}/getprofile"
        params = self.get_header()
        data = {
            "user_id": user_id
        }
        params.update({
            'data': data
        })

        response = requests.get(url, params)
        return response
    
    def store_user_info(self, datas):
        user_id = datas['sender']['id']
        address = datas['info']['address']
        phone = datas['info']['phone']
        city = datas['info']['city']
        district = datas['info']['district']
        name = datas['info']['name']

        is_existed = ZaloUser.objects.filter(user_id=user_id).exists()
        if not is_existed:
            new_user = ZaloUser(
                name = name,
                user_id = user_id, 
                address = address, 
                phone = phone, 
                city = city, 
                district = district)
            new_user.save()
        else:
            existed_user = ZaloUser.objects.get(user_id=user_id)
            existed_user.phone = phone
            existed_user.save()
        return {
            'success': 1,
            'message': "Success",
            'zalo_user_id': user_id,
        }
    
    def action_by_event(self, event_name, datas):
        if event_name == 'follow':
            user_id = datas['follower']['id']
            return self.send_buttons_message(user_id)
        if event_name == 'user_submit_info':
            return self.store_user_info(datas)
    
    # def send_confirm_message(self, phone):
    #     def _parse_phone(phone):
            # if 
        # existed_user = ZaloUser.objects.get(user_id=user_id)
            

    