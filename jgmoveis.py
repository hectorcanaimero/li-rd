#!/usr/bin/python

import json
import requests as req
import MySQLdb
from pprint import pprint


class Automated():

  def __init__(self):
    self.lojaApi = '41802ca9f25a956fe22f'
    self.lojaChave = '2649af1c-feee-43ae-90e7-33b88c6a1e3b'
    # Constante de Rd Station
    self.rdUrl = 'https://www.rdstation.com.br/api/1.3/conversions'
    self.rdApi = '62d9c778fa41b8ad8d694143731ceb6d'

  ## Cliente
  def cliente(self):
    url = 'https://api.awsli.com.br/v1/cliente/?format=json&chave_api=%s&chave_aplicacao=%s' %(self.lojaApi, self.lojaChave)
    data = json.loads(req.get(url).text)
    c = data['objects']
    try:
      conn = None
      conn = self.createDefCon()
      cursor = conn.cursor()
      for r in c:
        cursor.execute("""
          SELECT count(id) FROM cliente WHERE clienteId = %d
        """ %r.get('id'))    
        for registro in cursor:
          if registro[0] < 1:
            print('Boa')
            print(r.get('id'))
            self.insertClient(r)
          else:
            print("ya Cadastrado: %d" %r.get('id'))
    except conn.DataError:
      print(conn.DataError)
      return 0

  def insertClient(self, data):
    ID = data.get('id')
    print(ID)
    try:
      conn = self.createDefCon()
      add = conn.cursor()
      add.execute("""
        INSERT INTO cliente (clienteId) VALUES (%d)
    """ %ID)
      conn.commit()
      output = {
        'token_rdstation': self.rdApi,
        'identificador': 'LI - Novo Cliente',
        'email': data.get('email'),
        'nome': data.get('nome'),
        'data_nascimento': data.get('data_nascimento'),
        'sexo': data.get('sexo'),
        'rg': data.get('rg'),
        'tipo': data.get('tipo'),
        'cnpj': data.get('cnpj'),
        'cpf': data.get('cpf'),
        'razao_social': data.get('razao_social'),
        'ie': data.get('ie')
      }
      #pprint(output)
      self.rdStastion(output)
    except MySQLdb.Error as e:
      print ("Error:%d:%s" %(e.args[0], e.args[1]))

  ## Pedido
  def pedido(self):
    url = 'https://api.awsli.com.br/v1/pedido/?format=json&chave_api=%s&chave_aplicacao=%s' %(self.lojaApi, self.lojaChave)
    data = json.loads(req.get(url).text)
    c = data['objects']
    try:
      conn = None
      conn = self.createDefCon()
      cursor = conn.cursor()
      for r in c:
        cursor.execute("""
          SELECT count(id) FROM pedido WHERE pedidoId = %d
        """ %r.get('numero'))    
        for registro in cursor:
          if registro[0] < 1:
            pedidoId = r.get('numero')
            self.insertPedido(pedidoId)
          else:
            print("Pedido Cadastrado: %d" %r.get('numero'))
    except conn.DataError:
      print(conn.DataError)
      return 0


  def insertPedido(self, pedidoId):
    urlPedido = 'https://api.awsli.com.br/v1/pedido/%d?format=json&chave_api=%s&chave_aplicacao=%s' %(pedidoId, self.lojaApi, self.lojaChave)
    data = json.loads(req.get(urlPedido).text)
    for iten in data['itens']:
      pprint(iten.get('nome'))
      pprint(iten.get('sku'))
      pprint(iten.get('preco_venda'))
      pprint(iten.get('quantidade'))
    pprint(data['cliente'].get('email'))
    pprint(data.get('valor_total'))
    pprint(data['endereco_entrega'].get('bairro'))
    pprint(data['endereco_entrega'].get('numero'))
    pprint(data['endereco_entrega'].get('cep'))
    for envio in data['envios']:
      pprint(envio['forma_envio'].get('nome'))
    pprint(data['situacao'].get('nome'))
    for pag in data['pagamentos']:
      pprint(pag['forma_pagamento'].get('nome'))



    # try:
    #   conn = self.createDefCon()
    #   add = conn.cursor()
    #   add.execute("""
    #     INSERT INTO pedido (pedidoId) VALUES (%d)
    # """ %pedidoId)
    #   conn.commit()
    #   print(data.get())
    #   # output = {
    #   #   'token_rdstation': self.rdApi,
    #   #   'identificador': 'LI - Pedido',
    #   #   'email': data.get('email'),
    #   #   'nome': data.get('nome'),
    #   #   'data_nascimento': data.get('data_nascimento'),
    #   #   'sexo': data.get('sexo'),
    #   #   'rg': data.get('rg'),
    #   #   'tipo': data.get('tipo'),
    #   #   'cnpj': data.get('cnpj'),
    #   #   'cpf': data.get('cpf'),
    #   #   'razao_social': data.get('razao_social'),
    #   #   'ie': data.get('ie')
    #   # }
    #   #pprint(output)
    #   self.rdStastion(output)
    # except MySQLdb.Error as e:
    #   print ("Error:%d:%s" %(e.args[0], e.args[1]))


  ## Rd Station Integração
  def rdStastion(self, data):
    header = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    send = req.post(url = self.rdUrl, data = json.dumps(data), headers = header)
    pprint(send.text)

  def createDefCon(self):
    try:
      host = "localhost"
      port = 3306
      user = "root"
      passwd = "admin123!@#"
      db = "vangi_jgmoveis"
      con = MySQLdb.connect(host = host  ,port = port , user = user,passwd = passwd ,db = db)
      return con
    except: 
      return 0


bot = Automated()
# bot.cliente()
bot.insertPedido(2)