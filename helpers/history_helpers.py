from database.redis_cache_manager import RedisCacheManager


def get_chat_history(user_id):
    rcm = RedisCacheManager()
    rcm.connect()
    history = rcm.get_conversation_history(user_id)
    if isinstance(history, list) and len(history)>0:
        return history
    print('error loading cache history')
    return []

def update_history(user_id, question, response):
    rcm = RedisCacheManager()
    rcm.connect()
    rcm.store_conversation(user_id, 'user', question, expire_time=3600)
    rcm.store_conversation(user_id, 'agent', response, expire_time=3600)