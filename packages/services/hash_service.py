from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

class HashService:
    def generate_hash(self, password):
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    def check_hash(self, hash, password):
        return check_password_hash(hash, password)