# -*- coding: UTF-8 -*-
"""
@apiDefine Authorization
@apiVersion 0.1.0

@apiHeader Authorization User's token.

@apiHeaderExample {json} Header-Example:
    {
        "Authorization": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTU0ODg0NjYwMSwiZXhwIjoxNTUxNDM4NjAxfQ.eyJ1c2VybmFtZSI6IlRlbDExODkzNDYwIiwibGlmZXRpbWUiOjI1OTIwMDAsInJhbmQiOjY1MTd9.Q0-W8Icc1yocRB28ShuUDqKAriBKBs6qe_lXMeQi0mY"
    }

"""

"""
@apiDefine UnauthorizedError
@apiVersion 0.1.0

@apiError UnauthorizedError Unauthorized.

@apiErrorExample {text} Error-Response:
    HTTP/1.1 401 UNAUTHORIZED
    Unauthorized Access
"""

"""
@apiDefine InvalidRequestError
@apiVersion 0.1.0

@apiError InvalidRequest Invalid request.

@apiErrorExample {json} Error-Response:
    HTTP/1.1 400 BAD REQUEST
    {
        "error": "InvalidRequest",
        "message": "invalid request"
    }
"""

"""
@apiDefine UnknownError
@apiVersion 0.1.0

@apiError UnknownError Unknown error.

@apiErrorExample {json} Error-Response:
    HTTP/1.1 500 INTERNAL SERVER ERROR
    {
        "error": "UnknownError",
        "message": "unknown error"
    }
"""

"""
@apiDefine PostNotFoundError
@apiVersion 0.1.0

@apiError PostNotFound Post Not Found.

@apiErrorExample {json} Error-Response:
    HTTP/1.1 404 NOT FOUND
    {
        "message": "post not found"
    }
"""
