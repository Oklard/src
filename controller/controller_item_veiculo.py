from model.vendaVeiculo import Itemveiculo
from model.veiculo import Veiculo
from controller.controller_veiculo import Controller_Veiculo
from model.veiculo import veiculo
from controller.controller_veiculo import Controller_veiculo
from conexion.oracle_queries import OracleQueries

class Controller_Item_veiculo:
    def __init__(self):
        self.ctrl_Veiculo = Controller_Veiculo()
        self.ctrl_veiculo = Controller_veiculo()
        
    def inserir_item_veiculo(self) -> Itemveiculo:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        
        # Lista os veiculo existentes para inserir no item de veiculo
        self.listar_veiculos(oracle, need_connect=True)
        codigo_veiculo = str(input("Digite o número do veiculo: "))
        veiculo = self.valida_veiculo(oracle, codigo_veiculo)
        if veiculo == None:
            return None

        # Lista os veiculo existentes para inserir no item de veiculo
        self.listar_veiculo(oracle, need_connect=True)
        codigo_Veiculo = str(input("Digite o código do Veiculo: "))
        Veiculo = self.valida_Veiculo(oracle, codigo_Veiculo)
        if Veiculo == None:
            return None

        # Solicita a quantidade de itens do veiculo para o Veiculo selecionado
        quantidade = float(input(f"Informe a quantidade de itens do Veiculo {Veiculo.get_descricao()}: "))
        # Solicita o valor unitário do Veiculo selecionado
        valor_unitario = float(input(f"Informe o valor unitário do Veiculo {Veiculo.get_descricao()}: "))

        # Recupera o cursor para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo=output_value, quantidade=quantidade, valor_unitario=valor_unitario, codigo_veiculo=int(veiculo.get_codigo_veiculo()), codigo_Veiculo=int(Veiculo.get_codigo()))
        # Executa o bloco PL/SQL anônimo para inserção do novo item de veiculo e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            :codigo := veiculo_CODIGO_ITEM_SEQ.NEXTVAL;
            insert into itens_veiculo values(:codigo, :quantidade, :valor_unitario, :codigo_veiculo, :codigo_Veiculo);
        end;
        """, data)
        # Recupera o código do novo item de veiculo
        codigo_item_veiculo = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados do novo item de veiculo criado transformando em um DataFrame
        df_item_veiculo = oracle.sqlToDataFrame(f"select codigo_item_veiculo, quantidade, valor_unitario, codigo_veiculo, codigo_Veiculo from itens_veiculo where codigo_item_veiculo = {codigo_item_veiculo}")
        # Cria um novo objeto Item de veiculo
        novo_item_veiculo = Itemveiculo(df_item_veiculo.codigo_item_veiculo.values[0], df_item_veiculo.quantidade.values[0], df_item_veiculo.valor_unitario.values[0], veiculo, Veiculo)
        # Exibe os atributos do novo Item de veiculo
        print(novo_item_veiculo.to_string())
        # Retorna o objeto novo_item_veiculo para utilização posterior, caso necessário
        return novo_item_veiculo

    def atualizar_item_veiculo(self) -> Itemveiculo:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do item de veiculo a ser alterado
        codigo_item_veiculo = int(input("Código do Item de veiculo que irá alterar: "))        

        # Verifica se o item de veiculo existe na base de dados
        if not self.verifica_existencia_item_veiculo(oracle, codigo_item_veiculo):

            # Lista os veiculo existentes para inserir no item de veiculo
            self.listar_veiculos(oracle, need_connect=True)
            codigo_veiculo = str(input("Digite o número do veiculo: "))
            veiculo = self.valida_veiculo(oracle, codigo_veiculo)
            if veiculo == None:
                return None

            # Lista os veiculo existentes para inserir no item de veiculo
            self.listar_veiculo(oracle, need_connect=True)
            codigo_Veiculo = str(input("Digite o código do Veiculo: "))
            Veiculo = self.valida_Veiculo(oracle, codigo_Veiculo)
            if Veiculo == None:
                return None

            # Solicita a quantidade de itens do veiculo para o Veiculo selecionado
            quantidade = float(input(f"Informe a quantidade de itens do Veiculo {Veiculo.get_descricao()}: "))
            # Solicita o valor unitário do Veiculo selecionado
            valor_unitario = float(input(f"Informe o valor unitário do Veiculo {Veiculo.get_descricao()}: "))

            # Atualiza o item de veiculo existente
            oracle.write(f"update itens_veiculo set quantidade = {quantidade}, valor_unitario = {valor_unitario}, codigo_veiculo = {veiculo.get_codigo_veiculo()}, codigo_Veiculo = {Veiculo.get_codigo()} where codigo_item_veiculo = {codigo_item_veiculo}")
            # Recupera os dados do novo item de veiculo criado transformando em um DataFrame
            df_item_veiculo = oracle.sqlToDataFrame(f"select codigo_item_veiculo, quantidade, valor_unitario, codigo_veiculo, codigo_Veiculo from itens_veiculo where codigo_item_veiculo = {codigo_item_veiculo}")
            # Cria um novo objeto Item de veiculo
            item_veiculo_atualizado = Itemveiculo(df_item_veiculo.codigo_item_veiculo.values[0], df_item_veiculo.quantidade.values[0], df_item_veiculo.valor_unitario.values[0], veiculo, Veiculo)
            # Exibe os atributos do item de veiculo
            print(item_veiculo_atualizado.to_string())
            # Retorna o objeto veiculo_atualizado para utilização posterior, caso necessário
            return item_veiculo_atualizado
        else:
            print(f"O código {codigo_item_veiculo} não existe.")
            return None

    def excluir_item_veiculo(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do item de veiculo a ser alterado
        codigo_item_veiculo = int(input("Código do Item de veiculo que irá excluir: "))        

        # Verifica se o item de veiculo existe na base de dados
        if not self.verifica_existencia_item_veiculo(oracle, codigo_item_veiculo):            
            # Recupera os dados do novo item de veiculo criado transformando em um DataFrame
            df_item_veiculo = oracle.sqlToDataFrame(f"select codigo_item_veiculo, quantidade, valor_unitario, codigo_veiculo, codigo_Veiculo from itens_veiculo where codigo_item_veiculo = {codigo_item_veiculo}")
            veiculo = self.valida_veiculo(oracle, df_item_veiculo.codigo_veiculo.values[0])
            Veiculo = self.valida_Veiculo(oracle, df_item_veiculo.codigo_Veiculo.values[0])
            
            opcao_excluir = input(f"Tem certeza que deseja excluir o item de veiculo {codigo_item_veiculo} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                # Revome o Veiculo da tabela
                oracle.write(f"delete from itens_veiculo where codigo_item_veiculo = {codigo_item_veiculo}")                
                # Cria um novo objeto Item de veiculo para informar que foi removido
                item_veiculo_excluido = Itemveiculo(df_item_veiculo.codigo_item_veiculo.values[0], df_item_veiculo.quantidade.values[0], df_item_veiculo.valor_unitario.values[0], veiculo, Veiculo)
                # Exibe os atributos do Veiculo excluído
                print("Item do veiculo Removido com Sucesso!")
                print(item_veiculo_excluido.to_string())
        else:
            print(f"O código {codigo_item_veiculo} não existe.")

    def verifica_existencia_item_veiculo(self, oracle:OracleQueries, codigo:int=None) -> bool:
        # Recupera os dados do novo veiculo criado transformando em um DataFrame
        df_veiculo = oracle.sqlToDataFrame(f"select codigo_item_veiculo, quantidade, valor_unitario, codigo_veiculo, codigo_Veiculo from itens_veiculo where codigo_item_veiculo = {codigo}")
        return df_veiculo.empty

    def listar_veiculos(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select p.codigo_veiculo
                    , p.data_veiculo
                    , c.nome as cliente
                    , nvl(f.nome_fantasia, f.razao_social) as empresa
                    , i.codigo_item_veiculo as item_veiculo
                    , prd.descricao_Veiculo as Veiculo
                    , i.quantidade
                    , i.valor_unitario
                    , (i.quantidade * i.valor_unitario) as valor_total
                from veiculos p
                inner join clientes c
                on p.cpf = c.cpf
                inner join fornecedores f
                on p.cnpj = f.cnpj
                left join itens_veiculo i
                on p.codigo_veiculo = i.codigo_veiculo
                left join veiculo prd
                on i.codigo_Veiculo = prd.codigo_Veiculo
                order by c.nome
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def listar_veiculo(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select prd.codigo_Veiculo
                    , prd.descricao_Veiculo 
                from veiculo prd
                order by prd.descricao_Veiculo 
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def valida_veiculo(self, oracle:OracleQueries, codigo_veiculo:int=None) -> veiculo:
        if self.ctrl_veiculo.verifica_existencia_veiculo(oracle, codigo_veiculo):
            print(f"O veiculo {codigo_veiculo} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_veiculo = oracle.sqlToDataFrame(f"select codigo_veiculo, data_veiculo, cpf, cnpj from veiculos where codigo_veiculo = {codigo_veiculo}")
            cliente = self.ctrl_veiculo.valida_cliente(oracle, df_veiculo.cpf.values[0])
            fornecedor = self.ctrl_veiculo.valida_fornecedor(oracle, df_veiculo.cnpj.values[0])
            # Cria um novo objeto cliente
            veiculo = veiculo(df_veiculo.codigo_veiculo.values[0], df_veiculo.data_veiculo.values[0], cliente, fornecedor)
            return veiculo

    def valida_Veiculo(self, oracle:OracleQueries, codigo_Veiculo:int=None) -> Veiculo:
        if self.ctrl_Veiculo.verifica_existencia_Veiculo(oracle, codigo_Veiculo):
            print(f"O Veiculo {codigo_Veiculo} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo Veiculo criado transformando em um DataFrame
            df_Veiculo = oracle.sqlToDataFrame(f"select codigo_Veiculo, descricao_Veiculo from veiculo where codigo_Veiculo = {codigo_Veiculo}")
            # Cria um novo objeto Veiculo
            Veiculo = Veiculo(df_Veiculo.codigo_Veiculo.values[0], df_Veiculo.descricao_Veiculo.values[0])
            return Veiculo