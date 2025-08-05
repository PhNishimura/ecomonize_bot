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
async def processar_gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

        salvar_gasto(novo_gasto)

        #calculando os gastos
        gastos = carregar_gastos()
        mes_atual = datetime.now().month
        ano_atual = datetime.now().year
        total_mes = 0.0 

        for gasto in gastos: 
            data_gasto = datetime.strftime(gasto['data'], '%d/%m/%Y')
            if data_gasto.month == mes_atual and data_gasto.year == ano_atual:
                total_mes += gasto['valor']

        #mensagem para o usuario
        resposta = (
            f"✅ Gasto salvo com sucesso!\n"
            f"Lugar: {lugar}\n"
            f"Data: {data_str}\n\n"
            f"💰 Total de gastos este mês: R$ {total_mes:.2f}"
        )

        await update.message.reply_text(resposta)

    #mensagem de erro
    except(ValueError, IndexError):
        await update.message.reply_text(
            "Erro! Não consegui entender sua mensagem"
        )


#Configuração do bot
def main():
    TOKEN = "SeuBotToken"
    #cria a aplicação do bot com o token colocado
    application = Application.builder().token(TOKEN).build

    #recebe o /start e executa a função start
    application.add_handler(CommandHandler("start", start))

    #quando receber o texto normal, execute a função processar gasto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_gasto))

    #iniciando bot 
    print("Bot iniciado....")
    application.run_polling()


#iniciando a main
if __name__ == '__main__':
    main()