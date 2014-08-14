#!/usr/bin/env python
# -*- coding: latin-1 -*-
# Desenvolvimento Aberto
# CapturaSenhaChrome.py

#The MIT License (MIT)
#
#[OSI Approved License] 
#
#The MIT License (MIT)
#
#Copyright (c) 2014 - Desenvolvimento Aberto
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
  
# importa modulos
import wx
import wx.grid
import win32crypt
import sqlite3
from os import getenv

# Cria classe generica de uma WX.Grid
# A classe abaixo faz parte da documentação WXPython oficial
# Este trecho de código é util para manipular a grade
  
class GenericTable(wx.grid.PyGridTableBase):
    def __init__(self, data, rowLabels=None, colLabels=None):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        self.rowLabels = rowLabels
        self.colLabels = colLabels
  
    def GetNumberRows(self):
        return len(self.data)
  
    def GetNumberCols(self):
        return len(self.data[0])
  
    def GetColLabelValue(self, col):
        if self.colLabels:
            return self.colLabels[col]
  
    def GetRowLabelValue(self, row):
        if self.rowLabels:
            return self.rowLabels[row]
  
    def IsEmptyCell(self, row, col):
        return False
  
    def GetValue(self, row, col):
        return self.data[row][col]
  
    def SetValue(self, row, col, value):
        pass    
  
# Inicializa Grade
dados = []
colLabels  = ["Site", "Usuario", "senha"]
rowLabels = []
for linha in range(1,150):
    rowLabels.append(str(linha))

# Conecta ao banco de dados do usuario local
# Requer elevação de privilefios se o Chrome estiver aberto
conn = sqlite3.connect(getenv("APPDATA") + "\..\Local\Google\Chrome\User Data\Default\Login Data")
cursor = conn.cursor()

# Captura informações de login
cursor.execute('SELECT action_url, username_value, password_value FROM logins')

# Retorna resultados
resultado = cursor.fetchall()
for result in resultado:
  # Descriptografa senha
  # CryptUnprotectData requer o contexto do usuario local
  senha = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
  if senha:
      captura = [result[0], result[1], senha]
      dados.append(captura)

# Cria classe da grid
class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1, pos=(5,60), size=(850,200))
        tableBase = GenericTable(dados, rowLabels, colLabels)
        self.SetTable(tableBase)                   
 
# Cria formulario
class Formulario(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Desenvolvimento Aberto - Captura Senha - Google Chrome", size=(900, 350))
        panel = wx.Panel(self, wx.ID_ANY)
        label=wx.StaticText(panel, -1, label='Chrome - Captura sites e decifra senhas - Powred by Desenvolvimento Aberto', pos=(300,20))
        grid = SimpleGrid(panel)
        grid.SetColSize(0, 430);
        grid.SetColSize(1, 230);
        grid.SetColSize(2, 100);
 
# Inicializa a aplicação
app = wx.PySimpleApp()
frame = Formulario(None)
frame.Show(True)
app.MainLoop()

        
