class vendaVeiculo:
    def __init__(self, 
                 idVenda:int=None
                 ):
        ### SETTERS ###
    def set_idVenda(self, codigo:int):
        self.codigo = codigo
        
        ### GETTERS ###

    def get_idVenda(self) -> int:
        return self.codigo

    def to_string(self) -> str:
        return f"Codigo: {self.get_codigo()} | Descrição: {self.get_descricao()}"
    ### DUVIDA ###