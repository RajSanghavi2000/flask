__all__ = ['errors']

errors = {
    'BadRequestError': {
        'ok': False,
        'error': 'BAD_REQUEST',
        'message': "",
        'status': 400,
    },
    "JWtSignatureException": {
        "ok": False,
        "error": "JWT_SIGNATURE_EXCEPTION",
        "message": "Invalid JWT token",
        "status": 401
    }
}
