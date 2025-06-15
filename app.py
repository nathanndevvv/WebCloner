import sys
import os
import requests
import shutil
from bs4 import BeautifulSoup
import colorama
from colorama import Fore, Style

# Initialiser colorama pour Windows
colorama.init()

def print_banner():
    """Affiche le banner WebCloner en vert avec des caractères spéciaux"""
    banner = f"""
{Fore.GREEN}
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║    ██╗    ██╗███████╗██████╗  ██████╗██╗      ██████╗ ███╗   ██╗███████╗██████╗  ║
║    ██║    ██║██╔════╝██╔══██╗██╔════╝██║     ██╔═══██╗████╗  ██║██╔════╝██╔══██╗ ║
║    ██║ █╗ ██║█████╗  ██████╔╝██║     ██║     ██║   ██║██╔██╗ ██║█████╗  ██████╔╝ ║
║    ██║███╗██║██╔══╝  ██╔══██╗██║     ██║     ██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗ ║
║    ╚███╔███╔╝███████╗██████╔╝╚██████╗███████╗╚██████╔╝██║ ╚████║███████╗██║  ██║ ║
║     ╚══╝╚══╝ ╚══════╝╚═════╝  ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ║
║                                                                                  ║
║                    🌐 Site Web Cloner Tool 🌐                                   ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def get_user_input():
    """Demande l'URL et le nom du fichier à l'utilisateur"""
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║                    Configuration requise                    ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    # Demander l'URL du site
    while True:
        site_url = input(f"{Fore.YELLOW}🌐 Entrez l'URL du site à cloner (ex: https://example.com): {Style.RESET_ALL}").strip()
        if site_url:
            # Ajouter https:// si pas de protocole spécifié
            if not site_url.startswith(('http://', 'https://')):
                site_url = 'https://' + site_url
            break
        else:
            print(f"{Fore.RED}❌ L'URL ne peut pas être vide. Veuillez réessayer.{Style.RESET_ALL}")
    
    # Demander le nom du dossier de destination
    while True:
        project_name = input(f"{Fore.YELLOW}📁 Entrez le nom du dossier de destination: {Style.RESET_ALL}").strip()
        if project_name:
            # Nettoyer le nom du dossier (enlever les caractères spéciaux)
            import re
            project_name = re.sub(r'[<>:"/\\|?*]', '_', project_name)
            break
        else:
            print(f"{Fore.RED}❌ Le nom du dossier ne peut pas être vide. Veuillez réessayer.{Style.RESET_ALL}")
    
    return site_url, project_name

# Afficher le banner
print_banner()

# Obtenir les entrées utilisateur
site_name, project_name = get_user_input()

print(f"\n{Fore.GREEN}✅ Configuration validée:{Style.RESET_ALL}")
print(f"   🌐 Site: {Fore.CYAN}{site_name}{Style.RESET_ALL}")
print(f"   📁 Dossier: {Fore.CYAN}{project_name}{Style.RESET_ALL}")
print(f"\n{Fore.YELLOW}🚀 Démarrage du clonage...{Style.RESET_ALL}\n")

base_dir = os.getcwd()

project_path = "../" + project_name
os.makedirs(project_path, exist_ok=True)

visited_links = []
error_links = []


def save(bs, element, check):
    links = bs.find_all(element)

    for l in links:
        href = l.get("href")
        if href is not None and href not in visited_links:
            if check in href:
                href = l.get("href")
                print(f"{Fore.BLUE}📄 Téléchargement: {Fore.CYAN}{href}{Style.RESET_ALL}")
                if "//" in href:
                    path_s = href.split("/")
                    file_name = ""
                    for i in range(3, len(path_s)):
                        file_name = file_name + "/" + path_s[i]
                else:
                    file_name = href

                l = site_name + file_name

                try:
                    r = requests.get(l)
                except requests.exceptions.ConnectionError:
                    print(f"{Fore.RED}❌ Erreur de connexion: {href}{Style.RESET_ALL}")
                    error_links.append(l)
                    continue

                if r.status_code != 200:
                    print(f"{Fore.RED}❌ Erreur HTTP {r.status_code}: {href}{Style.RESET_ALL}")
                    error_links.append(l)
                    continue

                os.makedirs(os.path.dirname(project_path + file_name.split("?")[0]), exist_ok=True)
                with open(project_path + file_name.split("?")[0], "wb") as f:
                    f.write(r.text.encode('utf-8'))
                    f.close()

                print(f"{Fore.GREEN}✅ Sauvegardé: {file_name.split('?')[0]}{Style.RESET_ALL}")
                visited_links.append(l)


def save_assets(html_text):
    bs = BeautifulSoup(html_text, "html.parser")
    print(f"{Fore.YELLOW}🎨 Téléchargement des ressources CSS et JS...{Style.RESET_ALL}")
    save(bs=bs, element="link", check=".css")
    save(bs=bs, element="script", check=".js")

    print(f"{Fore.YELLOW}🖼️  Téléchargement des images...{Style.RESET_ALL}")
    links = bs.find_all("img")
    for l in links:
        href = l.get("src")
        if href is not None and href not in visited_links:
            print(f"{Fore.BLUE}🖼️  Téléchargement image: {Fore.CYAN}{href}{Style.RESET_ALL}")
            if "//" in href:
                path_s = href.split("/")
                file_name = ""
                for i in range(3, len(path_s)):
                    file_name = file_name + "/" + path_s[i]
            else:
                file_name = href

            l = site_name + file_name

            try:
                r = requests.get(l, stream=True)
            except requests.exceptions.ConnectionError:
                print(f"{Fore.RED}❌ Erreur de connexion: {href}{Style.RESET_ALL}")
                error_links.append(l)
                continue

            if r.status_code != 200:
                print(f"{Fore.RED}❌ Erreur HTTP {r.status_code}: {href}{Style.RESET_ALL}")
                error_links.append(l)
                continue

            os.makedirs(os.path.dirname(project_path + file_name.split("?")[0]), exist_ok=True)
            with open(project_path + file_name.split("?")[0], "wb") as f:
                shutil.copyfileobj(r.raw, f)

            print(f"{Fore.GREEN}✅ Image sauvegardée: {file_name.split('?')[0]}{Style.RESET_ALL}")
            visited_links.append(l)


def crawl(link):
    if "http://" not in link and "https://" not in link:
        link = site_name + link

    if site_name in link and link not in visited_links:
        print(f"{Fore.MAGENTA}🔗 Exploration: {Fore.CYAN}{link}{Style.RESET_ALL}")

        path_s = link.split("/")
        file_name = ""
        for i in range(3, len(path_s)):
            file_name = file_name + "/" + path_s[i]

        if file_name[len(file_name) - 1] != "/":
            file_name = file_name + "/"

        try:
            r = requests.get(link)
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}❌ Erreur de connexion au site{Style.RESET_ALL}")
            sys.exit(1)

        if r.status_code != 200:
            print(f"{Fore.RED}❌ Réponse invalide du serveur{Style.RESET_ALL}")
            sys.exit(1)
        
        print(f"{Fore.GREEN}📝 Création: {project_path + file_name}index.html{Style.RESET_ALL}")
        os.makedirs(os.path.dirname(project_path + file_name.split("?")[0]), exist_ok=True)
        with open(project_path + file_name.split("?")[0] + "index.html", "wb") as f:
            text = r.text.replace(site_name, project_name)
            f.write(text.encode('utf-8'))
            f.close()

        visited_links.append(link)

        save_assets(r.text)

        soup = BeautifulSoup(r.text, "html.parser")

        for link in soup.find_all('a'):
            try:
                crawl(link.get("href"))
            except:
                error_links.append(link.get("href"))


print(f"{Fore.YELLOW}🌐 Démarrage du clonage de {site_name}...{Style.RESET_ALL}\n")
crawl(site_name + "/")

print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
print(f"{Fore.GREEN}║                    RÉSUMÉ DU CLONAGE                        ║{Style.RESET_ALL}")
print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

print(f"\n{Fore.CYAN}📊 Liens traités ({len(visited_links)}):{Style.RESET_ALL}")
for link in visited_links:
    print(f"{Fore.GREEN}   ✅ {link}{Style.RESET_ALL}")

if error_links:
    print(f"\n{Fore.RED}❌ Liens en erreur ({len(error_links)}):{Style.RESET_ALL}")
    for link in error_links:
        print(f"{Fore.RED}   ❌ {link}{Style.RESET_ALL}")

print(f"\n{Fore.GREEN}🎉 Clonage terminé ! Le site a été sauvegardé dans: {Fore.CYAN}{project_path}{Style.RESET_ALL}")