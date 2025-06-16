import sys
import os
import requests
import shutil
from bs4 import BeautifulSoup
import colorama
from colorama import Fore, Style
from tqdm import tqdm
import re

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
║                    🌐 Site Web Cloner Tool 🌐                                    ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def get_user_input():
    """Demande l'URL et le nom du fichier à l'utilisateur"""
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║                    Configuration requise                     ║{Style.RESET_ALL}")
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
    
    # Demander le type de clonage
    print(f"\n{Fore.CYAN}📋 Choisissez le type de clonage:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1. 📄 Page unique (copie uniquement la page actuelle){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2. 🌐 Site complet (copie toutes les pages liées){Style.RESET_ALL}")
    
    while True:
        clone_type = input(f"{Fore.YELLOW}Votre choix (1 ou 2): {Style.RESET_ALL}").strip()
        if clone_type in ['1', '2']:
            clone_type = int(clone_type)
            break
        else:
            print(f"{Fore.RED}❌ Veuillez entrer 1 ou 2.{Style.RESET_ALL}")
    
    # Demander le nom du dossier de destination
    while True:
        project_name = input(f"{Fore.YELLOW}📁 Entrez le nom du dossier de destination: {Style.RESET_ALL}").strip()
        if project_name:
            # Nettoyer le nom du dossier (enlever les caractères spéciaux)
            project_name = re.sub(r'[<>:"/\\|?*]', '_', project_name)
            break
        else:
            print(f"{Fore.RED}❌ Le nom du dossier ne peut pas être vide. Veuillez réessayer.{Style.RESET_ALL}")
    
    return site_url, project_name, clone_type

# Afficher le banner
print_banner()

# Obtenir les entrées utilisateur
site_name, project_name, clone_type = get_user_input()

print(f"\n{Fore.GREEN}✅ Configuration validée:{Style.RESET_ALL}")
print(f"   🌐 Site: {Fore.CYAN}{site_name}{Style.RESET_ALL}")
print(f"   📁 Dossier: {Fore.CYAN}{project_name}{Style.RESET_ALL}")
if clone_type == 1:
    print(f"   📄 Type: {Fore.CYAN}Page unique{Style.RESET_ALL}")
else:
    print(f"   🌐 Type: {Fore.CYAN}Site complet{Style.RESET_ALL}")
print(f"\n{Fore.YELLOW}🚀 Démarrage du clonage...{Style.RESET_ALL}\n")

base_dir = os.getcwd()

project_path = "../" + project_name
os.makedirs(project_path, exist_ok=True)

visited_links = []
error_links = []
total_files = 0
downloaded_files = 0

def update_progress_bar():
    """Met à jour la barre de progression globale"""
    global downloaded_files, total_files
    if total_files > 0:
        progress = (downloaded_files / total_files) * 100
        print(f"\r{Fore.CYAN}📊 Progression globale: {Fore.GREEN}{downloaded_files}/{total_files}{Style.RESET_ALL} fichiers ({progress:.1f}%)", end="", flush=True)

def save(bs, element, check):
    global downloaded_files, total_files
    links = bs.find_all(element)
    
    # Compter les fichiers à télécharger
    files_to_download = []
    for l in links:
        href = l.get("href")
        if href is not None and href not in visited_links:
            if check in href:
                files_to_download.append(href)
    
    if files_to_download:
        print(f"{Fore.YELLOW}🎨 Téléchargement des fichiers {check}...{Style.RESET_ALL}")
        
        # Barre de progression pour les fichiers CSS/JS
        with tqdm(total=len(files_to_download), desc=f"📄 Fichiers {check}", 
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
            
            for href in files_to_download:
                if href not in visited_links:
                    pbar.set_description(f"📄 {check}: {os.path.basename(href)}")
                    
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
                        error_links.append(l)
                        pbar.update(1)
                        continue

                    if r.status_code != 200:
                        error_links.append(l)
                        pbar.update(1)
                        continue

                    os.makedirs(os.path.dirname(project_path + file_name.split("?")[0]), exist_ok=True)
                    with open(project_path + file_name.split("?")[0], "wb") as f:
                        f.write(r.text.encode('utf-8'))
                        f.close()

                    visited_links.append(l)
                    downloaded_files += 1
                    update_progress_bar()
                    pbar.update(1)

def save_assets(html_text):
    global downloaded_files, total_files
    bs = BeautifulSoup(html_text, "html.parser")
    
    # Traiter les CSS et JS
    save(bs=bs, element="link", check=".css")
    save(bs=bs, element="script", check=".js")

    # Traiter les images
    links = bs.find_all("img")
    images_to_download = []
    
    for l in links:
        href = l.get("src")
        if href is not None and href not in visited_links:
            images_to_download.append(href)
    
    if images_to_download:
        print(f"{Fore.YELLOW}🖼️  Téléchargement des images...{Style.RESET_ALL}")
        
        # Barre de progression pour les images
        with tqdm(total=len(images_to_download), desc="🖼️ Images", 
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
            
            for href in images_to_download:
                if href not in visited_links:
                    pbar.set_description(f"🖼️ Image: {os.path.basename(href)}")
                    
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
                        error_links.append(l)
                        pbar.update(1)
                        continue

                    if r.status_code != 200:
                        error_links.append(l)
                        pbar.update(1)
                        continue

                    os.makedirs(os.path.dirname(project_path + file_name.split("?")[0]), exist_ok=True)
                    with open(project_path + file_name.split("?")[0], "wb") as f:
                        shutil.copyfileobj(r.raw, f)

                    visited_links.append(l)
                    downloaded_files += 1
                    update_progress_bar()
                    pbar.update(1)

def crawl(link):
    global total_files, downloaded_files
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
        downloaded_files += 1
        update_progress_bar()

        # Analyser le contenu pour compter les fichiers à télécharger
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Compter les fichiers CSS, JS et images
        css_files = [l.get("href") for l in soup.find_all("link") if l.get("href") and ".css" in l.get("href")]
        js_files = [l.get("src") for l in soup.find_all("script") if l.get("src") and ".js" in l.get("src")]
        img_files = [l.get("src") for l in soup.find_all("img") if l.get("src")]
        
        # Ajouter au total global
        total_files += len(css_files) + len(js_files) + len(img_files)

        save_assets(r.text)

        # Ne suivre les liens que si on clone le site complet
        if clone_type == 2:
            for link in soup.find_all('a'):
                try:
                    crawl(link.get("href"))
                except:
                    error_links.append(link.get("href"))

def clone_single_page():
    """Clone uniquement la page principale sans suivre les liens"""
    global total_files, downloaded_files
    
    print(f"{Fore.YELLOW}📄 Clonage de la page unique: {site_name}{Style.RESET_ALL}\n")
    
    try:
        r = requests.get(site_name)
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}❌ Erreur de connexion au site{Style.RESET_ALL}")
        sys.exit(1)

    if r.status_code != 200:
        print(f"{Fore.RED}❌ Réponse invalide du serveur{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"{Fore.GREEN}📝 Création: {project_path}/index.html{Style.RESET_ALL}")
    os.makedirs(project_path, exist_ok=True)
    with open(project_path + "/index.html", "wb") as f:
        text = r.text.replace(site_name, project_name)
        f.write(text.encode('utf-8'))
        f.close()

    visited_links.append(site_name)
    downloaded_files += 1
    update_progress_bar()

    # Analyser le contenu pour compter les fichiers à télécharger
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Compter les fichiers CSS, JS et images
    css_files = [l.get("href") for l in soup.find_all("link") if l.get("href") and ".css" in l.get("href")]
    js_files = [l.get("src") for l in soup.find_all("script") if l.get("src") and ".js" in l.get("src")]
    img_files = [l.get("src") for l in soup.find_all("img") if l.get("src")]
    
    # Ajouter au total global
    total_files += len(css_files) + len(js_files) + len(img_files)

    save_assets(r.text)

print(f"{Fore.YELLOW}🌐 Démarrage du clonage de {site_name}...{Style.RESET_ALL}\n")

# Initialiser le compteur total
total_files = 1  # Au moins la page principale
downloaded_files = 0

# Choisir le type de clonage
if clone_type == 1:
    clone_single_page()
else:
    crawl(site_name + "/")

print(f"\n\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
print(f"{Fore.GREEN}║                    RÉSUMÉ DU CLONAGE                         ║{Style.RESET_ALL}")
print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

if clone_type == 1:
    print(f"\n{Fore.CYAN}📄 Type de clonage: {Fore.GREEN}Page unique{Style.RESET_ALL}")
else:
    print(f"\n{Fore.CYAN}🌐 Type de clonage: {Fore.GREEN}Site complet{Style.RESET_ALL}")

print(f"\n{Fore.CYAN}📊 Liens traités ({len(visited_links)}):{Style.RESET_ALL}")
for link in visited_links:
    print(f"{Fore.GREEN}   ✅ {link}{Style.RESET_ALL}")

if error_links:
    print(f"\n{Fore.RED}❌ Liens en erreur ({len(error_links)}):{Style.RESET_ALL}")
    for link in error_links:
        print(f"{Fore.RED}   ❌ {link}{Style.RESET_ALL}")

if clone_type == 1:
    print(f"\n{Fore.GREEN}🎉 Clonage de la page terminé ! Le fichier a été sauvegardé dans: {Fore.CYAN}{project_path}/index.html{Style.RESET_ALL}")
else:
    print(f"\n{Fore.GREEN}🎉 Clonage du site terminé ! Le site a été sauvegardé dans: {Fore.CYAN}{project_path}{Style.RESET_ALL}")