# Here go your api methods.

def get_initial_data():
    a = ["a" + str(i) for i in range(10)]
    return response.json(dict(
        animals = ['dog', 'cat', 'fish'],
        things = ['thing1', 'thing2', 'thing3'],
        other_things = a,
    ))
