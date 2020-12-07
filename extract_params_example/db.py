CONSUMERS = {
    'secretconsumerkey':
    {
        'secret': 'supersecretconsumersecret',
        'timestamp_and_nonce': []
    }
}


def get_secret(key):
    return CONSUMERS.get(str(key), {}).get('secret', '')


def is_key_valid(key):
    return key in CONSUMERS


def has_timestamp_and_nonce(key, timestamp, nonce):
    return (timestamp, nonce) in CONSUMERS[key]['timestamp_and_nonce']


def add_timestamp_and_nonce(key, timestamp, nonce):
    CONSUMERS[key]['timestamp_and_nonce'].append((timestamp, nonce))
