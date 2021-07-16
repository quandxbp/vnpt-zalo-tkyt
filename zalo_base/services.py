import requests
from .credentials import ZALO_CRE
from .models import ZaloUser
from .zalo_sdk import ZaloSDK

class ZaloService:

    def __init__(self):
        self.z_sdk = ZaloSDK(ZALO_CRE['access_token'])
        self.title = "BCĐ phòng chống dịch Covid19 Bình Phước"
    
    def store_user_info(self, user_id, **info):
        is_existed = ZaloUser.objects.filter(user_id=user_id).exists()
        if not is_existed:
            new_user = ZaloUser(
                user_id = user_id, 
                name = info.get('name', False),
                phone = info.get('phone', False),
                city = info.get('city', False),
                district = info.get('district', False),
                address = info.get('address', False),
                ward = info.get('ward', False),
                )
            new_user.save()
        else:
            existed_user = ZaloUser.objects.get(user_id=user_id)
            existed_user.name = info.get('name', False)
            existed_user.phone = info.get('phone', False)
            existed_user.city = info.get('phone', False)
            existed_user.district = info.get('district', False)
            existed_user.address = info.get('address', False)
            existed_user.ward = info.get('ward', False)

            existed_user.save()
        return {
            'success': 1,
            'message': "Success",
            'zalo_user_id': user_id,
        }
    
    def store_user_id(self, user_id):
        is_existed = ZaloUser.objects.filter(user_id=user_id).exists()
        if not is_existed:
            new_user = ZaloUser(user_id = user_id)
            new_user.save()
        return {
            'success': 1,
            'message': "Success",
            'zalo_user_id': user_id,
        }
    
    def send_confirm_message(self, user_id, datas):
        phone = datas.get('phone')
        name = datas.get('name')
        # self.store_user_info(user_id, name, phone)

        start_time = datas.get('start_time')
        # start_location = datas.get('start_location')
        # dest_location = datas.get('dest_location')

        message = f"""Cảm ơn bạn {name} - {phone} đã khai báo tờ khai Online.
- Ngày khởi hành: {start_time if start_time else 'Chưa xác định'}
Hãy đưa thông báo này cho cán bộ tại chốt kiểm soát để xác nhận lại đăng ký."""

        return self.z_sdk.post_message(user_id, message=message)

    def send_confirm_location_message(self, user_id, datas):
        longitude = datas['longitude']
        latitude = datas['latitude']
        location = f"https://www.google.com/maps/@{latitude},{longitude},15z"
        message = f"""Cảm ơn đã chia sẻ vị trí hiện tại của bạn.
- Vị trí xác định: {location}"""
        return self.z_sdk.post_message(user_id, message=message)
    
    def send_confirm_at_checkpoint(self, phone):
        is_existed = ZaloUser.objects.filter(phone=phone).exists()
        if is_existed:
            user = ZaloUser.objects.get(phone=phone)
            text = f"""Thành công xác nhận thông tin tại chốt kiểm soát.
Hãy nhấn vào nút bên dưới khi đã đến địa điểm của bạn!"""
            title = "Xác nhận khi vừa tới điểm đến"
            url = "https://google.com.vn"
            kwargs = {
                'text': text,
                'title': title,
                'url': url
            }
            return self.z_sdk.post_button_message(user.user_id, **kwargs)
        else:
            return {
                'success': 0,
                'message': f'Not found user by phone number: {phone}'
            }

    def send_checker_confirm(self, user_id, message):
        # response = requests.get(message)
        # if response.ok:
        #     data = response.json()
        buttons = [
            {
                "title": "Từ chối",
                "payload": {
                    "url": 'https://developers.zalo.me/'
                },
                "type": "oa.open.url"
            },
            {
                "title": "Xác nhận",
                "payload": {
                    "url": "https://developers.zalo.me/"
                },
                "type": "oa.open.url"
            },
        ]
        message = """Bùi Trần Đông Quân - 0981613096"""
        return self.z_sdk.post_button_message(user_id, text=message, buttons=buttons)

    
    def action_by_event(self, event_name, datas):
        if event_name == 'follow':
            user_id = datas['follower']['id']
            # text = "Đăng ký khai báo Online"
            buttons = [
                {
                    "title": "Đăng ký tờ khai y tế người dân Online",
                    "payload": {
                        "url": f"https://kiemdich.binhphuoc.gov.vn/#/to-khai-y-te/0/{user_id}"
                    },
                    "type": "oa.open.url"
                },
                {
                    "title": "Đăng ký tờ khai y tế vận tải Online",
                    "payload": {
                        "url": f"https://kiemdich.binhphuoc.gov.vn/#/to-khai-y-te/0/{user_id}"
                    },
                    "type": "oa.open.url"
                }
            ]

            return self.z_sdk.post_button_message(user_id, buttons=buttons)
        
        if event_name == "user_submit_info":
            user_id = datas['sender']['id']
            info = datas['info']
            # self.store_user_info(user_id, **info)
            return self.z_sdk.send_attachment_message(user_id, title=self.title)

        if event_name == "oa_send_text":
            user_id = datas['recipient']['id']
            message = datas['message']['text']
            if "#xacnhanvitri" in message:
                text = "Xác nhận vị trí hiện tại của bạn"
                buttons = [
                    {
                        "title": "Vị trí hiện tại",
                        "payload": {
                            "url": f"https://vnptbp-services.herokuapp.com/location/{user_id}"
                        },
                        "type": "oa.open.url"
                    }
                ]
                return self.z_sdk.post_button_message(user_id, text=text, buttons=buttons)
            if "#khaibaoonline" in message:
                text = "Hãy chọn tờ khai y tế phù hợp với bạn"
                buttons = [
                    {
                        "title": "Đăng ký tờ khai y tế dành cho người dân",
                        "payload": {
                            "url": f"https://kiemdich.binhphuoc.gov.vn/#/to-khai-y-te/0/{user_id}"
                        },
                        "type": "oa.open.url"
                    },
                    {
                        "title": "Đăng ký tờ khai y tế dành cho tài xế",
                        "payload": {
                            "url": f"https://kiemdich.binhphuoc.gov.vn/#/to-khai-y-te/0/{user_id}"
                        },
                        "type": "oa.open.url"
                    }
                ]
                return self.z_sdk.post_button_message(user_id, text=text, buttons=buttons)
        
        if event_name == "user_send_text":
            user_id = datas['sender']['id']
            message = datas['message']['text']
            
            if "#dangkykiemsoat" in message:
                pass
            # if "#xacnhandaden" in message:
            #     return self.z_sdk.post_message(user_id, f"Chào mừng đã đến nơi {user_id}")
            if 'user_info' in message:
                return self.send_checker_confirm(user_id, message)

    