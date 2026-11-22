PAGINAS_CONOCIDAS = {
    "google.com": "Sitio oficial de Google",
    "mozilla.org": "Bienvenido a Mozilla",
    "openai.com": "Sitio oficial de OpenAI",
    "stackoverflow.com": "Bienvenido a Stack Overflow",
    "merida.anahuac.mx": "Bienvenido a la Universidad Anáhuac Mayab",
    "github.com": "Sitio oficial de GitHub",
    "youtube.com": "Bienvenido a YouTube",
    "wikipedia.org": "Wikipedia, la enciclopedia libre"
}

CARACTERES_DOMINIO = "abcdefghijklmnopqrstuvwxyz0123456789-.:"


def tiene_protocolo(url):
    minusculas = url.lower()
    return minusculas.startswith("http://") or minusculas.startswith("https://")


def obtener_protocolo(url):
    if url.lower().startswith("http://"):
        return "http://"
    return "https://"


def quitar_protocolo(url):
    minusculas = url.lower()
    if minusculas.startswith("https://"):
        return url[8:]
    if minusculas.startswith("http://"):
        return url[7:]
    return url


def obtener_host(url):
    partes = quitar_protocolo(url).split("/")
    return partes[0].lower()


def obtener_dominio(url):
    dominio = obtener_host(url)
    if dominio.startswith("www."):
        dominio = dominio[4:]
    return dominio


def obtener_ruta(url):
    resto = quitar_protocolo(url)
    posicion = resto.find("/")
    if posicion == -1:
        return ""
    ruta = resto[posicion:]
    while ruta.endswith("/"):
        ruta = ruta[:-1]
    return ruta


def dominio_valido(dominio):
    if "." not in dominio:
        return False
    if dominio.startswith(".") or dominio.endswith("."):
        return False
    if dominio.startswith("-") or ".." in dominio:
        return False
    for caracter in dominio:
        if caracter not in CARACTERES_DOMINIO:
            return False
    return True


def normalizar_url(texto):
    url = texto.strip()
    if url == "" or " " in url:
        return None
    if not tiene_protocolo(url):
        if "://" in url:
            return None
        url = "https://" + url
    host = obtener_host(url)
    if not dominio_valido(host):
        return None
    return obtener_protocolo(url) + host + obtener_ruta(url)


def clave_pagina(url):
    return obtener_dominio(url) + obtener_ruta(url)


def obtener_descripcion(url):
    dominio = obtener_dominio(url)
    if dominio in PAGINAS_CONOCIDAS:
        return PAGINAS_CONOCIDAS[dominio]
    return "Bienvenido a " + dominio
