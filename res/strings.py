from .numbers import APILimits

class Misc:
    EMPTY   = ''
    NONE    = None

class APIEndpointPaths:
    SHRTNR              = 'shrtnr'
    SHRTZY_REDIRECT     = 'shrtzy-redirect'


class APIMethods:
    POST    = 'POST'
    GET     = 'GET'


class APIKeys:
    URL     = 'url'
    SHRTZY  = 'shrtzy'
    MSG     = 'message'


class APIResponseErrorMessages:
    INVALID_URL_REQUEST                     = 'invalid `url`, please request using a valid `url`.'
    SHRTZY_DOESNT_EXIST                     = '`shrtzy` does not exist, create a shrtzy by POSTing a `url` on this endpoint.'
    CANT_REQUEST_WITH_BOTH_SHRTZY_AND_URL   = 'use either `shrtzy` or `url` to make a POST request on this endpoint.'
    NO_DATA_POSTED                          = 'please POST either `url` or `shrtzy`.'
    METHOD_GET_NOT_ALLOWED                  = 'method GET is not allowed on this endpoint, please POST either `url` or `shrtzy`.'
    METHOD_NOT_ALLOWED                      = 'method not allowed, only POST is allowed on this endpoint'
    ONLY_METHOD_GET_IS_ALLOWED              = 'only method GET is allowed on this endpoint.'
    URL_TOO_LARGE                           = f'`url` too large, must be less than {APILimits.MAX_URL_LEN} chars.'
    SHRTZY_TOO_LARGE                        = f'`shrtzy` too large, must be less than {APILimits.MAX_SHRTZY_LEN} chars.'
    SHRTZY_CONTAIN_SPECIAL_CHARS            = '`shrtzy` contains illeagal special chars.'


class HTTPResponseErrorMessages:
    SHRTZY_DOESNT_EXIST                     = '`shrtzy` does not exist.'