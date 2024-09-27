from database.redis_cache_manager import RedisCacheManager


def extract_whatsapp_data(data: dict):
    sms_message_sid = data.get('SmsMessageSid')
    profile_name = data.get('ProfileName')
    message_type = data.get('MessageType')
    sms_sid = data.get('SmsSid')
    wa_id = data.get('WaId')
    sms_status = data.get('SmsStatus')
    body = data.get('Body')
    to = data.get('To')
    num_segments = data.get('NumSegments')
    referral_num_media = data.get('ReferralNumMedia')
    message_sid = data.get('MessageSid')
    account_sid = data.get('AccountSid')
    from_whatsapp = data.get('From')
    api_version = data.get('ApiVersion')
    attachment_description = None

    if data.get('NumMedia') != '0' and data.get('MediaContentType0'):
        media_content_type = data.get('MediaContentType0')
        num_media = data.get('NumMedia')
        media_url = data.get('MediaUrl0')
        attachment_description = process_attachment_message(media_content_type, num_media, media_url, body)

    chat_history = get_chat_history()

    return {
        'sms_message_sid': sms_message_sid,
        'profile_name': profile_name,
        'message_type': message_type,
        'sms_sid': sms_sid,
        'wa_id': wa_id,
        'sms_status': sms_status,
        'body': body,
        'to': to,
        'num_segments': num_segments,
        'referral_num_media': referral_num_media,
        'message_sid': message_sid,
        'account_sid': account_sid,
        'from_whatsapp': from_whatsapp,
        'api_version': api_version,
        'attachment_description': attachment_description,
        'chat_history': chat_history
    }


# TO-DO
def process_attachment_message(media_content_type, num_media, media_url, body):
    pass


def get_chat_history(user_id):
    rcm = RedisCacheManager()
    history = rcm.get_conversation_history(user_id)
    if isinstance(history, list) and len(history)>0:
        return history
    print('error loading cache history')
    return []

