from .bloque import Bloque
from .sha256 import SHA256


class BlockChain:
    def __init__(self, iComplexity, proofChar):
        self.block_chain = []
        self.complexity = iComplexity
        self.proof_of_work = proofChar * self.complexity

    def get_block_chain(self):
        return self.block_chain

    def block_exist(self, blk):
        for block in self.block_chain:
            if block.get_id() == blk.get_id():
                return True
        return False

    def get_block(self, index):
        return self.block_chain[index]

    def get_last_block(self):
        return self.block_chain[-1]

    def size(self):
        return len(self.block_chain)

    def create_genesis_with_balance(self, pInitialBalance, pClient):
        if self.size() < 1:
            tmp_block = Bloque(
                0, "0000000000000000000000000000000000000000000000000000000000000000"
            )
            if pInitialBalance > 0:
                tmp_block.set_transaction_data("0000GeNeSiS", pInitialBalance, pClient)
            self.block_chain.append(tmp_block)
            self.mine_block()
            return True
        return False

    def create_genesis(self):
        if self.size() < 1:
            tmp_block = Bloque(
                0, "0000000000000000000000000000000000000000000000000000000000000000"
            )
            self.block_chain.append(tmp_block)
            self.mine_block()
            return True
        return False

    def create_block(self):
        prev_hash = self.block_chain[-1].get_hash()
        self.block_chain.append(Bloque(self.size(), prev_hash))

    def get_balance(self, pClient):
        positive_amount = 0.0
        negative_amount = 0.0
        for block in self.block_chain:
            for j in range(block.count_transactions()):
                tx = block.get_transaction(j)
                if tx.get_receiver() == pClient:
                    positive_amount += tx.get_amount()
                elif tx.get_sender() == pClient:
                    negative_amount += tx.get_amount()
        return positive_amount - negative_amount

    def get_proof_of_work_over_block(self, blk):
        cad = blk.to_string()
        nonce = blk.get_nonce()
        sHash = self.generate_hash(cad + str(nonce))
        return sHash == blk.get_hash()

    def add_proved_block(self, blk):
        if not self.block_exist(blk):
            if self.get_proof_of_work_over_block(blk):
                self.block_chain.append(blk)
                return True
        return False

    def mine_block(self):
        bloque_actual = self.block_chain[-1]
        cad = bloque_actual.to_string()
        nonce = 0
        sHash = ""
        while True:
            sHash = self.generate_hash(cad + str(nonce))
            if sHash[: self.complexity] == self.proof_of_work:
                bloque_actual.register(nonce, sHash)
                break
            nonce += 1

    def generate_hash(self, pCad):
        try:
            return SHA256.generate_hash(pCad)
        except Exception:
            return None

    def transaction_report(self, nBlock):
        sCad = ""
        blk = self.block_chain[nBlock]
        for i in range(blk.count_transactions()):
            tx = blk.get_transaction(i)
            sCad += f"\tTransacion #{tx.get_id()}: ${tx.get_amount()}.\t({tx.get_sender()} ---> {tx.get_receiver()})\n"
        return sCad

    def to_string(self):
        block_chain_str = ""
        for block in self.block_chain:
            block_chain_str += block.to_string() + "\n"
        return block_chain_str
