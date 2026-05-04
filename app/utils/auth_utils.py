from flask import session, redirect, url_for, flash, abort
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] not in roles:
                flash("Acesso não autorizado", "danger")
                return redirect(url_for('eventos.listar_eventos'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
