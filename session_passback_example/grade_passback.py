from lti.tool_provider import ToolProvider
from db import get_secret, get_unsend_solution, set_passbacked_flag
import threading


PASSBACK_TIMER = None
PASSBACK_INTERVAL = 20


def put_unsend_result(use_timer=True):
    print('put_unsend_result()')
    for solution in get_unsend_solution():
        print('Try to send {}'.format(solution['_id']))
        grade_passback(solution)
    if use_timer:
        PASSBACK_TIMER = threading.Timer(PASSBACK_INTERVAL, put_unsend_result)
        PASSBACK_TIMER.start()


def grade_passback(solution):
    print(solution)
    passback_params = solution.get('passback_params', {})
    if not passback_params:
        set_passbacked_flag(solution.get('_id'), True)
        print("No passback_params for solution={}".format(solution))
        return

    #if passback_params['lis_result_sourcedid'] == Config.c.lti_imitation.sourced_id:
    #    set_asnwer_passback_flag(solution.get('_id'), False)
    #    print("Imitated response for grade passback (imitated session): solution - {}, user - {}".format(solution.get('_id'), solution.get('user')))
    #    return 

    consumer_secret = get_secret(passback_params['oauth_consumer_key'])
    response = ToolProvider.from_unpacked_request(secret=consumer_secret, params=passback_params, headers=None, url=None).post_replace_result(score=solution.get('score'))
    
    if response.code_major == 'success' and response.severity == 'status':
        set_passbacked_flag(solution.get('_id'), True)
        print("Success grade passback. Solution {} of {}. {} {} {}".format(solution.get('_id'), solution.get('login'), response.description, response.response_code, response.code_major))
    else:
        print("Error while putting result to lms. Solution {}. {} {} {}".format(solution.get('_id'), solution.get('login'), response.description, response.response_code, response.code_major))