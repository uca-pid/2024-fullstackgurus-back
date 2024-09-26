from firebase_admin import auth



def verify_token_service(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
    except Exception as e:
        print(e)
        return None