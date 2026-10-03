from hashlib import sha1


def assign(key: str, train: float = .8, dev: float = .1) -> str:
    if train <= 0 or dev < 0 or train + dev >= 1:
        raise ValueError("require 0 < train and train + dev < 1")
    value = int(sha1(key.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
    if value < train:
        return "train"
    if value < train + dev:
        return "dev"
    return "test"
