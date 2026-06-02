import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()


def generate_quiz_questions(section_title: str, section_content: str, n: int = 3) -> list[dict]:
    """
    Genera n preguntas de multiple choice para una sección del manual.
    Retorna lista de dicts: {question, options: [str x4], correct: int (0-3)}
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return _fallback_questions(section_title)

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Generá exactamente {n} preguntas de múltiple choice para validar que alguien leyó esta sección del Manual de Ventas Vázquez Auto.

Sección: {section_title}

Contenido:
{section_content[:3000]}

Reglas:
- Las preguntas deben ser sencillas y directas — si leyeron el contenido, deben poder responderlas.
- 4 opciones por pregunta, solo una correcta.
- No hagas preguntas trampa.
- Respondé ÚNICAMENTE con un array JSON válido, sin texto extra ni backticks.

Formato exacto:
[
  {{
    "question": "Texto de la pregunta",
    "options": ["Opción A", "Opción B", "Opción C", "Opción D"],
    "correct": 0
  }}
]

El campo "correct" es el índice (0-3) de la opción correcta."""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = message.content[0].text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        questions = json.loads(raw)
        return questions[:n]
    except Exception:
        return _fallback_questions(section_title)


def _fallback_questions(section_title: str) -> list[dict]:
    return [
        {
            "question": f"¿Sobre qué trata principalmente la sección '{section_title}'?",
            "options": [
                "Sobre el proceso de venta y sus etapas",
                "Sobre los valores y estándares de Vázquez Auto",
                "Sobre la gestión administrativa",
                "Sobre el contenido de esta sección del manual"
            ],
            "correct": 3
        }
    ]
