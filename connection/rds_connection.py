import pymysql
import sys
import boto3
import os
import time

class RDSConnection: 

    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host='db-recorte-placas.cz6qo20eugb1.us-east-2.rds.amazonaws.com',  # Endpoint do RDS
                user='admin',                       # Usuário do banco
                password='rnEDQpsZuEttzjiEmOwv',                      # Senha do usuário
                port=3306,                                # Porta do MySQL
                database='db-recorte-placas'                 # Nome do banco de dados
            )

            if self.connection.open:
                print("Conexão estabelecida com sucesso!")
                # Obter informações do servidor
                db_info = self.connection.get_server_info()
                print("Versão do servidor MySQL:", db_info)
        except Exception as e:
            print("Erro ao conectar ao MySQL", e)

        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()
        print("Conexão encerrada!")
    
    def insert_data(self, trap_id, user_id, status):
        try:
            query = "INSERT INTO dados (trap_id, user_id, status) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (trap_id, user_id, status))
            self.connection.commit()
            print("Dados inseridos com sucesso!")
        except Exception as e:
            print("Erro ao inserir dados", e)

    def see_data(self, rows = 25):
        try:
            query = "SELECT * FROM dados LIMIT %s"
            self.cursor.execute(query, (rows,))
            data = self.cursor.fetchall()
            for row in data:
                print(row)
        except Exception as e:
            print("Erro ao consultar dados", e)