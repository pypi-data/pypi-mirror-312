class Profile:
    def __init__(self):
        self.name = "profile"
        self.id = None
        self.skey = None
        self.balance = None
        self.balance_id = None
        self.balances: list[dict] = None
        self.msg = None
        self.currency = None
        self.minimum_amount = 1
        self.balance_type = None
        self.currency_char = None
        self.time_zone = -3
