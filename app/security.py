import bcrypt


def hash_pin(pin):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pin.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def check_pin(pin):
    return bcrypt.checkpw(pin.encode("utf-8"), pin.encode("utf-8"))