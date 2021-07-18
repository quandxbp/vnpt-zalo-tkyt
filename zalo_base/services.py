import requests
from .credentials import ZALO_CRE
from .models import ZaloUser
from .zalo_sdk import ZaloSDK

class ZaloService:

    def __init__(self):
        self.z_sdk = ZaloSDK(ZALO_CRE['access_token'])
        self.title = "BCĐ phòng chống dịch Covid19 Bình Phước"
        self.default_qr = "https://4js.com/online_documentation/fjs-gst-2.50.02-manual-html/Images/grw_qr_code_example_width_3cm.jpg"

    def get_user_detail_message(self, info):
        address = info.get('address', 'Chưa xác định')
        if info.get('district'):
            address = f"{address}, {info.get('district')}"
        if info.get('city'):
            address = f"{address}, {info.get('city')}"
        message = f"""Cảm ơn bạn đã cung cấp thông tin để đăng ký cấp quản lý
- Họ và tên: {info.get('name', "Chưa xác định")}
- Số điện thoại: {info.get('phone', 'Chưa xác định')}
- Địa chỉ: {address}"""         
        return message
    
    def get_delare_buttons(self, user_id):
        return [
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
    
    def send_confirm_message(self, user_id, datas):
        phone = datas.get('phone', "Chưa xác định")
        name = datas.get('name', "Chưa xác định")
        qr_image = datas.get('qr_image', self.default_qr)

        text = f"""Cảm ơn bạn {name} - {phone} đã khai báo tờ khai Online.
Đây là mã QR Code thông tin đăng ký của bạn.
Hãy đưa thông báo này cho cán bộ tại chốt kiểm soát để xác nhận lại đăng ký."""

        return self.z_sdk.send_attachment_message(user_id, text=text, url=qr_image,)

    def send_confirm_location_message(self, user_id, datas):
        longitude = datas['longitude']
        latitude = datas['latitude']
        location = f"https://www.google.com/maps?q={latitude},{longitude}&z=14&t=m&mapclient=embed"
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
            text = "Hãy chọn tờ khai y tế phù hợp với bạn"
            buttons = self.get_delare_buttons(user_id)

            return self.z_sdk.post_button_message(user_id, text=text, buttons=buttons)
        
        if event_name == "user_submit_info":
            user_id = datas['sender']['id']
            info = datas.get('info')
            if info:
                #TODO: Send user_id and phone to server
                message = self.get_user_detail_message(info)
            else:
                message = f"Bạn chưa cung cấp đầy đủ thông tin, vui lòng thực hiện lại"
        
            return self.z_sdk.post_message(user_id, message=message)

        if event_name == "oa_send_text":
            user_id = datas['recipient']['id']
            message = datas['message']['text']

            # Xác nhận vị trí
            if "#xacnhanvitri" in message:
                title = "Xác nhận vị trí hiện tại của bạn"
                subtitle = "Cung cấp vị trí hiện tại của bạn cho BCĐ phòng chống dịch Covid-19 tỉnh Bình Phước"
                url = f"https://vnptbp-services.herokuapp.com/location/{user_id}"
                return self.z_sdk.post_banner_message(user_id, title=title, subtitle=subtitle, url=url)
            # Khai báo Online
            if "#khaibaoonline" in message:
                text = "Hãy chọn tờ khai y tế phù hợp với bạn"
                buttons = self.get_delare_buttons(user_id)
                return self.z_sdk.post_button_message(user_id, text=text, buttons=buttons)

            if "#dangkyquanly" in message:
                title = "Đăng ký tài khoản cấp Quản lý"
                subtitle = "Hãy cung cấp thông tin cá nhân theo mẫu để tiến hành đăng ký cấp Quản lý"
                user_response = self.z_sdk.get_profile(user_id)

                if user_response['success']:
                    res_data = user_response.get('res_data')
                    shared_info = res_data['data'].get('shared_info')
                    if shared_info:
                        #TODO: Send user_id and phone to server
                        message = self.get_user_detail_message(shared_info)
                        return self.z_sdk.post_message(user_id, message=message)
                return self.z_sdk.request_user_info(user_id, title=title, subtitle=subtitle)

        if event_name == "user_send_text":
            user_id = datas['sender']['id']
            message = datas['message']['text']
            
            if 'TKVT_' in message:
                return self.send_checker_confirm(user_id, message)

    