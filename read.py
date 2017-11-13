import os
from time import gmtime, strftime
import csv
import win_inet_pton
from pyModbusTCP.client import ModbusClient

os.system('cls')
print ''
print '====== ModReader v0.1 ======'
print ''
print ''
print ''
filename = raw_input('Digite o nome do arquivo contendo os dados para leitura: ')
regQty = int(raw_input('Quantidade de registros para leitura: '))
delimiter = raw_input('Qual o caracter separador no CSV (";" eh usado como padrao): ')
if delimiter == "":
    delimiter = ";"
outputFile = raw_input('Nome que deseja salvar o arquivo com os dados (Ex. output.csv): ')
if outputFile == "":
    outputFile = strftime("%Y%m%d_%H%M%S.csv", gmtime())

print ''

print "Acessando arquivo de configuracao"

with open(filename, 'rb') as csvfile:
    fileObject = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
    RowCount = sum(1 for row in fileObject)

print "Iniciando leitura"

i = 0
# Abre arquivo CSV para indicar caminho dos registros
with open(filename, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
    for row in spamreader:
        i += 1
        IPAddress = row[0]
        RegAddress = row[1]

        # TCP auto connect on modbus request, close after it
        c = ModbusClient(host=IPAddress, auto_open=True, auto_close=True)

        try:
            regs = c.read_input_registers(int(RegAddress)-1, int(regQty))
        except:
            print "ERRO ao ler linha " + str(i)
            break
        
        if regs:
            with open(outputFile, 'ab') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=delimiter, 
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([IPAddress, RegAddress, regs])
            print "(" + str(i) + "/" + str(RowCount) + ") Lendo IP:" + IPAddress + " Reg: " + RegAddress
        else:
            with open(outputFile, 'ab') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=delimiter,
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([IPAddress, RegAddress, regs, "ERROR"])
            print "(" + str(i) + "/" + str(RowCount) + ") ERRO lendo IP:" + IPAddress + " Reg: " + RegAddress

raw_input("Pressione qualquer tecla para sair...")
