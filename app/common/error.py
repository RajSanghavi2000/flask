
__all__ = ['errors']

errors = {
    'DuplicateEmailException': {
        'ok': False,
        'error': 'EMAIL_ALREADY_EXIST',
        'message': "Email is already exist",
        'status': 409,
    },
    'PersonNotFoundException': {
            'ok': False,
            'error': 'PERSON_NOT_FOUND',
            'message': 'Requested person not found',
            'status': 404
    }
}
