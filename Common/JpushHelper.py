#encoding: utf-8

import jpush


def Push_message(message):
    _jpush = jpush.JPush('3a4aec73aa214a395930061b', 'cfc6654a8205f743007db463')
    push = _jpush.create_push()
    # if you set the logging level to "DEBUG",it will show the debug logging.
    _jpush.set_logging("DEBUG")
    push.audience = jpush.all_
    ios_msg = jpush.ios(alert=message, badge="+1")  # , sound="a.caf", extras={'k1':'v1'})
    push.notification = jpush.notification(ios=ios_msg)
    push.options = {"time_to_live": 86400, "sendno": 12345, "apns_production": False}
    push.platform = jpush.all_
    try:
        response = push.send()
    except:
        print("error")

