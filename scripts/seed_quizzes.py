"""
Inserta quizzes de calidad para las 17 secciones del manual.
Correr: python scripts/seed_quizzes.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()
from supabase_client import get_admin_client

QUIZZES = {
    "1": [
        {"question": "¿Cuál es la Regla Central de Vázquez Auto?",
         "options": ["Cerrar la mayor cantidad de ventas posible", "Preferimos perder una venta antes que comprometer la confianza o el estándar de calidad", "El cliente siempre tiene razón", "El precio es lo más importante"],
         "correct": 1},
        {"question": "¿Cómo se define el rol del vendedor en Vázquez Auto?",
         "options": ["Un cerrador de ventas agresivo", "Un asesor comercial que ayuda al cliente a tomar la mejor decisión", "Un tomador de pedidos", "Un negociador de precios"],
         "correct": 1},
        {"question": "¿Cuál es el activo más importante de Vázquez Auto según el manual?",
         "options": ["El stock de autos", "La confianza", "El precio competitivo", "La ubicación del local"],
         "correct": 1},
    ],
    "2": [
        {"question": "¿Cuál es el propósito principal de Vázquez Auto?",
         "options": ["Vender la mayor cantidad de autos posible", "Ayudar a las personas a tomar la mejor decisión al comprar un vehículo", "Ofrecer los precios más bajos del mercado", "Ser la concesionaria más grande de la región"],
         "correct": 1},
        {"question": "¿Qué diferencia a Vázquez Auto de la competencia según el manual?",
         "options": ["Precios más bajos", "Mayor variedad de modelos", "Estándar de respuesta y seguimiento que genera clientes que vuelven y recomiendan", "Financiación exclusiva"],
         "correct": 2},
        {"question": "El vendedor ideal de Vázquez Auto hace seguimiento...",
         "options": ["Con insistencia hasta lograr la venta", "Con criterio, sin insistir", "Solo si el cliente lo solicita", "Una vez por semana sin excepción"],
         "correct": 1},
    ],
    "3": [
        {"question": "¿Qué hace el Director en la estructura de Vázquez Auto?",
         "options": ["Atiende clientes directamente", "Define estrategia, precios, condiciones y supervisa todo el proceso", "Solo administra el stock", "Gestiona las redes sociales"],
         "correct": 1},
        {"question": "¿Cuándo puede un vendedor cerrar una operación sin consultar al encargado?",
         "options": ["Siempre que el cliente esté listo", "Nunca — toda operación requiere validación del encargado o director", "Cuando el descuento sea menor al 5%", "Solo en ventas de contado"],
         "correct": 1},
        {"question": "¿Qué rol tiene el Encargado de Sucursal?",
         "options": ["Solo administra el local", "Supervisa vendedores, valida operaciones y garantiza estándares de atención", "Toma las decisiones de precios", "Se encarga solo de la parte legal"],
         "correct": 1},
    ],
    "4": [
        {"question": "¿Cuál NO es una competencia clave del vendedor de Vázquez Auto?",
         "options": ["Escucha activa", "Conocimiento del producto", "Presión para cerrar rápido", "Comunicación clara"],
         "correct": 2},
        {"question": "La competencia de 'indagación' consiste en...",
         "options": ["Investigar el historial del cliente", "Hacer las preguntas correctas para entender la necesidad real del cliente", "Buscar información del auto en internet", "Preguntar siempre por el presupuesto primero"],
         "correct": 1},
        {"question": "¿Qué debe hacer el vendedor antes de cotizar?",
         "options": ["Mostrar el auto más caro disponible", "Preguntar y entender la necesidad del cliente", "Dar el precio más bajo posible", "Hablar de las formas de financiación"],
         "correct": 1},
    ],
    "5.1": [
        {"question": "En el primer contacto, ¿cuál es el objetivo principal del vendedor?",
         "options": ["Cerrar la venta en esa misma llamada", "Calificar al cliente y entender en qué etapa de búsqueda está", "Enviar el catálogo de precios completo", "Pedir los datos personales del cliente"],
         "correct": 1},
        {"question": "¿Qué significa 'calificar' a un lead?",
         "options": ["Puntuar al cliente según su comportamiento", "Determinar si el cliente tiene intención real de compra y cuáles son sus necesidades", "Verificar que el cliente tenga dinero", "Clasificarlo por zona geográfica"],
         "correct": 1},
        {"question": "¿Cuál es el tiempo máximo de respuesta a un lead nuevo según el manual?",
         "options": ["24 horas", "48 horas", "Lo antes posible — idealmente en los primeros minutos", "Dentro del día hábil"],
         "correct": 2},
    ],
    "5.2": [
        {"question": "¿Qué debe hacer el vendedor ANTES de mostrar opciones de autos?",
         "options": ["Mostrar el auto más caro para anclar el precio", "Identificar las necesidades reales del cliente mediante preguntas", "Dar los precios de todos los modelos disponibles", "Hablar de las ventajas de Vázquez Auto"],
         "correct": 1},
        {"question": "¿Qué es la 'venta consultiva'?",
         "options": ["Consultar al encargado antes de cada venta", "Asesorar al cliente basándose en sus necesidades reales, no en el auto que queremos vender", "Ofrecer múltiples opciones siempre", "Vender usando folletos y catálogos"],
         "correct": 1},
        {"question": "Cuando el cliente dice 'estoy mirando opciones', el vendedor debe...",
         "options": ["Bajar el precio inmediatamente", "Hacer preguntas para entender qué está comparando y qué valoriza", "Insistir en que Vázquez Auto es la mejor opción", "Darle tiempo y no contactarlo más"],
         "correct": 1},
    ],
    "5.3": [
        {"question": "Una cotización profesional en Vázquez Auto debe incluir...",
         "options": ["Solo el precio final", "Precio, condiciones, documentación incluida y próximos pasos claros", "El precio y el número de cuotas", "Solo la información que el cliente pide explícitamente"],
         "correct": 1},
        {"question": "¿Cuándo se debe enviar una cotización?",
         "options": ["Siempre en el primer contacto para no perder al cliente", "Después de entender las necesidades del cliente y presentar una opción relevante", "Solo por correo electrónico", "Cuando el cliente lo pide explícitamente"],
         "correct": 1},
        {"question": "¿Qué se debe evitar en una cotización?",
         "options": ["Detallar las condiciones de pago", "Dar precios sin condiciones claras o prometer algo que no se puede cumplir", "Incluir información del auto", "Mencionar la garantía"],
         "correct": 1},
    ],
    "5.4": [
        {"question": "Cuando el cliente pide un descuento, el vendedor debe primero...",
         "options": ["Dar el descuento máximo posible para no perder la venta", "Construir valor antes de negociar precio", "Decir que no hay descuentos", "Consultar al encargado inmediatamente"],
         "correct": 1},
        {"question": "¿Qué es el seguimiento consultivo?",
         "options": ["Llamar al cliente todos los días hasta que compre", "Hacer seguimiento con valor agregado — no solo 'ya se decidió?'", "Enviar el mismo presupuesto varias veces", "Esperar que el cliente llame"],
         "correct": 1},
        {"question": "¿Cuándo se considera que una objeción fue manejada correctamente?",
         "options": ["Cuando el cliente deja de hablar de eso", "Cuando se responde con información real y el cliente siente que su preocupación fue escuchada", "Cuando se baja el precio lo suficiente", "Cuando el encargado interviene"],
         "correct": 1},
    ],
    "5.5": [
        {"question": "¿Qué es el SDR (Seña De Reserva)?",
         "options": ["Un contrato de compraventa definitivo", "Un pago inicial que reserva el auto mientras se gestiona el resto de la operación", "Un descuento por pago adelantado", "Una garantía de entrega"],
         "correct": 1},
        {"question": "¿Qué debe quedar documentado al momento de la seña?",
         "options": ["Solo el monto pagado", "El auto, precio, condiciones, forma de pago y fecha estimada de entrega", "El nombre del vendedor y la fecha", "Los datos del comprador únicamente"],
         "correct": 1},
        {"question": "Si el cliente quiere pagar la seña pero las condiciones no están cerradas, el vendedor debe...",
         "options": ["Aceptar la seña para no perder al cliente", "Consultar al encargado antes de recibir cualquier dinero", "Pedirle que vuelva cuando esté todo listo", "Hacer el recibo de forma provisoria"],
         "correct": 1},
    ],
    "5.6": [
        {"question": "¿Qué incluye la gestión de cancelación total de una operación?",
         "options": ["Solo devolver el dinero pagado", "Documentar el motivo, gestionar la devolución según contrato y registrar en el sistema", "Hablar con el cliente para convencerlo de no cancelar", "Transferir el caso al director directamente"],
         "correct": 1},
        {"question": "¿Cuándo se puede cancelar una operación sin penalidad para el cliente?",
         "options": ["Nunca — toda cancelación tiene penalidad", "Según las condiciones pactadas en el contrato o seña", "Siempre que el cliente lo solicite dentro de las 24 horas", "Solo si el auto no fue entregado"],
         "correct": 1},
        {"question": "¿Qué debe hacer el vendedor ante una solicitud de cancelación?",
         "options": ["Intentar convencer al cliente de no cancelar con descuentos", "Escuchar el motivo, informar las condiciones del contrato y derivar al encargado", "Procesar la cancelación directamente", "Decirle al cliente que hable con el encargado sin más información"],
         "correct": 1},
    ],
    "5.7": [
        {"question": "¿Qué debe estar garantizado al momento de la entrega del vehículo?",
         "options": ["Que el auto esté limpio y tanque lleno", "Que la documentación esté completa, la transferencia gestionada y el auto sin deuda", "Que el vendedor esté presente", "Que el cliente firme el contrato de servicio"],
         "correct": 1},
        {"question": "La entrega del vehículo es importante porque...",
         "options": ["Es el momento de cobrar el saldo pendiente", "Es la última impresión que el cliente tiene del negocio y define si recomienda Vázquez Auto", "Es cuando se hace la transferencia del dominio", "Es cuando el cliente puede pedir cambios de último momento"],
         "correct": 1},
        {"question": "¿Qué documentación debe estar lista en la entrega?",
         "options": ["Solo la factura", "Título, transferencia iniciada, libre de multas y toda documentación acordada", "El manual del fabricante y la garantía", "Solo lo que el cliente solicita"],
         "correct": 1},
    ],
    "5.8": [
        {"question": "¿Qué es la 'postventa cumplida'?",
         "options": ["Llamar al cliente una vez después de la venta", "Hacer seguimiento real después de la entrega para asegurarse de que el cliente esté conforme", "Enviar una encuesta de satisfacción por WhatsApp", "Ofrecerle un descuento en la próxima compra"],
         "correct": 1},
        {"question": "¿Por qué es importante el seguimiento postventa?",
         "options": ["Para generar una venta adicional inmediata", "Para detectar problemas a tiempo, generar confianza y obtener recomendaciones", "Para cumplir con el CRM", "Para evitar reclamos formales"],
         "correct": 1},
        {"question": "¿Cuándo debe hacerse el primer contacto postventa?",
         "options": ["A los 30 días de la entrega", "Dentro de los primeros días posteriores a la entrega", "Solo si el cliente llama con un problema", "A los 6 meses para ofrecerle otro auto"],
         "correct": 1},
    ],
    "6": [
        {"question": "¿Para qué sirve el CRM en Vázquez Auto?",
         "options": ["Solo para guardar los datos de contacto", "Para registrar y hacer seguimiento de todos los leads y operaciones de forma ordenada", "Para calcular comisiones", "Para comunicarse internamente entre vendedores"],
         "correct": 1},
        {"question": "¿Qué debe registrarse en el CRM después de cada interacción con un lead?",
         "options": ["Solo el nombre y teléfono", "El estado de la conversación, el auto de interés y el próximo paso pactado", "La opinión personal del vendedor sobre el cliente", "El precio ofrecido únicamente"],
         "correct": 1},
        {"question": "Un lead 'frío' en el CRM es...",
         "options": ["Un cliente que nunca va a comprar", "Un contacto que no ha respondido en varios días o no tiene intención de compra clara", "Un cliente nuevo que acaba de consultar", "Un cliente que compró hace más de un año"],
         "correct": 1},
    ],
    "7": [
        {"question": "¿Cuál es la función principal de los indicadores en la rutina del encargado?",
         "options": ["Controlar que los vendedores trabajen", "Identificar oportunidades de mejora y tomar decisiones basadas en datos reales", "Calcular comisiones", "Reportar al director semanalmente"],
         "correct": 1},
        {"question": "¿Con qué frecuencia debe el encargado revisar los indicadores de su equipo?",
         "options": ["Solo a fin de mes", "Diaria o semanalmente según el indicador", "Cuando el director lo solicita", "Solo cuando hay un problema"],
         "correct": 1},
        {"question": "¿Qué debe hacer el encargado cuando un vendedor tiene indicadores bajos?",
         "options": ["Sancionarlo directamente", "Analizar la causa raíz y dar feedback constructivo con un plan de mejora", "Asignarle menos leads", "Reportarlo al director para que intervenga"],
         "correct": 1},
    ],
    "8": [
        {"question": "¿Qué son las 'Condiciones Administrativas' en el manual?",
         "options": ["Los horarios de trabajo del equipo", "Los procesos y requisitos para que una operación sea válida y esté bien documentada", "Las políticas de vacaciones", "Los criterios de contratación de vendedores"],
         "correct": 1},
        {"question": "¿Qué debe tener toda operación para ser válida en Vázquez Auto?",
         "options": ["Solo la firma del cliente", "Documentación completa, validación del encargado y registro en el sistema", "El visto bueno del vendedor únicamente", "Solo el comprobante de pago"],
         "correct": 1},
        {"question": "¿Quién puede autorizar excepciones a las condiciones administrativas estándar?",
         "options": ["Cualquier vendedor con más de 6 meses de antigüedad", "Solo el encargado o el director", "El cliente si lo solicita formalmente", "Nadie — no hay excepciones"],
         "correct": 1},
    ],
    "9": [
        {"question": "¿Cuál es el propósito de los 'Límites y Reglas No Negociables'?",
         "options": ["Limitar la creatividad del vendedor", "Proteger la integridad de la operación, al cliente y la reputación de Vázquez Auto", "Cumplir con requisitos legales únicamente", "Facilitar el trabajo administrativo"],
         "correct": 1},
        {"question": "Si un cliente presiona para saltear un requisito administrativo, el vendedor debe...",
         "options": ["Ceder si la venta es importante", "Explicar que no puede hacerlo y derivar al encargado si el cliente insiste", "Ignorar la presión y seguir adelante igual", "Decirle que consulte con el encargado sin más explicación"],
         "correct": 1},
        {"question": "¿Qué ejemplo de límite no negociable menciona el manual?",
         "options": ["No se puede vender más de 2 autos por día", "No se promete lo que no se puede cumplir ni se omite información relevante al cliente", "No se acepta efectivo en ninguna operación", "No se entregan autos los fines de semana"],
         "correct": 1},
    ],
    "10": [
        {"question": "¿Qué contiene la sección de 'Anexos y Políticas'?",
         "options": ["Información extra que no cabe en otras secciones", "Documentos de referencia, políticas específicas y procedimientos complementarios al manual", "Solo las políticas de devolución", "Los contratos tipo para imprimir"],
         "correct": 1},
        {"question": "¿Para qué sirven los anexos del manual?",
         "options": ["Son solo para el director", "Proveen información detallada de procedimientos específicos que complementan el contenido principal", "Son opcionales y no es necesario leerlos", "Solo aplican en casos de reclamos"],
         "correct": 1},
        {"question": "¿Cuándo debe consultar el vendedor los anexos?",
         "options": ["Nunca, están solo para el encargado", "Cuando necesita profundizar en un procedimiento específico o resolver una situación particular", "Solo en la primera semana de trabajo", "Una vez por mes como repaso"],
         "correct": 1},
    ],
}

def main():
    client = get_admin_client()
    sections = client.table("manual_sections").select("id,section_number,title").order("id").execute().data

    print(f"Actualizando quizzes para {len(sections)} secciones...")
    for s in sections:
        num = str(s["section_number"])
        questions = QUIZZES.get(num)
        if questions:
            client.table("manual_sections").update({"quiz_questions": questions}).eq("id", s["id"]).execute()
            print(f"  OK [{num}] {s['title']} — {len(questions)} preguntas")
        else:
            print(f"  SIN QUIZ [{num}] {s['title']}")

    # Limpiar historial de lecturas para que todos empiecen de cero
    client.table("manual_reads").delete().neq("id", 0).execute()
    print("\nHistorial de lecturas limpiado (todos empiezan de cero).")
    print("Listo.")

if __name__ == "__main__":
    main()
