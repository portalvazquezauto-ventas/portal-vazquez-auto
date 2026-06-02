import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

PROFILES = {
    "precio": {
        "name": "El que pelea precio",
        "description": "Compara constantemente, presiona por descuento, dice que lo vio más barato.",
        "gender": "male",
        "system_prompt": """Sos un cliente que quiere comprar un auto en Vázquez Auto. Tu principal preocupación es el precio. Comparás constantemente con otras concesionarias. Decís frases como "en otro lado lo vi más barato", "¿no me podés hacer un mejor precio?", "es caro para lo que es". Sin embargo, si el vendedor logra mostrarte valor real (garantía, historial, servicio postventa), podés ablandarte. Respondé en primera persona, en español rioplatense, en 1-3 oraciones. No des información adicional a menos que el vendedor te la pregunte directamente. Nunca rompas el personaje."""
    },
    "indeciso": {
        "name": "El indeciso",
        "description": "Quiere pensarlo, consultar con alguien, nunca cierra solo.",
        "gender": "female",
        "system_prompt": """Sos un cliente interesado en comprar un auto en Vázquez Auto pero muy indeciso. Decís cosas como "lo tengo que pensar", "le tengo que consultar a mi señora/marido", "no sé si es el momento". Si el vendedor te hace preguntas precisas sobre tus necesidades y te da información concreta, podés avanzar. Respondé en primera persona, español rioplatense, 1-3 oraciones. No des información de más. Nunca rompas el personaje."""
    },
    "informado": {
        "name": "El sobre-informado",
        "description": "Investigó todo por internet, quiere validar lo que sabe.",
        "gender": "male",
        "system_prompt": """Sos un cliente que investigó mucho antes de ir a Vázquez Auto. Usaste ChatGPT y Google para comparar modelos, precios y financiación. Llegás con información (a veces correcta, a veces desactualizada) y querés que el vendedor valide lo que sabés. Si el vendedor te demuestra conocimiento superior y honestidad, confiás más. Respondé en primera persona, español rioplatense, 1-3 oraciones. Nunca rompas el personaje."""
    },
    "agro": {
        "name": "El cliente agro",
        "description": "Productor agropecuario, necesita vehículo para campo, prioriza durabilidad.",
        "gender": "male",
        "system_prompt": """Sos un productor agropecuario que busca una camioneta o auto robusto para uso mixto: campo y ciudad. Priorizás durabilidad, tracción, altura al piso, consumo y servicio postventa en zona rural. Preguntás sobre garantía en usados, qué pasa si se rompe lejos, si tienen repuestos. Sos desconfiado pero directo. Respondé en primera persona, español rioplatense, 1-3 oraciones. Nunca rompas el personaje."""
    },
    "credito": {
        "name": "El que necesita crédito",
        "description": "Necesita financiar, duda si califica, no entiende bien las cuotas.",
        "gender": "female",
        "system_prompt": """Sos un cliente que necesita financiamiento para comprar un auto en Vázquez Auto. Tenés dudas sobre si vas a calificar para el crédito, no entendés bien las cuotas, los gastos y las tasas. Si el vendedor te explica el proceso claramente y te transmite seguridad, avanzás. Respondé en primera persona, español rioplatense, 1-3 oraciones. Nunca rompas el personaje."""
    },
    "primera_compra": {
        "name": "Primera compra",
        "description": "Nunca compró un auto, necesita ser guiado en todo el proceso.",
        "gender": "male",
        "system_prompt": """Sos alguien que nunca compró un auto. No sabés bien la diferencia entre 0km stock, 0km a demanda y usado. No conocés los trámites y te preocupa no entender el proceso. Si el vendedor te acompaña con paciencia y claridad, generás confianza rápido. Respondé en primera persona, español rioplatense, 1-3 oraciones. Nunca rompas el personaje."""
    }
}

EVALUATOR_SYSTEM = """Sos un coach de ventas experto en el método de Vázquez Auto (Manual de Ventas 2026).
Evaluás la respuesta de un vendedor durante una simulación de venta.

El manual establece:
- El vendedor no es un cerrador, es un asesor comercial.
- Regla central: preferimos perder una venta antes que comprometer la confianza.
- Proceso de 8 etapas con gates de salida obligatorios.
- Ante presión de precio: retroceder en el proceso para reconstruir valor antes de negociar el número.
- Manejo de objeciones: "Me parece caro" → ofrecer simulación de cuota; "Lo voy a pensar" → preguntar qué genera dudas; "Lo vi más barato" → preguntar qué más valúa; "No sé si el financiamiento me sale" → hacer pre-consulta en 24hs.

Criterios de evaluación (0-100 cada uno):
- indagacion: ¿hizo preguntas que descubren la necesidad real del cliente? ¿Usó las preguntas clave?
- objeciones: ¿usó las respuestas del manual ante objeciones de precio, tiempo, crédito? ¿Construyó valor antes de tocar precio?
- consultivo: ¿habló como asesor, no como cerrador? ¿Siguió el proceso ordenadamente?

Respondé SOLO con un objeto JSON válido, sin texto extra, sin backticks:
{
  "feedback": "Una observación concreta y constructiva de 1-2 oraciones.",
  "indagacion": 0,
  "objeciones": 0,
  "consultivo": 0
}"""


def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY no configurada")
    return anthropic.Anthropic(api_key=api_key)


def get_opening_message(profile_type: str) -> str:
    """Genera el primer mensaje del cliente para iniciar la simulación."""
    profile = PROFILES.get(profile_type, PROFILES["precio"])
    openings = {
        "precio": "Hola, estoy buscando un auto pero quiero ver si me pueden mejorar el precio, porque en otro lugar lo vi más barato.",
        "indeciso": "Hola, estoy mirando autos... no sé bien qué quiero todavía, vine a ver qué tienen.",
        "informado": "Hola, investigué bastante y sé que este modelo tiene ciertas características. Quería que me confirmen algunas cosas.",
        "agro": "Buenas. Busco algo para el campo, necesito que sea resistente. ¿Qué tienen para mostrarme?",
        "credito": "Hola, me interesa un auto pero necesitaría financiarlo. No sé bien cómo funciona eso acá.",
        "primera_compra": "Hola, es la primera vez que vengo a una concesionaria... nunca compré un auto. No sé muy bien por dónde empezar.",
    }
    return openings.get(profile_type, "Hola, vengo a ver autos.")


def chat_with_client(profile_type: str, messages: list[dict], seller_message: str) -> str:
    """Envía un mensaje del vendedor al cliente IA y retorna la respuesta."""
    profile = PROFILES.get(profile_type, PROFILES["precio"])
    client = get_client()

    conversation = []
    for msg in messages:
        conversation.append({"role": msg["role"], "content": msg["content"]})
    conversation.append({"role": "user", "content": seller_message})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=profile["system_prompt"],
        messages=conversation
    )
    return response.content[0].text.strip()


def evaluate_seller_message(seller_message: str, client_message: str, profile_type: str) -> dict:
    """Evalúa una respuesta del vendedor y retorna scores + feedback."""
    client = get_client()

    prompt = f"""Perfil del cliente: {PROFILES[profile_type]['name']}
Mensaje del cliente: "{client_message}"
Respuesta del vendedor: "{seller_message}"

Evaluá la respuesta del vendedor según los criterios del manual."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            system=EVALUATOR_SYSTEM,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.content[0].text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except Exception:
        return {"feedback": "No se pudo evaluar.", "indagacion": 50, "objeciones": 50, "consultivo": 50}


def get_suggested_answer(client_message: str, profile_type: str) -> str:
    """Genera una respuesta sugerida basada en el manual (solo modo entrenamiento)."""
    client = get_client()

    profile_name = PROFILES[profile_type]["name"]
    prompt = f"""Sos un vendedor experto de Vázquez Auto que aplica el Manual de Ventas 2026.
El cliente es "{profile_name}" y dice: "{client_message}"

Escribí UNA respuesta ideal del vendedor (2-3 oraciones) que aplique el método consultivo del manual.
Respondé directamente con la respuesta del vendedor, sin explicaciones."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except Exception:
        return "Entiendo tu consulta. ¿Me contás un poco más sobre qué es lo más importante para vos en esta compra?"


def generate_final_feedback(session_data: dict) -> str:
    """Genera un reporte final narrativo de la sesión."""
    client = get_client()

    profile_name = PROFILES[session_data["profile_type"]]["name"]
    scores = {
        "indagacion": session_data.get("score_indagacion", 0),
        "objeciones": session_data.get("score_objeciones", 0),
        "consultivo": session_data.get("score_consultivo", 0),
        "global": session_data.get("score_global", 0),
    }

    prompt = f"""Generá un reporte de feedback final para un vendedor de Vázquez Auto después de una simulación.

Perfil trabajado: {profile_name}
Modalidad: {session_data.get("mode", "training")}
Score indagación: {scores["indagacion"]}/100
Score manejo de objeciones: {scores["objeciones"]}/100
Score consultivo: {scores["consultivo"]}/100
Score global: {scores["global"]}/100
Usó respuestas sugeridas: {"Sí" if session_data.get("used_hints") else "No"}

Escribí un párrafo de 3-4 oraciones con:
1. Lo que hizo bien
2. El área principal a mejorar
3. Un tip concreto del manual de Vázquez Auto para aplicar en la próxima sesión"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except Exception:
        return "Sesión completada. Revisá los scores individuales para identificar áreas de mejora."


def calculate_global_score(scores: list[dict]) -> dict:
    """Calcula promedios de scores de la sesión."""
    if not scores:
        return {"indagacion": 0, "objeciones": 0, "consultivo": 0, "global": 0}
    avg_ind = sum(s.get("indagacion", 0) for s in scores) // len(scores)
    avg_obj = sum(s.get("objeciones", 0) for s in scores) // len(scores)
    avg_con = sum(s.get("consultivo", 0) for s in scores) // len(scores)
    avg_global = (avg_ind + avg_obj + avg_con) // 3
    return {
        "indagacion": avg_ind,
        "objeciones": avg_obj,
        "consultivo": avg_con,
        "global": avg_global
    }
