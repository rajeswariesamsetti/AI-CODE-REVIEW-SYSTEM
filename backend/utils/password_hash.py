import bcrypt

def hash_password(password):

    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password.encode(), salt)


def verify_password(password, hashed):

    return bcrypt.checkpw(password.encode(), hashed)