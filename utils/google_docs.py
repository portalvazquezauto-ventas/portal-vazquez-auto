import os
import json
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]


def _get_docs_service():
    sa_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "credentials/google_service_account.json")
    creds = service_account.Credentials.from_service_account_file(sa_path, scopes=SCOPES)
    return build("docs", "v1", credentials=creds)


def _extract_text_from_doc(doc: dict) -> str:
    """Extrae texto plano del documento de Google Docs."""
    full_text = []
    body = doc.get("body", {})
    for element in body.get("content", []):
        paragraph = element.get("paragraph")
        if not paragraph:
            continue
        para_text = ""
        for pe in paragraph.get("elements", []):
            tr = pe.get("textRun")
            if tr:
                para_text += tr.get("content", "")
        full_text.append(para_text)
    return "".join(full_text)


def fetch_manual_from_google_docs() -> list[dict]:
    """
    Lee el manual de Google Docs y lo parsea en secciones.
    Retorna lista de dicts con keys: section_number, title, content
    """
    doc_id = os.getenv("GOOGLE_DOC_ID", "1CILYMGIrof1ieBP_gPVTd_eh6Ct2mFc5")
    service = _get_docs_service()
    doc = service.documents().get(documentId=doc_id).execute()
    raw_text = _extract_text_from_doc(doc)
    return _parse_sections(raw_text)


def _parse_sections(text: str) -> list[dict]:
    """Parsea el texto del manual en secciones numeradas."""
    section_pattern = re.compile(
        r'^((?:\d+(?:\.\d+)*)\s+.+)$',
        re.MULTILINE
    )

    SECTION_TITLES = {
        "1": ("1", "Introducción y Regla Central"),
        "2": ("2", "Propósito y Objetivos"),
        "2.1": ("2.1", "Propósito"),
        "2.2": ("2.2", "Objetivos Generales"),
        "2.3": ("2.3", "El Vendedor Vázquez Auto"),
        "3": ("3", "Estructura del Área y Roles"),
        "3.1": ("3.1", "Estructura del Área"),
        "3.2": ("3.2", "Descripción de Roles"),
        "4": ("4", "Competencias del Vendedor"),
        "4.1": ("4.1", "Competencias Técnicas"),
        "4.2": ("4.2", "Competencias Blandas"),
        "5.1": ("5.1", "Primer Contacto y Calificación"),
        "5.2": ("5.2", "Asesoramiento e Identificación de Necesidades"),
        "5.3": ("5.3", "Cotización Profesional"),
        "5.4": ("5.4", "Negociación y Seguimiento Consultivo"),
        "5.5": ("5.5", "Cierre de Venta — SDR + Seña"),
        "5.6": ("5.6", "Gestión y Cancelación Total"),
        "5.7": ("5.7", "Entrega de la Unidad"),
        "5.8": ("5.8", "Postventa Cumplida"),
        "6": ("6", "Gestión de Leads en CRM"),
        "7": ("7", "Indicadores y Rutina del Encargado"),
        "8": ("8", "Condiciones Administrativas"),
        "9": ("9", "Límites y Reglas No Negociables"),
        "10": ("10", "Anexos y Políticas"),
    }

    sections = []
    lines = text.split('\n')
    current_section = None
    current_content = []

    for line in lines:
        match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)$', line.strip())
        if match:
            num = match.group(1)
            if num in SECTION_TITLES or len(sections) == 0:
                if current_section:
                    current_section["content"] = "\n".join(current_content).strip()
                    sections.append(current_section)
                    current_content = []

                title = SECTION_TITLES.get(num, (num, match.group(2)))
                current_section = {
                    "section_number": title[0],
                    "title": title[1],
                    "content": ""
                }
                continue
        if current_section:
            current_content.append(line)

    if current_section and current_content:
        current_section["content"] = "\n".join(current_content).strip()
        sections.append(current_section)

    if not sections:
        sections = _get_default_sections()

    return sections


def _get_default_sections() -> list[dict]:
    """Secciones por defecto si no se puede parsear el doc."""
    return [
        {"section_number": "1", "title": "Introducción y Regla Central", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "2", "title": "Propósito y Objetivos", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "3", "title": "Estructura del Área y Roles", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "4", "title": "Competencias del Vendedor", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "5.1", "title": "Primer Contacto y Calificación", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "5.2", "title": "Asesoramiento e Identificación de Necesidades", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "5.3", "title": "Cotización Profesional", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "5.4", "title": "Negociación y Seguimiento Consultivo", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "5.5", "title": "Cierre de Venta — SDR + Seña", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "5.6", "title": "Gestión y Cancelación Total", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "5.7", "title": "Entrega de la Unidad", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "5.8", "title": "Postventa Cumplida", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "6", "title": "Gestión de Leads en CRM", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "7", "title": "Indicadores y Rutina del Encargado", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "8", "title": "Condiciones Administrativas", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "9", "title": "Límites y Reglas No Negociables", "content": "Contenido pendiente de actualización desde Google Docs."},
        {"section_number": "10", "title": "Anexos y Políticas", "content": "Contenido pendiente de actualización desde Google Docs."},
    ]
