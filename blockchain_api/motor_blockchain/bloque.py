import time

from .transaccion import Transaccion


class Bloque:
    def __init__(self, pId=-1, pPrevHash=None):
        self.id = pId
        self.time_stamp = int(time.time() * 1000)
        self.previous_hash = pPrevHash
        self.a_transactions = []
        self.nonce = -1
        self.hash = None

    def register(self, pNonce, pHash):
        if self.id > -1 and self.nonce < 0 and self.hash is None:
            self.nonce = pNonce
            self.hash = pHash
            return True
        return False

    def set_transaction_data(self, pSender, pAmount, pReceiver):
        self.a_transactions.append(
            Transaccion(len(self.a_transactions), pSender, pReceiver, pAmount)
        )

    def set_transaction_obj(self, pTran):
        self.a_transactions.append(
            Transaccion(
                len(self.a_transactions),
                pTran.get_sender(),
                pTran.get_receiver(),
                pTran.get_amount(),
            )
        )

    def get_transaction(self, pId):
        return self.a_transactions[pId]

    def count_transactions(self):
        return len(self.a_transactions)

    def get_id(self):
        return self.id

    def get_nonce(self):
        return self.nonce

    def get_hash(self):
        return self.hash

    def get_previous_hash(self):
        return self.previous_hash

    def to_string(self):
        sCad = str(self.id) + str(self.time_stamp) + str(self.previous_hash)
        for tx in self.a_transactions:
            sCad += tx.to_string()
        return sCad
