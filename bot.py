#!/usr/bin/env python3
“””
╔══════════════════════════════════════════════════════════╗
║         BOT TELEGRAM — AGENCE WEB                        ║
║  Formulaire Création + Mise à jour de site               ║
╚══════════════════════════════════════════════════════════╝

CONFIGURATION RAPIDE :

1. Remplace BOT_TOKEN par le token de ton bot (@BotFather)
1. Remplace OWNER_ID par ton ID Telegram (@userinfobot)
1. Lance : python bot.py
   “””

import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
Application, CommandHandler, MessageHandler,
ConversationHandler, filters, ContextTypes
)

# ════════════════════════════════════════════════════════

# ⚙️  CONFIGURATION — MODIFIE CES 2 LIGNES

# ════════════════════════════════════════════════════════

BOT_TOKEN = “7788151587:AAFWYIIxkIsp8wZ1_m8Missi1JWSmai3ZS8”
OWNER_ID  = 922766851

# ════════════════════════════════════════════════════════

logging.basicConfig(format=”%(asctime)s - %(levelname)s - %(message)s”, level=logging.INFO)

# ── ÉTATS DU FORMULAIRE CRÉATION ──────────────────────

(
C_NOM, C_CONTACT, C_TYPE_SITE, C_ACTIVITE, C_CIBLE,
C_STYLE, C_COULEURS, C_FONTS, C_LOGO, C_PHOTOS,
C_NB_PAGES, C_SECTIONS, C_TEXTES, C_LANGUES,
C_RESEAUX, C_FONCTIONNALITES, C_CONCURRENTS,
C_BUDGET, C_DELAI, C_INFOS_SUPP
) = range(20)

# ── ÉTATS DU FORMULAIRE MISE À JOUR ───────────────────

(
U_NOM, U_CONTACT, U_SITE_URL,
U_SECTION, U_NOUVEAU_TEXTE, U_IMAGES,
U_AJOUT_PAGE, U_BUG, U_AUTRES, U_URGENCE
) = range(20, 30)

# ════════════════════════════════════════════════════════

# HELPERS

# ════════════════════════════════════════════════════════

def kbd(options, cols=2):
“”“Crée un clavier rapide.”””
rows = [options[i:i+cols] for i in range(0, len(options), cols)]
return ReplyKeyboardMarkup(rows, resize_keyboard=True, one_time_keyboard=True)

def no_kbd():
return ReplyKeyboardRemove()

async def send_to_owner(context, text):
“”“Envoie le résumé final à l’owner (toi).”””
await context.bot.send_message(chat_id=OWNER_ID, text=text, parse_mode=“Markdown”)

# ════════════════════════════════════════════════════════

# COMMANDE /start

# ════════════════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
name = update.effective_user.first_name
await update.message.reply_text(
f”👋 *Bonjour {name} !*\n\n”
“Bienvenue chez *WebStudio* 🚀\n\n”
“Je suis ton assistant pour :\n”
“📝 *Créer* un nouveau site web\n”
“🔧 *Mettre à jour* un site existant\n\n”
“Que souhaites-tu faire ?”,
parse_mode=“Markdown”,
reply_markup=kbd([“📝 Créer un site”, “🔧 Mettre à jour mon site”])
)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
text = update.message.text
if “Créer” in text:
await update.message.reply_text(
“🚀 *Super ! Commençons la création de ton site.*\n\n”
“Je vais te poser quelques questions pour que ton site soit *parfait*.\n”
“Réponds le plus précisément possible 😊\n\n”
“━━━━━━━━━━━━━━━━\n”
“*Question 1/20*\n\n”
“👤 Quel est le *nom de ton entreprise* ou ton nom complet ?”,
parse_mode=“Markdown”,
reply_markup=no_kbd()
)
return C_NOM
elif “Mettre à jour” in text:
await update.message.reply_text(
“🔧 *Demande de mise à jour*\n\n”
“Je vais noter toutes tes modifications 📋\n\n”
“━━━━━━━━━━━━━━━━\n”
“*Question 1/10*\n\n”
“👤 Quel est ton *nom* (ou nom de l’entreprise) ?”,
parse_mode=“Markdown”,
reply_markup=no_kbd()
)
return U_NOM

# ════════════════════════════════════════════════════════

# FORMULAIRE CRÉATION — 20 ÉTAPES

# ════════════════════════════════════════════════════════

async def c_nom(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_nom”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 2/20*\n\n”
“📱 Quel est ton *email ou numéro WhatsApp* pour te recontacter ?”,
parse_mode=“Markdown”
)
return C_CONTACT

async def c_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_contact”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 3/20*\n\n”
“🌐 Quel *type de site* veux-tu ?”,
parse_mode=“Markdown”,
reply_markup=kbd([
“🏪 Vitrine (présentation)”,
“🛒 E-commerce (boutique)”,
“📝 Blog / Magazine”,
“💼 Portfolio”,
“🎮 Jeu en ligne”,
“📋 Autre”
])
)
return C_TYPE_SITE

async def c_type_site(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_type”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 4/20*\n\n”
“🏢 Décris ton *activité ou ton projet* en 2-3 phrases.\n\n”
“*Ex: Je vends des bijoux faits main, je suis coach sportif, j’ai un restaurant…*”,
parse_mode=“Markdown”,
reply_markup=no_kbd()
)
return C_ACTIVITE

async def c_activite(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_activite”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 5/20*\n\n”
“🎯 Qui est ton *public cible* ? (âge, profession, centres d’intérêt…)\n\n”
“*Ex: Femmes 25-45 ans, entrepreneurs, étudiants…*”,
parse_mode=“Markdown”
)
return C_CIBLE

async def c_cible(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_cible”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 6/20*\n\n”
“🎨 Quel *style visuel* tu imagines pour ton site ?”,
parse_mode=“Markdown”,
reply_markup=kbd([
“✨ Moderne & Épuré”,
“🌙 Dark / Sombre”,
“🌸 Doux & Pastel”,
“💎 Luxe & Élégant”,
“🎮 Gaming / Néon”,
“🌿 Nature & Bio”,
“⚡ Dynamique & Coloré”,
“🏛️ Classique & Formel”
])
)
return C_STYLE

async def c_style(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_style”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 7/20*\n\n”
“🎨 Quelles sont tes *couleurs préférées* pour le site ?\n\n”
“*Ex: Bleu marine et doré, noir et rouge, vert et blanc… ou envoie un code couleur #FF5500*\n\n”
“*(Réponds ‘Je sais pas’ si tu veux me laisser choisir)*”,
parse_mode=“Markdown”,
reply_markup=no_kbd()
)
return C_COULEURS

async def c_couleurs(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_couleurs”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 8/20*\n\n”
“🔤 Tu as une *préférence de police / typographie* ?\n\n”
“*Ex: Moderne, manuscrite, très lisible, fantaisie…*\n”
“*(Réponds ‘Je sais pas’ pour laisser faire)*”,
parse_mode=“Markdown”
)
return C_FONTS

async def c_fonts(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_fonts”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 9/20*\n\n”
“🖼️ As-tu un *logo* ?”,
parse_mode=“Markdown”,
reply_markup=kbd([“✅ Oui, je vais l’envoyer”, “❌ Non, pas encore”, “🎨 J’en veux un créé”])
)
return C_LOGO

async def c_logo(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.photo:
context.user_data[“c_logo”] = “📎 Logo envoyé en photo”
elif update.message.document:
context.user_data[“c_logo”] = “📎 Logo envoyé en fichier”
else:
context.user_data[“c_logo”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 10/20*\n\n”
“📸 As-tu des *photos / images* pour le site ?\n\n”
“*(Tu peux en envoyer maintenant, ou plusieurs à la suite)*”,
parse_mode=“Markdown”,
reply_markup=kbd([“📸 Je vais en envoyer”, “🚫 Pas de photos”, “🖼️ Utilise des images gratuites”])
)
return C_PHOTOS

async def c_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.photo or update.message.document:
context.user_data[“c_photos”] = “📎 Photos envoyées”
else:
context.user_data[“c_photos”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 11/20*\n\n”
“📄 Combien de *pages* veux-tu sur ton site ?”,
parse_mode=“Markdown”,
reply_markup=kbd([“1 page (one-page)”, “2-3 pages”, “4-6 pages”, “7+ pages”])
)
return C_NB_PAGES

async def c_nb_pages(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_nb_pages”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 12/20*\n\n”
“📋 Quelles *sections* veux-tu sur ton site ?\n_(Sélectionne toutes celles qui t’intéressent, une par message)_\n\n”
“Sections disponibles :\n”
“• Accueil / Hero\n• À propos\n• Services / Offres\n• Portfolio / Galerie\n”
“• Témoignages\n• Blog\n• FAQ\n• Contact\n• Équipe\n• Tarifs\n\n”
“*Écris toutes les sections que tu veux, séparées par des virgules.*”,
parse_mode=“Markdown”,
reply_markup=no_kbd()
)
return C_SECTIONS

async def c_sections(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_sections”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 13/20*\n\n”
“✍️ As-tu déjà des *textes / contenus* à mettre sur le site ?\n\n”
“*Ex: description de tes services, ta biographie, tes tarifs…*\n”
“*(Tu peux coller le texte ici directement, ou dire ‘Je ferai ça plus tard’)*”,
parse_mode=“Markdown”
)
return C_TEXTES

async def c_textes(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_textes”] = update.message.text[:500] + (”…” if len(update.message.text) > 500 else “”)
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 14/20*\n\n”
“🌍 En quelle(s) *langue(s)* doit être le site ?”,
parse_mode=“Markdown”,
reply_markup=kbd([“🇫🇷 Français”, “🇬🇧 Anglais”, “🇫🇷🇬🇧 Français + Anglais”, “Autre”])
)
return C_LANGUES

async def c_langues(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_langues”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 15/20*\n\n”
“📱 Quels *réseaux sociaux* veux-tu intégrer au site ?”,
parse_mode=“Markdown”,
reply_markup=kbd([
“📸 Instagram”, “📘 Facebook”,
“🐦 Twitter/X”, “💼 LinkedIn”,
“🎵 TikTok”, “▶️ YouTube”,
“✅ Tous”, “🚫 Aucun”
])
)
return C_RESEAUX

async def c_reseaux(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_reseaux”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 16/20*\n\n”
“⚙️ As-tu besoin de *fonctionnalités spéciales* ?\n\n”
“*Sélectionne tout ce qui te convient (ou écris librement)*”,
parse_mode=“Markdown”,
reply_markup=kbd([
“📩 Formulaire de contact”,
“🛒 Boutique en ligne”,
“📅 Prise de rendez-vous”,
“💬 Chat en direct”,
“🗺️ Carte Google Maps”,
“📊 Blog / Articles”,
“🔐 Espace membre”,
“🚫 Rien de spécial”
])
)
return C_FONCTIONNALITES

async def c_fonctionnalites(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_fonctionnalites”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 17/20*\n\n”
“🔍 As-tu des *sites concurrents ou des références* que tu aimes ?\n\n”
“*Colle des URLs ou des noms de marques dont tu aimes le style*\n”
“*(Réponds ‘Non’ si tu n’en as pas)*”,
parse_mode=“Markdown”,
reply_markup=no_kbd()
)
return C_CONCURRENTS

async def c_concurrents(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_concurrents”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 18/20*\n\n”
“💰 Quel est ton *budget approximatif* pour ce site ?”,
parse_mode=“Markdown”,
reply_markup=kbd([
“🟢 Moins de 200€”,
“🔵 200€ - 500€”,
“🟣 500€ - 1000€”,
“🔴 1000€ - 2000€”,
“⚫ 2000€+”,
“❓ À discuter”
])
)
return C_BUDGET

async def c_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_budget”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 19/20*\n\n”
“📅 Quel est ton *délai souhaité* pour la livraison ?”,
parse_mode=“Markdown”,
reply_markup=kbd([
“⚡ Urgent (- d’1 semaine)”,
“🚀 Rapide (1-2 semaines)”,
“👍 Normal (2-4 semaines)”,
“🗓️ Pas pressé (+ d’1 mois)”
])
)
return C_DELAI

async def c_delai(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_delai”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 20/20 — Dernière étape !* 🎉\n\n”
“💬 Y a-t-il des *informations supplémentaires* importantes que je dois savoir ?\n\n”
“*Tout détail qui n’a pas été couvert, des contraintes particulières, des envies spéciales…*\n”
“*(Réponds ‘Non, c’est tout’ si tu n’as rien à ajouter)*”,
parse_mode=“Markdown”,
reply_markup=no_kbd()
)
return C_INFOS_SUPP

async def c_infos_supp(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“c_infos_supp”] = update.message.text
d = context.user_data

```
# Confirmation au client
await update.message.reply_text(
    "✅ *Parfait ! Formulaire complété avec succès !*\n\n"
    "Voici un récapitulatif de ta demande :\n\n"
    f"👤 *Client :* {d.get('c_nom')}\n"
    f"📱 *Contact :* {d.get('c_contact')}\n"
    f"🌐 *Type :* {d.get('c_type')}\n"
    f"💰 *Budget :* {d.get('c_budget')}\n"
    f"📅 *Délai :* {d.get('c_delai')}\n\n"
    "📬 *Ta demande a bien été transmise !*\n"
    "Tu seras recontacté(e) très prochainement 🚀\n\n"
    "_Tu peux envoyer /start pour faire une nouvelle demande._",
    parse_mode="Markdown",
    reply_markup=no_kbd()
)

# Résumé complet envoyé à l'owner
summary = (
    "🔔 *NOUVELLE DEMANDE DE CRÉATION DE SITE*\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    f"👤 *Nom :* {d.get('c_nom')}\n"
    f"📱 *Contact :* {d.get('c_contact')}\n\n"
    f"🌐 *Type de site :* {d.get('c_type')}\n"
    f"🏢 *Activité :* {d.get('c_activite')}\n"
    f"🎯 *Cible :* {d.get('c_cible')}\n\n"
    f"🎨 *Style :* {d.get('c_style')}\n"
    f"🎨 *Couleurs :* {d.get('c_couleurs')}\n"
    f"🔤 *Typo :* {d.get('c_fonts')}\n\n"
    f"🖼️ *Logo :* {d.get('c_logo')}\n"
    f"📸 *Photos :* {d.get('c_photos')}\n\n"
    f"📄 *Nb pages :* {d.get('c_nb_pages')}\n"
    f"📋 *Sections :* {d.get('c_sections')}\n"
    f"✍️ *Textes :* {d.get('c_textes')}\n\n"
    f"🌍 *Langue(s) :* {d.get('c_langues')}\n"
    f"📱 *Réseaux :* {d.get('c_reseaux')}\n"
    f"⚙️ *Fonctionnalités :* {d.get('c_fonctionnalites')}\n\n"
    f"🔍 *Références :* {d.get('c_concurrents')}\n\n"
    f"💰 *Budget :* {d.get('c_budget')}\n"
    f"📅 *Délai :* {d.get('c_delai')}\n\n"
    f"💬 *Infos supp :* {d.get('c_infos_supp')}\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━"
)
await send_to_owner(context, summary)
context.user_data.clear()
return ConversationHandler.END
```

# ════════════════════════════════════════════════════════

# FORMULAIRE MISE À JOUR — 10 ÉTAPES

# ════════════════════════════════════════════════════════

async def u_nom(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“u_nom”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 2/10*\n\n”
“📱 Ton *email ou numéro* pour te recontacter ?”,
parse_mode=“Markdown”
)
return U_CONTACT

async def u_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“u_contact”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 3/10*\n\n”
“🌐 Quelle est *l’adresse (URL) de ton site* à modifier ?\n\n”
“*Ex: monsite.netlify.app ou www.monsite.fr*\n”
“*(Réponds ‘Je sais pas’ si tu l’as pas sous la main)*”,
parse_mode=“Markdown”
)
return U_SITE_URL

async def u_site_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“u_url”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 4/10*\n\n”
“📍 *Quelle(s) section(s)* du site veux-tu modifier ?\n\n”
“*Ex: Header, page Accueil, section Contact, page À propos…*”,
parse_mode=“Markdown”,
reply_markup=kbd([
“🏠 Accueil / Hero”,
“👤 À propos”,
“🛠️ Services”,
“📸 Galerie / Photos”,
“💬 Témoignages”,
“📩 Contact”,
“🔝 Navigation / Menu”,
“📄 Autre page”
])
)
return U_SECTION

async def u_section(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“u_section”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 5/10*\n\n”
“✍️ Quel est le *nouveau texte* à mettre ?\n\n”
“*Colle directement le texte ici, le plus précis possible*\n”
“*(Réponds ‘Pas de changement texte’ si c’est uniquement des images)*”,
parse_mode=“Markdown”,
reply_markup=no_kbd()
)
return U_NOUVEAU_TEXTE

async def u_nouveau_texte(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“u_texte”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 6/10*\n\n”
“📸 As-tu des *nouvelles images / photos* à intégrer ?”,
parse_mode=“Markdown”,
reply_markup=kbd([“📸 Oui, je vais les envoyer”, “🚫 Non, pas d’images”])
)
return U_IMAGES

async def u_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.photo or update.message.document:
context.user_data[“u_images”] = “📎 Images envoyées”
else:
context.user_data[“u_images”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 7/10*\n\n”
“📄 Veux-tu *ajouter de nouvelles pages* au site ?”,
parse_mode=“Markdown”,
reply_markup=kbd([“✅ Oui”, “❌ Non”])
)
return U_AJOUT_PAGE

async def u_ajout_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
rep = update.message.text
if “Oui” in rep:
await update.message.reply_text(
“📄 Décris les *nouvelles pages* à ajouter :\n\n”
“*Ex: Une page Tarifs avec 3 offres, une page Blog…*”,
parse_mode=“Markdown”,
reply_markup=no_kbd()
)
context.user_data[“u_ajout_page”] = “À préciser”
else:
context.user_data[“u_ajout_page”] = “Non”
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 8/10*\n\n”
“🐛 As-tu des *bugs ou problèmes* à signaler ?”,
parse_mode=“Markdown”,
reply_markup=kbd([“🐛 Oui, j’ai un bug”, “✅ Non, tout fonctionne”])
)
return U_BUG
return U_AJOUT_PAGE

async def u_ajout_page_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“u_ajout_page”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 8/10*\n\n”
“🐛 As-tu des *bugs ou problèmes* à signaler ?”,
parse_mode=“Markdown”,
reply_markup=kbd([“🐛 Oui, j’ai un bug”, “✅ Non, tout fonctionne”])
)
return U_BUG

async def u_bug(update: Update, context: ContextTypes.DEFAULT_TYPE):
rep = update.message.text
if “bug” in rep.lower() or “Oui” in rep:
context.user_data[“u_bug”] = “À préciser”
await update.message.reply_text(
“🐛 Décris le *bug* :\n\n”
“*Ex: Le formulaire ne s’envoie pas, une image ne charge pas, le menu mobile bug…*”,
parse_mode=“Markdown”,
reply_markup=no_kbd()
)
else:
context.user_data[“u_bug”] = “Aucun bug signalé”
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 9/10*\n\n”
“💬 As-tu d’*autres demandes* non listées ci-dessus ?”,
parse_mode=“Markdown”,
reply_markup=kbd([“🚫 Non, c’est tout”])
)
return U_AUTRES
return U_BUG

async def u_bug_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“u_bug”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 9/10*\n\n”
“💬 As-tu d’*autres demandes* non listées ci-dessus ?”,
parse_mode=“Markdown”,
reply_markup=kbd([“🚫 Non, c’est tout”])
)
return U_AUTRES

async def u_autres(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“u_autres”] = update.message.text
await update.message.reply_text(
“━━━━━━━━━━━━━━━━\n*Question 10/10 — Dernière !* 🎉\n\n”
“⚡ Quelle est l’*urgence* de cette mise à jour ?”,
parse_mode=“Markdown”,
reply_markup=kbd([
“🔴 Urgent (aujourd’hui)”,
“🟠 Rapide (2-3 jours)”,
“🟢 Normal (1 semaine)”,
“⚪ Pas pressé”
])
)
return U_URGENCE

async def u_urgence(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data[“u_urgence”] = update.message.text
d = context.user_data

```
# Confirmation au client
await update.message.reply_text(
    "✅ *Demande de mise à jour enregistrée !*\n\n"
    f"👤 *Client :* {d.get('u_nom')}\n"
    f"🌐 *Site :* {d.get('u_url')}\n"
    f"📍 *Section :* {d.get('u_section')}\n"
    f"⚡ *Urgence :* {d.get('u_urgence')}\n\n"
    "📬 Ta demande a été transmise !\n"
    "Tu seras recontacté(e) rapidement 🚀\n\n"
    "_Envoie /start pour une nouvelle demande._",
    parse_mode="Markdown",
    reply_markup=no_kbd()
)

# Résumé envoyé à l'owner
summary = (
    "🔔 *DEMANDE DE MISE À JOUR DE SITE*\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    f"👤 *Nom :* {d.get('u_nom')}\n"
    f"📱 *Contact :* {d.get('u_contact')}\n"
    f"🌐 *URL du site :* {d.get('u_url')}\n\n"
    f"📍 *Section à modifier :* {d.get('u_section')}\n"
    f"✍️ *Nouveau texte :* {d.get('u_texte')}\n"
    f"📸 *Images :* {d.get('u_images')}\n\n"
    f"📄 *Nouvelles pages :* {d.get('u_ajout_page')}\n"
    f"🐛 *Bugs :* {d.get('u_bug')}\n"
    f"💬 *Autres demandes :* {d.get('u_autres')}\n\n"
    f"⚡ *Urgence :* {d.get('u_urgence')}\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━"
)
await send_to_owner(context, summary)
context.user_data.clear()
return ConversationHandler.END
```

# ── ANNULATION ────────────────────────────────────────

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
context.user_data.clear()
await update.message.reply_text(
“❌ *Demande annulée.*\n\nEnvoie /start pour recommencer.”,
parse_mode=“Markdown”,
reply_markup=no_kbd()
)
return ConversationHandler.END

# ════════════════════════════════════════════════════════

# MAIN

# ════════════════════════════════════════════════════════

def main():
app = Application.builder().token(BOT_TOKEN).build()

```
# Conversation CRÉATION
creation_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("Créer"), menu)],
    states={
        C_NOM:             [MessageHandler(filters.ALL, c_nom)],
        C_CONTACT:         [MessageHandler(filters.ALL, c_contact)],
        C_TYPE_SITE:       [MessageHandler(filters.ALL, c_type_site)],
        C_ACTIVITE:        [MessageHandler(filters.ALL, c_activite)],
        C_CIBLE:           [MessageHandler(filters.ALL, c_cible)],
        C_STYLE:           [MessageHandler(filters.ALL, c_style)],
        C_COULEURS:        [MessageHandler(filters.ALL, c_couleurs)],
        C_FONTS:           [MessageHandler(filters.ALL, c_fonts)],
        C_LOGO:            [MessageHandler(filters.ALL & ~filters.COMMAND, c_logo)],
        C_PHOTOS:          [MessageHandler(filters.ALL & ~filters.COMMAND, c_photos)],
        C_NB_PAGES:        [MessageHandler(filters.ALL, c_nb_pages)],
        C_SECTIONS:        [MessageHandler(filters.ALL, c_sections)],
        C_TEXTES:          [MessageHandler(filters.ALL, c_textes)],
        C_LANGUES:         [MessageHandler(filters.ALL, c_langues)],
        C_RESEAUX:         [MessageHandler(filters.ALL, c_reseaux)],
        C_FONCTIONNALITES: [MessageHandler(filters.ALL, c_fonctionnalites)],
        C_CONCURRENTS:     [MessageHandler(filters.ALL, c_concurrents)],
        C_BUDGET:          [MessageHandler(filters.ALL, c_budget)],
        C_DELAI:           [MessageHandler(filters.ALL, c_delai)],
        C_INFOS_SUPP:      [MessageHandler(filters.ALL, c_infos_supp)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

# Conversation MISE À JOUR
update_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("Mettre à jour"), menu)],
    states={
        U_NOM:          [MessageHandler(filters.ALL, u_nom)],
        U_CONTACT:      [MessageHandler(filters.ALL, u_contact)],
        U_SITE_URL:     [MessageHandler(filters.ALL, u_site_url)],
        U_SECTION:      [MessageHandler(filters.ALL, u_section)],
        U_NOUVEAU_TEXTE:[MessageHandler(filters.ALL, u_nouveau_texte)],
        U_IMAGES:       [MessageHandler(filters.ALL & ~filters.COMMAND, u_images)],
        U_AJOUT_PAGE:   [MessageHandler(filters.Regex("Oui"), u_ajout_page),
                         MessageHandler(filters.Regex("Non"), u_ajout_page),
                         MessageHandler(filters.TEXT & ~filters.COMMAND, u_ajout_page_detail)],
        U_BUG:          [MessageHandler(filters.Regex("bug|Oui"), u_bug),
                         MessageHandler(filters.Regex("Non|fonctionne"), u_bug),
                         MessageHandler(filters.TEXT & ~filters.COMMAND, u_bug_detail)],
        U_AUTRES:       [MessageHandler(filters.ALL, u_autres)],
        U_URGENCE:      [MessageHandler(filters.ALL, u_urgence)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(creation_handler)
app.add_handler(update_handler)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))

print("✅ Bot démarré ! En attente de messages...")
app.run_polling()
```

if **name** == “**main**”:
main()
