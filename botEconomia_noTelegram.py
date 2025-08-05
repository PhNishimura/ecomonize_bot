import json #ler dados do json
import os #verifica se o arquivo json ja existe
from datetime import datetime # datas
from telegram import Update #cria o bot do telegram (responde mensagens e comandos)
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

#verificando se o arquivo json existe
def carregar_gastos():
    if not os.path.exists('gastos.json'):
        return[]
    try:
        with open('gastos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return[]
    
def salvar_gasto(gasto):
    gastos = carregar_gastos()
    gastos.append(gasto)

    with open('gastos.json', 'w', encoding='uft-8') as f:
        json.dump(gastos, f, ensure_ascii=False, ident=4) #ensure para deixar palavras em pt-br 

#função chamada quando o usuario digitar /start no chat 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #mensagem que o usuario recebe quando iniciar a conversa com o bot
    mensagem =(
        "Olá sou seu robo de controle de gastos! =) \n\n"
        "Para adicionar um novo gasto, me envie uma mensagem no, seguinte formato:\n"
        "Lugar, Valor\n\n"
        "Por exemplo:\n"
        "Sorveteria, 30.00\n\n"
        "Eu usarei a data de hojee automaticamente. Mas se quiser especificar uma data, use:\n "
        "Lugar, Valor, DD/MM/AAAA"
    )
    await update.message.reply_text(mensagem)

#função que processa as mensagens de gastos
async def processar_gastos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_mensagem = update.message.text
    try:
        partes = [p.strip() for p in texto_mensagem.split(',')]
        
        if len(partes) < 2: 
            raise ValueError("Formato invalido!")
        
        lugar = partes[0]
        valor = float(partes[1].replace(',', '.'))
        data_str = datetime.now().strftime('%d/%m/%Y')

        if len(partes) > 2: 
            #verificando se o usuario colocou a data
            datetime.strftime(partes[2], '%d/%m/%Y')
            data_str = partes[2]

        novo_gasto ={
            "lugar": lugar, 
            "valor": valor, 
            "data": data_str
        }
