CONSUMERS = {
    'secretconsumerkey':
    {
        'secret': 'supersecretconsumersecret',
        'timestamp_and_nonce': []
    }
}

SESSIONS = {}

### Consumers block ###

def get_secret(key):
    return CONSUMERS.get(str(key), {}).get('secret', '')


def is_key_valid(key):
    return key in CONSUMERS


def has_timestamp_and_nonce(key, timestamp, nonce):
    return (timestamp, nonce) in CONSUMERS[key]['timestamp_and_nonce']


def add_timestamp_and_nonce(key, timestamp, nonce):
    CONSUMERS[key]['timestamp_and_nonce'].append((timestamp, nonce))


### Sessions block ###

def get_session(session_id): return SESSIONS.get(session_id, {})


def add_session(session_id, task, passback_params, admin=False): 
    session = get_session(session_id)
    if session:
        session['tasks'][task] = dict(passback_params=passback_params)
        session['admin'] = admin
    else:
        SESSIONS[session_id] = {'tasks': {task: {'passback_params': passback_params}}, 'admin': admin}
    print(SESSIONS)