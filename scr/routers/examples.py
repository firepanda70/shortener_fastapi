from scr.core.config import settings

OK_SHORTCUT_DATA = {
    'url': 'https://www.google.com/',
    'status_code': 301,
    'id': 1,
    'disabled': False,
    'shortcut': 'google2',
    'created_at': '2024-01-30T19:40:03.454Z',
    'updated_at': '2024-01-30T19:40:03.454Z',
    'shortcut_full': f'{settings.host}google2'
}

CREATE_SHORTCUT_BODY_EXAMPLES = {
    'ok': {
        'summary': 'Working example',
        'description': 'A **normal** request only with url body param',
        'value': {
            'url': 'https://ya.ru/',
        },
    },
    'Also ok': {
        'summary': 'Working example 2',
        'description': 'A **normal** requset with optional body param **status_code**',
        'value': {
            'url': 'https://ya.ru/',
            'status_code': 303,
        },
    },
    'Invalid URL format': {
        'summary': 'Invalid URL example',
        'description': 'Request with invalid URL format',
        'value': {
            'url': 'not_url_entirely',
        },
    },
    'Invalid Recursive URL': {
        'summary': 'Invalid recursive URL example',
        'description': 'Request with attemt to create shortcut to shortcut',
        'value': {
            'url': f'{settings.host}recursive',
        },
    },
    'Invalid status code value': {
        'summary': 'Invalid stats code example',
        'description': 'Request with invalid **status_code** value',
        'value': {
            'url': 'https://ya.ru/',
            'status_code': 404
        },
    },
}

CREATE_SHORTCUT_RESPONSES = {
    201: {
        'description': 'Successfull response',
        'content': {
            'application/json': {
                'example': [OK_SHORTCUT_DATA]
            }
        },
    }
}

GET_SHORTCUT_RESPONSES = {
    200: {
        'description': 'Successfull response',
        'content': {
            'application/json': {
                'example': [OK_SHORTCUT_DATA]
            }
        },
    }
}

UPDATE_SHORTCUT_BODY_EXAMPLES = {
    'ok': {
        'summary': 'Working example',
        'description': 'A **normal** request with every possible body param',
        'value': {
            'url': 'https://google.ru/',
            'status_code': 303,
            'disabled': True,
            'shortcut': 'unique_shortcut'
        },
    },
    'Invalid URL format': {
        'summary': 'Invalid URL example',
        'description': 'Request with invalid URL format',
        'value': {
            'url': 'not_url_entirely',
        },
    },
    'Invalid Recursive URL': {
        'summary': 'Invalid recursive URL example',
        'description': 'Request with attemt to create shortcut to shortcut',
        'value': {
            'url': f'{settings.host}recursive',
        },
    },
    'Invalid status code value': {
        'summary': 'Invalid stats code example',
        'description': 'Request with invalid **status_code** value',
        'value': {
            'status_code': 404
        },
    },
    'Invalid shortcut': {
        'summary': 'Invalid shotcut string indentifier example',
        'description': 'Request with invalid characters for shortcut',
        'value': {
            'shortcut': '-&=()$#@*_+'
        },
    },
    'Too long shortcut': {
        'summary': 'Too long shotcut string indentifier example',
        'description': 'Request with too long shortcut string identifier',
        'value': {
            'shortcut': 'verylong' * 10
        },
    },
}

UPDATE_SHORTCUT_RESPONSES = {
    200: {
        'description': 'Successfull response',
        'content': {
            'application/json': {
                'example': [OK_SHORTCUT_DATA]
            }
        },
    },
    400: {
        'description': 'Shortcut identifier already taken',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Shortcut <shortcut> already in use'
                }
            }
        },
    },
    404: {
        'description': 'Shortcut not found',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Shortcut <shortcut> not found'
                }
            }
        },
    }
}

DELETE_SHORTCUT_RESPONSES = {
    200: {
        'description': 'Successfull response',
        'content': {
            'application/json': {
                'example': [OK_SHORTCUT_DATA]
            }
        },
    },
    404: {
        'description': 'Shortcut not found',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Shortcut <shortcut> not found'
                }
            }
        },
    }
}

