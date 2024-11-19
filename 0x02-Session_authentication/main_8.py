#!/usr/bin/python3
""" Check response
"""

if __name__ == "__main__":
    try:
        from api.v1.auth.session_db_auth import SessionDBAuth
        sbda = SessionDBAuth()
        session_id = "Session doesn't exist"
        user_id = sbda.user_id_for_session_id(session_id)
        if user_id is not None:
            print("user_id_for_session_id should return None if session_id doesn't exist")
            exit(1)
        
        print("OK", end="")
    except:
        import sys
        print("Error: {}".format(sys.exc_info()))
