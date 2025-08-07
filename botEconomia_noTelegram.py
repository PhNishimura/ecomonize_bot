import json
import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# verificando se o arquivo json existe
def carregar_gastos():
    if not os.path.exists('gastos.json'):
        return []
    try:
        with open('gastos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def salvar_gasto(gasto):
    gastos = carregar_gastos()
    gastos.append(gasto)
    with open('gastos.json', 'w', encoding='utf-8') as f:
        json.dump(gastos, f, ensure_ascii=False, indent=4)  # ensure para deixar palavras em pt-br

# função chamada quando o usuario digitar /start no chat
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # mensagem que o usuario recebe quando iniciar a conversa com o bot
    mensagem = (
        "Olá sou seu robo de controle de gastos! =) \n\n"
        "Para adicionar um novo gasto, me envie uma mensagem no, seguinte formato:\n"
        "Lugar, Valor\n\n"
        "Por exemplo:\n"
        "Sorveteria, 30.00\n\n"
        "Eu usarei a data de hojee automaticamente. Mas se quiser especificar uma data, use:\n"
        "Lugar, Valor, DD/MM/AAAA"
    )
    await update.message.reply_text(mensagem)

# função que processa as mensagens de gastos
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
            # verificando se o usuario colocou a data
            datetime.strftime(partes[2], '%d/%m/%Y')
            data_str = partes[2]

        novo_gasto = {
            "lugar": lugar,
            "valor": valor,
            "data": data_str
        }

        salvar_gasto(novo_gasto)

        # calculando os gastos
        gastos = carregar_gastos()
        mes_atual = datetime.now().month
        ano_atual = datetime.now().year
        total_mes = 0.0

        for gasto in gastos:
            data_gasto = datetime.strptime(gasto['data'], '%d/%m/%Y')
            if data_gasto.month == mes_atual and data_gasto.year == ano_atual:
                total_mes += gasto['valor']

        # mensagem para o usuario
        resposta = (
            f"✅ Gasto salvo com sucesso!\n"
            f"Lugar: {lugar}\n"
            f"Data: {data_str}\n\n"
            f"💰 Total de gastos este mês: R$ {total_mes:.2f}"
        )

        await update.message.reply_text(resposta)

        # verificação de limite
        limite_de_gastos = 800.0
        total_anterior = total_mes - valor

        if total_mes > limite_de_gastos and total_anterior <= limite_de_gastos:
            mensagem_de_aviso = (
                f"⚠️ ATENÇÃO! ⚠️\n\n"
                f"Você ultrapassou seu limite de gastos de R$ {limite_de_gastos:.2f} para este mês!"
            )
            # envia mensagem para o usuario
            await update.message.reply_text(mensagem_de_aviso)

    # mensagem de erro
    except (ValueError, IndexError):
        await update.message.reply_text(
            "Erro! Não consegui entender sua mensagem"
        )

# função para extrato
async def extrato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gastos = carregar_gastos()

    if not gastos:
        # carregar os dados da memoria do json
        await update.message.reply_text("Você aind não possui nenhum gasto registrado. 🤔")
        return
    args = context.args
    hoje = datetime.now()

    gastos_filtrados = []
    periodo_str = ""

    try:
        if len(args) == 2:
            mes_desejado = int(args[0])
            ano_desejado = int(args[1])
            periodo_str = f"{mes_desejado:02d/{ano_desejado}}"

            for gasto in gastos:
                data_gasto = datetime.strptime(gasto['data'], '%d/%m/%Y')
                if data_gasto.month == mes_desejado and data_gasto.year == ano_desejado:
                    gastos_filtrados.append(gasto)
        elif len(args) == 1 and args[0].lower() == 'total':
            periodo_str = "Total"
            gastos_filtrados = gastos
        else:
            mes_atual = hoje.month
            ano_atual = hoje.year
            periodo_str = f"Mês atual ({mes_atual:02d}/{ano_atual})"

            for gasto in gastos:
                data_gasto = datetime.strptime(gasto['data'], '%d/%m/%Y')
                if data_gasto.month == mes_atual and data_gasto.year == ano_atual:
                    gastos_filtrados.append(gasto)

        if not gastos_filtrados:
            resposta = f"Nenhum gastos encontrados para o periodo: {periodo_str}."
        else:
            gastos_filtrados.sort(key=lambda g: datetime.strptime(g['data'], '%d/%m/%Y'))

            linhas_extrato = [f"🧾 *Extrato do Período: {periodo_str}* 🧾\n"]
            total_extrato = 0.0

            for gasto in gastos_filtrados:
                valor_formatado = f"R$ {gasto['valor']:.2f}".replace('.', ',')
                linhas_extrato.append(f"`{gasto['data']}` - {valor_formatado:<12} - {gasto['lugar']}")
                total_extrato += gasto['valor']

            total_formatado = f"R$ {total_extrato:.2f}".replace('.', ',')
            linhas_extrato.append(f"\n*Total do Período:* {total_formatado}")

            resposta = "\n".join(linhas_extrato)

        await update.message.reply_text(resposta, parse_mode='Markdown')

    except (ValueError, IndexError):
        await update.message.reply_text(
            "❌ Formato de comando inválido. Use:\n"
            "`/extrato` (mês atual)\n"
            "`/extrato <mês> <ano>` (ex: /extrato 7 2025)\n"
            "`/extrato total`",
            parse_mode='Markdown'
        )

# Configuração do bot
def main():
    TOKEN = "8371830638:AAH8_BIlwHMVhk2F-aqm9nRWhcEuskkeqWo"
    # cria a aplicação do bot com o token colocado
    application = Application.builder().token(TOKEN).build()

    # recebe o /start e executa a função start
    application.add_handler(CommandHandler("start", start))

    # função extrato 
    application.add_handler(CommandHandler("extrato", extrato)) 

    # quando receber o texto normal, execute a função processar gasto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_gasto))

    # iniciando bot
    print("Bot iniciado....")
    application.run_polling()

# iniciando a main
if __name__ == '__main__':
    main()
