import time


class Transaccion:
    def __init__(self, pId, pSender, pReceiver, pAmount):
        self.id = pId
        self.time_stamp = int(time.time() * 1000)
        self.sender = pSender
        self.receiver = pReceiver
        self.amount = float(pAmount)

    def to_string(self):
        return (
            str(self.id)
            + str(self.time_stamp)
            + self.sender
            + self.receiver
            + str(self.amount)
        )

    def get_id(self):
        return self.id

    def get_sender(self):
        return self.sender

    def get_receiver(self):
        return self.receiver

    def get_amount(self):
        return self.amount
