import hashlib
import hmac


class Encryption:
    @staticmethod
    def generate_encrypted_token(request_body, webhook_secret):
        plain_token = request_body['payload']['plainToken']
        encrypted_token = hmac.new(
            webhook_secret.encode('utf-8'),
            plain_token.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        result = {
            "plainToken": plain_token,
            "encryptedToken": encrypted_token
        }

        return result
