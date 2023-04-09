# Importing the Pillow module to manipule images
from PIL import Image

# Esconder o valor de A no bit menos significante de B
def lsb_code(A, B):
    # Right shift 5 posições, sobrando os 3 bits mais significantes 00000xyz
    a1 = A >> 5
    # & com 11111000, sobra os 5 bits mais significantes
    b1 = B & 248
    # soma b1 e a1
    C = b1 + a1
    return C

def lsb_decode(C):
    # Pega os 3 bits menos significantes de C nas posições menos significantes
    a1 = C & 7
    # Left shift do valor em 5 posições, deixando os 3 bits menos significantes nas posições mais de bit mais significante 
    A = a1 << 5
    return A


def esconder(picture, message):
    # Quebrar a imagem em tuplas dos canais diferentes de cores (R, G, B e alpha)
    r, g, b, a = picture.split()
    # Transformar em listas e jogar na variável respectiva
    data_r = list(r.getdata())
    data_g = list(g.getdata())
    data_b = list(b.getdata())
    if len(message) > 265 or len(message) > len(data_r)-1:
        return
    
    # Escondendo o tamanho da mensagem no primeiro byte da imagem em canais diferentes
    data_r[0] = lsb_code(len(message), data_r[0])
    data_g[0] = lsb_code(len(message) << 3, data_g[0])
    data_b[0] = lsb_code(len(message) << 6, data_b[0])
    
    # Escondendo os caracteres em cada pixel - itera em cada caracter da mensagem
    i = 1
    for c in message:
        data_r[i] = lsb_code(ord(c), data_r[i])
        data_g[i] = lsb_code(ord(c)<<3, data_g[i])
        data_b[i] = lsb_code(ord(c)<<6, data_b[i])
        i += 1
    
    # Colocando o novo valor nas variáveis iniciais
    r.putdata(data_r)
    g.putdata(data_g)
    b.putdata(data_b)
    
    # Mergeando a imagem
    new_pic = Image.merge(picture.mode, (r, g, b, a))
    return new_pic

def extrair(picture):
    r, g, b, a = picture.split()
    data_r = list(r.getdata())
    data_g = list(g.getdata())
    data_b = list(b.getdata())

    # Extraindo o tamanho da mensagem
    len_message = lsb_decode(data_r[0])+(lsb_decode(data_g[0])>>3)+(lsb_decode(data_b[0])>>6)
    message = []
  
    # Extraindo caracteres um por um
    for i in range(1, len_message+1):
        c = chr(lsb_decode(data_r[i])+(lsb_decode(data_g[i])>>3)+(lsb_decode(data_b[i])>>6))
        # juntando cada caracter achado em uma lista
        message.append(c)
    #Transformando a lista em um único string
    message = ''.join(message)
    return message

path = input("Insira o caminho da imagem:\n> ")
picture = Image.open(path)
choice = input("Esconder (1) ou extrair (2) mensagem na imagem?\n> ")
if choice == "1":
    message = input("Insira a mensagem (limite de 256 caracteres):\n> ")
    output = input("Insira o nome do output:\n> ")
    new_pic = esconder(picture, message)
    if new_pic != None:
        new_pic.save(output)
        print("A nova imagem foi salva em '"+output+"'!")
    else:
        print("Erro")
elif choice == "2":
    message = extrair(picture)
    print("Mensagem escondida:\n"+message)
