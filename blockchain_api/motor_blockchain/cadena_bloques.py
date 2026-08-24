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

    def create_genesis_with_record(self, pEntidad, pPaciente):
        if self.size() < 1:
            tmp_block = Bloque(
                0, "0000000000000000000000000000000000000000000000000000000000000000"
            )
            # Semilla inicial adaptada a datos médicos
            tmp_block.set_registro_clinico(
                "0000GeNeSiS", pPaciente, "INICIO", "HISTORIAL_CREADO"
            )
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

    def get_historial_paciente(self, pPaciente):
        historial = []
        for block in self.block_chain:
            for j in range(block.count_registros()):
                reg = block.get_registro(j)
                if reg.get_paciente_id() == pPaciente:
                    historial.append(reg)
        return historial

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

    def registro_report(self, nBlock):
        sCad = ""
        blk = self.block_chain[nBlock]
        for i in range(blk.count_registros()):
            reg = blk.get_registro(i)
            sCad += f"\tRegistro #{reg.get_id()}: {reg.get_categoria()}.\t({reg.get_entidad_emisora()} ---> {reg.get_paciente_id()})\n"
        return sCad

    def to_string(self):
        block_chain_str = ""
        for block in self.block_chain:
            block_chain_str += block.to_string() + "\n"
        return block_chain_str
