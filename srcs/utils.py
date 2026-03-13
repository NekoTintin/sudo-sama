import sys
import os
import gettext
import locale
import shutil
from dotenv import load_dotenv
import builtins

# Stop VScode warnings
if not hasattr(builtins, "_"):
	_ = lambda s: s

def reset_all():
	print(_("reset_all_warning"))

	if (input() == "YES"):
		print(_("reset_all_ask_again"))
		if (input() == "YES I WILL DO IT"):
			shutil.rmtree("data/")
			sys.exit(0)
	sys.exit(_("reset_all_cancelled"))

def no_dotenv_error() -> None:
	print(_("no_dotenv_error"))

	token = input(_("insert_discord_token"))
	if token == None:
		print(_("no_token_provided"))
		sys.exit(1)
	model = input(_("insert_model"))
	if model == None:
		print(_("no_model_provided"))
		sys.exit(1)

	with open(".env", "w") as env_file:
		env_file.write(f'CLIENT_TOKEN = "{token}"')
		env_file.write('\n\n')
		env_file.write(f'MODEL = "{model}"')
	sys.exit(1)

def dotenv_error() -> None:
	print(_("dotenv_load_error"))
	sys.exit(1)

def print_help() -> None:
	print(_("help_message"))
	sys.exit(0)

def setup_i18n(language: str = None) -> None:
	if language is None:
		system_lang = locale.getlocale()[0]
		lang = system_lang.split("_")[0] if system_lang else "en"
		language = lang if lang in ["en", "fr"] else "en"

	localedir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "locale")

	try:
		translation = gettext.translation(
			language,
			localedir=localedir,
			languages=[language],
			fallback=False
		)
		# Installer manuellement _ dans les builtins
		import builtins
		builtins._ = translation.gettext
	except Exception as e:
		print(f"Error when loading translations: {e}")
		sys.exit(1)

def error_management() -> None:
	if len(sys.argv) > 1:
		if (sys.argv[1] == "--reset"):
			reset_all()
		elif (sys.argv[1] == "--help") or (sys.argv[1] == "-h"):
			print_help()
		else:
			print(_("unknown_arg"))
			print_help()
	if not os.path.exists(".env"):
		no_dotenv_error()
	if not load_dotenv():
		dotenv_error()