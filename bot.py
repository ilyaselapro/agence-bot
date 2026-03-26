import logging
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

C_NOM, C_CONTACT, C_TYPE, C_ACTIVITE, C_CIBLE, C_STYLE, C_COULEURS, C_LOGO, C_PHOTOS, C_PAGES, C_SECTIONS, C_RESEAUX, C_FONCTIONS, C_BUDGET, C_DELAI, C_PLUS = range(16)
U_NOM, U_CONTACT, U_URL, U_SECTION, U_TEXTE, U_IMAGES, U_PAGE, U_BUG, U_AUTRES, U_URGENCE = range(16, 26)

def kbd(options, cols=2):
    rows = [options[i:i+cols] for i in range(0, len(options), cols)]
    return ReplyKeyboardMarkup(rows, resize_keyboard=True, one_time_keyboard=True)

def nkbd():
    return ReplyKeyboardRemove()

async def send_owner(context, text):
    await context.bot.send_message(chat_id=OWNER_ID, text=text, parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        "Bonjour " + name + "!\n\nBienvenue chez WebStudio.\n\nQue veux-tu faire ?",
        reply_markup=kbd(["Creer un site", "Mettre a jour mon site"])
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "Creer" in text:
        await update.message.reply_text("Super! Creons ton site.\n\nQuestion 1/16\n\nQuel est le nom de ton entreprise ?", reply_markup=nkbd())
        return C_NOM
    else:
        await update.message.reply_text("Question 1/10\n\nQuel est ton nom ?", reply_markup=nkbd())
        return U_NOM

async def c_nom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["nom"] = update.message.text
    await update.message.reply_text("Question 2/16\n\nTon email ou WhatsApp pour te recontacter ?")
    return C_CONTACT

async def c_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = update.message.text
    await update.message.reply_text("Question 3/16\n\nType de site ?", reply_markup=kbd(["Vitrine", "E-commerce", "Blog", "Portfolio", "Jeu", "Autre"]))
    return C_TYPE

async def c_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["type"] = update.message.text
    await update.message.reply_text("Question 4/16\n\nDecris ton activite en 2-3 phrases.", reply_markup=nkbd())
    return C_ACTIVITE

async def c_activite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["activite"] = update.message.text
    await update.message.reply_text("Question 5/16\n\nQui est ton public cible ?")
    return C_CIBLE

async def c_cible(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["cible"] = update.message.text
    await update.message.reply_text("Question 6/16\n\nStyle visuel ?", reply_markup=kbd(["Moderne", "Dark", "Pastel", "Luxe", "Gaming", "Nature", "Colore", "Classique"]))
    return C_STYLE

async def c_style(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["style"] = update.message.text
    await update.message.reply_text("Question 7/16\n\nCouleurs preferees ? (ex: bleu et or)", reply_markup=nkbd())
    return C_COULEURS

async def c_couleurs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["couleurs"] = update.message.text
    await update.message.reply_text("Question 8/16\n\nAs-tu un logo ?", reply_markup=kbd(["Oui je vais envoyer", "Non pas encore", "Je veux un logo"]))
    return C_LOGO

async def c_logo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo or update.message.document:
        context.user_data["logo"] = "Logo envoye"
    else:
        context.user_data["logo"] = update.message.text
    await update.message.reply_text("Question 9/16\n\nAs-tu des photos pour le site ?", reply_markup=kbd(["Oui je vais envoyer", "Non", "Utilise des images gratuites"]))
    return C_PHOTOS

async def c_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo or update.message.document:
        context.user_data["photos"] = "Photos envoyees"
    else:
        context.user_data["photos"] = update.message.text
    await update.message.reply_text("Question 10/16\n\nCombien de pages ?", reply_markup=kbd(["1 page", "2-3 pages", "4-6 pages", "7+ pages"]))
    return C_PAGES

async def c_pages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pages"] = update.message.text
    await update.message.reply_text("Question 11/16\n\nQuelles sections ? (ex: Accueil, A propos, Services, Contact...)", reply_markup=nkbd())
    return C_SECTIONS

async def c_sections(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["sections"] = update.message.text
    await update.message.reply_text("Question 12/16\n\nReseaux sociaux a integrer ?", reply_markup=kbd(["Instagram", "Facebook", "TikTok", "YouTube", "Tous", "Aucun"]))
    return C_RESEAUX

async def c_reseaux(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["reseaux"] = update.message.text
    await update.message.reply_text("Question 13/16\n\nFonctionnalites speciales ?", reply_markup=kbd(["Formulaire contact", "Boutique", "Rendez-vous", "Blog", "Carte Maps", "Rien"]))
    return C_FONCTIONS

async def c_fonctions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["fonctions"] = update.message.text
    await update.message.reply_text("Question 14/16\n\nBudget ?", reply_markup=kbd(["Moins 200", "200-500", "500-1000", "1000-2000", "2000+", "A discuter"]))
    return C_BUDGET

async def c_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["budget"] = update.message.text
    await update.message.reply_text("Question 15/16\n\nDelai souhaite ?", reply_markup=kbd(["Urgent -1 semaine", "1-2 semaines", "2-4 semaines", "Pas presse"]))
    return C_DELAI

async def c_delai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["delai"] = update.message.text
    await update.message.reply_text("Question 16/16\n\nInfos supplementaires ? (ou reponds Non)", reply_markup=nkbd())
    return C_PLUS

async def c_plus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["plus"] = update.message.text
    d = context.user_data
    await update.message.reply_text("Parfait! Ta demande a ete envoyee. Je te recontacte bientot!")
    msg = ("*NOUVELLE DEMANDE CREATION SITE*\n\n"
        "Nom: " + str(d.get("nom")) + "\n"
        "Contact: " + str(d.get("contact")) + "\n"
        "Type: " + str(d.get("type")) + "\n"
        "Activite: " + str(d.get("activite")) + "\n"
        "Cible: " + str(d.get("cible")) + "\n"
        "Style: " + str(d.get("style")) + "\n"
        "Couleurs: " + str(d.get("couleurs")) + "\n"
        "Logo: " + str(d.get("logo")) + "\n"
        "Photos: " + str(d.get("photos")) + "\n"
        "Pages: " + str(d.get("pages")) + "\n"
        "Sections: " + str(d.get("sections")) + "\n"
        "Reseaux: " + str(d.get("reseaux")) + "\n"
        "Fonctions: " + str(d.get("fonctions")) + "\n"
        "Budget: " + str(d.get("budget")) + "\n"
        "Delai: " + str(d.get("delai")) + "\n"
        "Infos: " + str(d.get("plus")))
    await send_owner(context, msg)
    context.user_data.clear()
    return ConversationHandler.END

async def u_nom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["u_nom"] = update.message.text
    await update.message.reply_text("Question 2/10\n\nTon email ou WhatsApp ?")
    return U_CONTACT

async def u_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["u_contact"] = update.message.text
    await update.message.reply_text("Question 3/10\n\nURL de ton site ?", reply_markup=nkbd())
    return U_URL

async def u_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["u_url"] = update.message.text
    await update.message.reply_text("Question 4/10\n\nQuelle section modifier ?", reply_markup=kbd(["Accueil", "A propos", "Services", "Galerie", "Contact", "Menu", "Autre"]))
    return U_SECTION

async def u_section(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["u_section"] = update.message.text
    await update.message.reply_text("Question 5/10\n\nNouveau texte a mettre ? (ou Non)", reply_markup=nkbd())
    return U_TEXTE

async def u_texte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["u_texte"] = update.message.text
    await update.message.reply_text("Question 6/10\n\nNouvelles images ?", reply_markup=kbd(["Oui je vais envoyer", "Non"]))
    return U_IMAGES

async def u_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo or update.message.document:
        context.user_data["u_images"] = "Images envoyees"
    else:
        context.user_data["u_images"] = update.message.text
    await update.message.reply_text("Question 7/10\n\nAjouter des pages ?", reply_markup=kbd(["Oui", "Non"]))
    return U_PAGE

async def u_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["u_page"] = update.message.text
    await update.message.reply_text("Question 8/10\n\nBug a signaler ?", reply_markup=kbd(["Oui j ai un bug", "Non tout fonctionne"]))
    return U_BUG

async def u_bug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["u_bug"] = update.message.text
    await update.message.reply_text("Question 9/10\n\nAutres demandes ?", reply_markup=kbd(["Non c est tout"]))
    return U_AUTRES

async def u_autres(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["u_autres"] = update.message.text
    await update.message.reply_text("Question 10/10\n\nUrgence ?", reply_markup=kbd(["Urgent aujourd hui", "2-3 jours", "1 semaine", "Pas presse"]))
    return U_URGENCE

async def u_urgence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["u_urgence"] = update.message.text
    d = context.user_data
    await update.message.reply_text("Demande enregistree! Je te recontacte bientot.")
    msg = ("*DEMANDE MISE A JOUR SITE*\n\n"
        "Nom: " + str(d.get("u_nom")) + "\n"
        "Contact: " + str(d.get("u_contact")) + "\n"
        "URL: " + str(d.get("u_url")) + "\n"
        "Section: " + str(d.get("u_section")) + "\n"
        "Texte: " + str(d.get("u_texte")) + "\n"
        "Images: " + str(d.get("u_images")) + "\n"
        "Nouvelle page: " + str(d.get("u_page")) + "\n"
        "Bug: " + str(d.get("u_bug")) + "\n"
        "Autres: " + str(d.get("u_autres")) + "\n"
        "Urgence: " + str(d.get("u_urgence")))
    await send_owner(context, msg)
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Annule. Envoie /start pour recommencer.", reply_markup=nkbd())
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    creation = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("Creer"), menu)],
        states={
            C_NOM: [MessageHandler(filters.ALL, c_nom)],
            C_CONTACT: [MessageHandler(filters.ALL, c_contact)],
            C_TYPE: [MessageHandler(filters.ALL, c_type)],
            C_ACTIVITE: [MessageHandler(filters.ALL, c_activite)],
            C_CIBLE: [MessageHandler(filters.ALL, c_cible)],
            C_STYLE: [MessageHandler(filters.ALL, c_style)],
            C_COULEURS: [MessageHandler(filters.ALL, c_couleurs)],
            C_LOGO: [MessageHandler(filters.ALL, c_logo)],
            C_PHOTOS: [MessageHandler(filters.ALL, c_photos)],
            C_PAGES: [MessageHandler(filters.ALL, c_pages)],
            C_SECTIONS: [MessageHandler(filters.ALL, c_sections)],
            C_RESEAUX: [MessageHandler(filters.ALL, c_reseaux)],
            C_FONCTIONS: [MessageHandler(filters.ALL, c_fonctions)],
            C_BUDGET: [MessageHandler(filters.ALL, c_budget)],
            C_DELAI: [MessageHandler(filters.ALL, c_delai)],
            C_PLUS: [MessageHandler(filters.ALL, c_plus)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    maj = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("Mettre"), menu)],
        states={
            U_NOM: [MessageHandler(filters.ALL, u_nom)],
            U_CONTACT: [MessageHandler(filters.ALL, u_contact)],
            U_URL: [MessageHandler(filters.ALL, u_url)],
            U_SECTION: [MessageHandler(filters.ALL, u_section)],
            U_TEXTE: [MessageHandler(filters.ALL, u_texte)],
            U_IMAGES: [MessageHandler(filters.ALL, u_images)],
            U_PAGE: [MessageHandler(filters.ALL, u_page)],
            U_BUG: [MessageHandler(filters.ALL, u_bug)],
            U_AUTRES: [MessageHandler(filters.ALL, u_autres)],
            U_URGENCE: [MessageHandler(filters.ALL, u_urgence)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(creation)
    app.add_handler(maj)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))
    print("Bot demarre!")
    app.run_polling()

if __name__ == "__main__":
    main()
