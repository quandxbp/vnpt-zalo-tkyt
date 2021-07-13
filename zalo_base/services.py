import requests
from .credentials import ZALO_CRE
from .models import ZaloUser
from .zalo_sdk import ZaloSDK

class ZaloService:

    def __init__(self):
        self.z_sdk = ZaloSDK(ZALO_CRE['access_token'])
    
    def store_user_info(self, user_id, name='', phone=''):
        is_existed = ZaloUser.objects.filter(user_id=user_id).exists()
        if not is_existed:
            new_user = ZaloUser(
                name = name,
                user_id = user_id, 
                phone = phone)
            new_user.save()
        else:
            existed_user = ZaloUser.objects.get(user_id=user_id)
            existed_user.name = name
            existed_user.phone = phone
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
    
    def action_by_event(self, event_name, datas):
        if event_name == 'follow':
            user_id = datas['follower']['id']
            self.store_user_info(user_id)
            return self.z_sdk.post_banner_message(user_id)
    
    def send_confirm_message(self, datas):
        user_id = datas.get('zuser_id')
        phone = datas.get('phone')
        name = datas.get('name')
        self.store_user_info(user_id, name, phone)

        start_time = datas.get('start_time')
        # start_location = datas.get('start_location')
        # dest_location = datas.get('dest_location')

        message = f"""Cảm ơn bạn {name} - {phone} đã khai báo tờ khai Online.
- Ngày khởi hành: {start_time if start_time else 'Chưa xác định'}
Hãy đưa thông báo này cho cán bộ tại chốt kiểm soát để xác nhận lại đăng ký."""

        return self.z_sdk.post_message(user_id, message=message)
    
    def send_confirm_at_checkpoint(self, phone):
        is_existed = ZaloUser.objects.filter(phone=phone).exists()
        if is_existed:
            user = ZaloUser.objects.get(phone=phone)
            text = f"""Thành công xác nhận thônt tin tại chốt kiểm soát.
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
            

    