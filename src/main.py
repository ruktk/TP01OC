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

def Traduz_Instrucao(linha):
    linha = linha.replace("(", " ").replace(")", " ").replace(" x", " ")
    linha = linha.replace(",", " ").split()

    #linha = [sub, 1, 2, 3]
    #linha = lh x1, 1(x2) = [lh, x1, 1, x2]
    #a linha vai ser por exemplo: a instrução "sub x6 x6 x5", se tornando "sub 6 6 5"

    #Define o opcode e o funct3 a partir do dicionário de instruções, usando a instrução da linha como chave
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

            return f"{int(imm):012b}{int(rs1):05b}{funct3}{int(rd):05b}{opcode}"
        
        if funct3 == "001":
            #exemplo: linha = lh x1, 1(x2) = [lh, 1, 1, 2]
            #rd é o primeiro registrador, rs1 é o segundo registrador e imm é o valor imediato entre eles (o 1)
            rd = linha[1]
            rs1 = linha[3]
            imm = linha[2]
            return f"{int(imm):012b}{int(rs1):05b}{funct3}{int(rd):05b}{opcode}"
        
    elif instrucoes[linha[0]]["type"] == "S":
        #linha = sh x1, 1(x2) = [sh, 1, 1, 2]
        funct3 = instrucoes[linha[0]]["funct3"]
        rs1 = linha[1]
        rs2 = linha[3]
        imm = linha[2]

        imm = format(int(imm), '012b')

        #divide o imediato
        return f"{imm[11:4:-1]}{int(rs1):05b}{int(rs2):05b}{funct3}{imm[:5]}{opcode}"

    elif instrucoes[linha[0]]["type"] == "SB":
        funct3 = instrucoes[linha[0]]["funct3"]
        rs1 = linha[1]
        rs2 = linha[2]
        label = linha[3]

        # para melhor compreensão do codigo, o label foi definido como um numero inteiro
        #verifica se o label e positivo, se nao for ele converte o valor para binario em complemento de dois
        label = f"{int(label):012b}" if int(label) >= 0 else format(2**12 + int(label), '012b')

        #divide o offset como o imediato da instrucao'''
        return f"{label[0]}{label[2:8]}{int(rs2):05b}{int(rs1):05b}{funct3}{label[8:]}{label[1]}{opcode}"
    else: 
        print("Instrução não implementada")


def main():

    #o arquivo de entrada precisa necessariamente ter o nome "teste.asm"
    if sys.argv[1][-4:] != ".asm":
        print("Formato de arquivo errado!")
        exit()    

    #saida no terminal
    if len(sys.argv) == 2:
        out = "terminal"
    #saida em arquivo
    elif len(sys.argv) == 4 and sys.argv[2] == "-o":
        out = "arquivo"

    try:
        arq_entrada = open(sys.argv[1], "r")
    except:
        print("Nao foi possivel abrir o arquivo de entrada!")
        exit()


    #lê todas as linhas do arquivo de entrada
    lista_instrucoes = arq_entrada.readlines()


    if out == "terminal":
        print("Código de máquina RISC-V:")
    
    for linha in lista_instrucoes:
        #ignora os rotulos
        if ":" in linha or linha == "\n":
            continue
        linhabin = Traduz_Instrucao(linha)

        if out == "arquivo":
            try:
                arquivo_saida = sys.argv[3]
                arquivo_saida += ".txt"

                with open(arquivo_saida, 'a') as arq_saida:
                    arq_saida.write(f"{linhabin}\n")
            except:
                print("Nao foi possivel abrir o arquivo de saída!")
                exit()


        elif out == "terminal":
            print(linhabin)



if __name__ == "__main__":
    main()

