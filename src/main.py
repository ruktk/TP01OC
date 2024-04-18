import sys

# Dicionário de instruções RISC-V para suas representações em linguagem de máquina
instrucoes = {
    "lh": {"type": "I", "opcode": "0000011", "funct3": "001"},
    "sh": {"type": "S", "opcode": "0100011", "funct3": "001"},
    "sub": {"type": "R", "opcode": "0110011", "funct3": "000", "funct7": "0100000"},
    "or": {"type": "R", "opcode": "0110011", "funct3": "110", "funct7": "0000000"},
    "andi": {"type": "I", "opcode": "0010011", "funct3": "111"},
    "srl": {"type": "R", "opcode": "0110011", "funct3": "101", "funct7": "0000000"},
    "beq": {"type": "SB", "opcode": "1100011", "funct3": "000"}
}


# Função para traduzir uma instrução assembly para linguagem de máquina RISC-V
""" def traduzir_instrucao(instrucao):
    print("inicio funcao instrucao")
    partes = instrucao.split()
    opcode = instrucoes[partes[0]]["opcode"]
    if instrucoes[partes[0]]["type"] == "R":
        funct3 = instrucoes[partes[0]]["funct3"]
        funct7 = instrucoes[partes[0]].get("funct7", "0000000")
        rd, rs1, rs2 = map(lambda x: int(x[1:]), partes[1:])
        return f"{funct7:07b}{rs2:05b}{rs1:05b}{funct3}{rd:05b}{opcode}"
    elif instrucoes[partes[0]]["type"] == "I":
        funct3 = instrucoes[partes[0]]["funct3"]
        rd, rs1, imm = map(lambda x: int(x[1:]), partes[1:])
        imm_bin = format(imm, '012b') if imm >= 0 else format(2**12 + imm, '012b')
        return f"{imm_bin}{rs1:05b}{funct3}{rd:05b}{opcode}"
    elif instrucoes[partes[0]]["type"] == "S":
        funct3 = instrucoes[partes[0]]["funct3"]
        rs1, rs2, imm = map(lambda x: int(x[1:]), partes[1:])
        imm_bin = format(imm, '012b')
        return f"{imm_bin[0:7]}{rs2:05b}{rs1:05b}{funct3}{imm_bin[7:]}{opcode}"
    elif instrucoes[partes[0]]["type"] == "SB":
        funct3 = instrucoes[partes[0]]["funct3"]
        rs1, rs2, label = map(lambda x: int(x[1:]), partes[1:])
        offset = label - (int(partes[0]) + 4) // 2  # Calcula o offset em relação à próxima instrução
        imm_bin = format(offset, '012b') if offset >= 0 else format(2**12 + offset, '012b')
        return f"{imm_bin[0]}{imm_bin[2:8]}{rs2:05b}{rs1:05b}{funct3}{imm_bin[8:]}{imm_bin[1]}{opcode}"
     """
def traduzir_arquivo(nome_arquivo):
    print("inicio traduzir arquivo")
    with open(nome_arquivo, "r") as f:
        linhas = f.readlines()
    """     f = open(nome_arquivo, "r")
    linhas = f.readlines() """
    #print(f"linhas: {linhas}")
    codigo_maquina = []
    for linha in linhas:
        if ":" in linha:  # Ignora rótulos
            continue
        print(f"linha: {linha}")
        instrucao = linha.strip().split(',')[0]  # Remove comentários e parâmetros
        codigo_maquina.append(traduzir_instrucao(instrucao))
    return codigo_maquina


def Traduz_Instrucao(linha):
    linha = linha.replace("(", " ").replace(")", " ").replace(" x", " ")
    linha = linha.replace(",", " ").split()

    '''linha = [sub, 1, 2, 3]'''
    '''linha = lh x1, 1(x2) = [lh, x1, 1, x2]'''
    """a linha vai ser por ex a instruçao sub x1 x2 x3"""
    opcode = instrucoes[linha[0]]["opcode"]
    funct3 = instrucoes[linha[0]]["funct3"]

    if instrucoes[linha[0]]["type"] == "R":

        if funct3 == "000":
            funct7 = instrucoes[linha[0]]["funct7"]
            rd = linha[1]
            rs1 = linha[2]
            rs2 = linha[3]
            return f"{funct7}{int(rs2):05b}{int(rs1):05b}{funct3}{int(rd):05b}{opcode}"
        
        elif funct3 == "110":

            funct7 = instrucoes[linha[0]]["funct7"]
            rd = linha[1]
            rs1 = linha[2]
            rs2 = linha[3]
            return f"{funct7}{int(rs2):05b}{int(rs1):05b}{funct3}{int(rd):05b}{opcode}"
        
        elif funct3 == "101":
            funct7 = instrucoes[linha[0]]["funct7"]
            rd = linha[1]
            rs1 = linha[2]
            rs2 = linha[3]
            return f"{funct7}{int(rs2):05b}{int(rs1):05b}{funct3}{int(rd):05b}{opcode}"
        
    elif instrucoes[linha[0]]["type"] == "I":

        if funct3 == "111":
            rd = linha[1]
            rs1 = linha[2]
            imm = linha[3]
            #print(rd, rs1, imm)
            return f"{int(imm):012b}{int(rs1):05b}{funct3}{int(rd):05b}{opcode}"
        
        if funct3 == "001":
            '''linha = lh x1, 1(x2) = [lh, 1, 1, 2]
            rd é o primeiro registrador, rs1 é o segundo registrador e imm é o valor imediato entre eles (o 1)'''
            rd = linha[1]
            rs1 = linha[3]
            imm = linha[2]
            return f"{int(imm):012b}{int(rs1):05b}{funct3}{int(rd):05b}{opcode}"
        
    elif instrucoes[linha[0]]["type"] == "S":
        '''linha = sh x1, 1(x2) = [sh, 1, 1, 2]'''
        funct3 = instrucoes[linha[0]]["funct3"]
        rs1 = linha[1]
        rs2 = linha[3]
        imm = linha[2]

        imm = format(int(imm), '012b')
        '''divide o imediato'''
        return f"{imm[5:12]}{int(rs2):05b}{int(rs1):05b}{funct3}{imm[0:5]}{opcode}"

    elif instrucoes[linha[0]]["type"] == "SB":
        funct3 = instrucoes[linha[0]]["funct3"]
        rs1 = linha[1]
        rs2 = linha[2]
        label = linha[3]

        '''''verifica se o label e positivo, se nao for ele converte o valor para binario em complemento de dois'''
        label = f"{int(label):012b}" if int(label) >= 0 else format(2**12 + int(label), '012b')

        '''''divide o offset como o imediato da instrucao'''
        return f"{label[0]}{label[2:8]}{int(rs2):05b}{int(rs1):05b}{funct3}{label[8:]}{label[1]}{opcode}"
    else: 
        print("Instrução não implementada")


def main():

    if sys.argv[1][-4:] != ".asm":
        print("Formato de arquivo errado!")
        exit()    

    if len(sys.argv) == 2:
        out = "terminal"
    elif len(sys.argv) == 3 and sys.argv[2] == "-o":
        out = "arquivo"

    try:
        arq_entrada = open(sys.argv[1], "r")
    except:
        print("Nao foi possivel abrir o arquivo de entrada!")
        exit()


    #Favor nao tocar nisso pq ta funcionando depois de 1h 
    lista_instrucoes = arq_entrada.readlines()


    if out == "terminal":
        print("Código de máquina RISC-V:")
    
    for linha in lista_instrucoes:
        #print(linha)
        if ":" in linha or linha == "\n":
            continue
        linhabin = Traduz_Instrucao(linha)

        if out == "arquivo":
            try:
                with open('arquivo_saida.txt', 'a') as arq_saida:
                    arq_saida.write(f"{linhabin}\n")
            except:
                print("Nao foi possivel abrir o arquivo de saída!")
                exit()


            
        elif out == "terminal":
            print(linhabin)




if __name__ == "__main__":
    main()

