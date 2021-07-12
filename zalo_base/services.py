import requests
from ..common.credentials import ZALO_CRE

class ZaloConnection:

    def get_headers(self):
        return {
            'access_token': ZALO_CRE['access_token']
        }
    
    def post_message(self, user_id, message):
        url = f"{ZALO_CRE['base_url']}/message"
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

    