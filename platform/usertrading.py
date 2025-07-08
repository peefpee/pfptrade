import userclass

class usertrading:
    def __init__(self, user: userclass.UserClass):
        self.user = user

    def nexttradeid(self):
        all_ids = []

        if self.user.orders:
            all_ids += [order["id"] for order in self.user.orders]

        if self.user.positions:
            all_ids += [pos["id"] for pos in self.user.positions]

        if self.user.history:
            all_ids += [hist["id"] for hist in self.user.history]

        return (max(all_ids) + 1) if all_ids else 1
