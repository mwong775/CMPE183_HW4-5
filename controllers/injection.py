def script():
    return dict()

def delayed():
    return dict()

def get_record():
    r = db.mytable(request.vars.record_id)
    return response.json(dict(
        title=r.title,
        paragraph=r.paragraph,
    ))