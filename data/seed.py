"""
Script de seed para Portal Vázquez Auto.
Ejecutar una sola vez: python data/seed.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from supabase_client import get_admin_client

USERS = [
    {"full_name": "Esteban Vázquez", "email": "esteban@vazquezauto.com.ar", "password": "Direccion2026!", "role": "director"},
    {"full_name": "Victor Oller", "email": "voller@vazquezauto.com.ar", "password": "Vazquez2026!", "role": "manager"},
    {"full_name": "Leonardo Lopez", "email": "llopez@vazquezauto.com.ar", "password": "Vazquez2026!", "role": "manager"},
    {"full_name": "Matias Ribotta", "email": "mribotta@vazquezauto.com.ar", "password": "Vendedor2026!", "role": "seller"},
    {"full_name": "Lucas Lucero", "email": "llucero@vazquezauto.com.ar", "password": "Vendedor2026!", "role": "seller"},
    {"full_name": "Manuel Vazquez", "email": "mvazquez@vazquezauto.com.ar", "password": "Vendedor2026!", "role": "seller"},
    {"full_name": "Raul Pozzi", "email": "rpozzi@vazquezauto.com.ar", "password": "Vendedor2026!", "role": "seller"},
    {"full_name": "Nicolas Barrionuevo", "email": "nbarrionuevo@vazquezauto.com.ar", "password": "Vendedor2026!", "role": "seller"},
]

MANUAL_SECTIONS = [
    {
        "section_number": "1",
        "title": "Introducción y Regla Central",
        "content": """# Introducción — Manual de Ventas Vázquez Auto 2026

Este manual define el estándar de actuación del equipo comercial de Vázquez Auto. No es una guía de técnicas de cierre: es el modelo de trabajo de un equipo que vende con criterio, con respeto y con consistencia.

## Regla Central

**"Preferimos perder una venta antes que comprometer la confianza o el estándar de calidad de Vázquez Auto."**

Esta regla no es un slogan. Es el criterio de decisión ante cualquier situación donde el vendedor sienta presión para hacer algo que no se alinea con los valores del equipo: prometer algo que no puede cumplir, omitir información relevante, o ceder ante una demanda que compromete la integridad de la operación.

El vendedor de Vázquez Auto no es un cerrador. Es un asesor comercial. Su rol es ayudar al cliente a tomar la mejor decisión para él, dentro de las condiciones que Vázquez Auto puede ofrecer con honestidad.

Cuando el vendedor actúa desde ese lugar, los resultados llegan. Cuando actúa desde la desesperación por cerrar, se generan problemas: promesas incumplidas, clientes insatisfechos, y reputación dañada.

**La confianza es el activo más importante de Vázquez Auto. Cada vendedor es responsable de cuidarla.**"""
    },
    {
        "section_number": "2",
        "title": "Propósito y Objetivos",
        "content": """# Propósito y Objetivos

## 2.1 Propósito

Vázquez Auto existe para ayudar a las personas a tomar la mejor decisión al comprar un vehículo, ofreciendo transparencia, respaldo documental y acompañamiento real en cada etapa del proceso.

No vendemos autos. Acompañamos decisiones de compra importantes en la vida de las personas.

## 2.2 Objetivos Generales

- Brindar una experiencia de compra ordenada, honesta y sin sorpresas.
- Garantizar que cada unidad entregada esté documentada, transferida y libre de deuda.
- Mantener un estándar de respuesta y seguimiento que diferencie a Vázquez Auto de la competencia.
- Generar clientes que vuelvan y recomienden, no clientes que compran una sola vez.

## 2.3 El Vendedor Vázquez Auto

El vendedor ideal de Vázquez Auto:
- Escucha antes de hablar.
- Pregunta antes de cotizar.
- Construye valor antes de negociar precio.
- Conoce el proceso y lo explica con claridad.
- Nunca promete lo que no puede cumplir.
- Hace seguimiento con criterio, no con insistencia.
- Cuida la reputación del equipo en cada interacción."""
    },
    {
        "section_number": "3",
        "title": "Estructura del Área y Roles",
        "content": """# Estructura del Área de Ventas

## 3.1 Estructura

El área comercial de Vázquez Auto opera con la siguiente estructura:

**Dirección** → **Encargados de Sucursal** → **Vendedores**

La Dirección define los parámetros de negociación, los estándares de calidad y las políticas comerciales. Los Encargados supervisan la operación diaria, forman al equipo y garantizan el cumplimiento de los procesos. Los Vendedores ejecutan el proceso de venta en contacto directo con el cliente.

## 3.2 Descripción de Roles

| Rol | Responsabilidades clave |
|-----|------------------------|
| **Director** | Estrategia comercial, parámetros de negociación, aprobación de excepciones |
| **Encargado de Sucursal** | Supervisión del equipo, seguimiento de métricas, formación, gestión de casos complejos |
| **Vendedor** | Atención al cliente, proceso de venta de 8 etapas, gestión en CRM, seguimiento de leads |

### El Encargado no cierra ventas por el vendedor

El encargado está para orientar, no para reemplazar. Si un vendedor escala una situación, el encargado ayuda a definir la estrategia, pero el vendedor conduce la relación con el cliente.

### El Vendedor es el dueño del lead

Desde el primer contacto hasta la postventa, el vendedor es responsable de esa relación. No existe "esto es responsabilidad de otro" dentro del proceso de venta."""
    },
    {
        "section_number": "4",
        "title": "Competencias del Vendedor",
        "content": """# Competencias del Vendedor Vázquez Auto

## 4.1 Competencias Técnicas

**Conocimiento del producto:**
- Dominar las diferencias entre 0km stock, 0km a demanda y usados selecto.
- Conocer los modelos disponibles, sus características y diferenciales clave.
- Entender las condiciones de garantía de usados selecto (3 meses motor/caja).

**Conocimiento del proceso:**
- Conocer las 8 etapas del proceso de venta y los gates de salida de cada una.
- Manejar el CRM con disciplina: cada contacto registrado, cada estado actualizado.
- Saber cómo funciona la pre-evaluación crediticia y qué información necesita.

**Conocimiento administrativo:**
- Entender cómo funciona la seña, el SDR, y las formas de pago aceptadas.
- Saber qué documentos necesita el cliente según el tipo de operación.

## 4.2 Competencias Blandas

**Escucha activa:** El vendedor que habla más que el cliente no está vendiendo. Está presentando.

**Gestión de objeciones:** Las objeciones son señales de interés, no rechazos. El vendedor las recibe, las valida y las trabaja con información.

**Tolerancia a la frustración:** No todos los leads convierten. El vendedor que personaliza el rechazo pierde energía y perspectiva.

**Comunicación escrita:** Los mensajes de WhatsApp y los mails reflejan la imagen de Vázquez Auto. Deben ser claros, correctos y profesionales.

**Disciplina de proceso:** El vendedor que saltea etapas o no registra en el CRM crea problemas downstream. La disciplina no es burocracia: es respeto por el sistema que hace funcionar al equipo."""
    },
    {
        "section_number": "5.1",
        "title": "Primer Contacto y Calificación",
        "content": """# Etapa 1: Primer Contacto y Calificación

## SLA de Contacto

**Todo lead nuevo debe ser contactado dentro de los 30 minutos de recibido**, independientemente del canal de origen (web, Instagram, WhatsApp, llamada, visita presencial).

Si el lead llega fuera del horario comercial, debe ser contactado a primera hora del día siguiente.

## Objetivo de esta etapa

Calificar al lead: entender si tiene intención real de compra, qué está buscando, y si Vázquez Auto puede satisfacer esa necesidad.

## Preguntas de calificación inicial

1. ¿Qué tipo de vehículo estás buscando? (0km, usado, segmento)
2. ¿Para qué uso principalmente? (ciudad, campo, mixto, familiar)
3. ¿Tenés algo para entregar en parte de pago?
4. ¿Cómo pensás financiar? (contado, financiación, combinado)
5. ¿Cuándo estás pensando en concretar?

## Gate de salida

Para avanzar a la siguiente etapa, el vendedor debe tener claro:
- Qué busca el cliente
- Si tiene urgencia o está en etapa de exploración
- Si hay capacidad de pago (contado, crédito, parte de pago)

Si el cliente no puede/quiere dar esta información, se agenda un contacto posterior y se registra en el CRM como "en calificación"."""
    },
    {
        "section_number": "5.2",
        "title": "Asesoramiento e Identificación de Necesidades",
        "content": """# Etapa 2: Asesoramiento e Identificación de Necesidades

## El principio de esta etapa

Antes de mostrar un precio, hay que entender qué necesita el cliente. El vendedor que cotiza sin preguntar está tirando números al aire.

## Preguntas clave de asesoramiento

**Para entender el uso:**
- ¿Cuántos km hacés por mes aproximadamente?
- ¿Usás el auto principalmente en ciudad o también en ruta/campo?
- ¿Cuántas personas viajan normalmente con vos?
- ¿Necesitás baúl grande, tracción 4x4, altura al piso?

**Para entender la decisión:**
- ¿Ya viste algo que te gustó, o estás en etapa de exploración?
- ¿Qué es lo más importante para vos en esta compra? (precio, garantía, marca, financiación)
- ¿Estás comparando con otros lugares? ¿Qué tenían?

## Orden de la oferta

1. Primero escuchás.
2. Después mostrás opciones que se ajusten a lo que te dijo.
3. Nunca mostrés todo el stock. Mostrá lo que es relevante para ese cliente.

## Diferenciales a comunicar siempre

Para usados selecto:
- Garantía 3 meses motor/caja
- Transferido + libre de deuda al momento de la entrega
- Historia clínica del vehículo disponible
- Fotos y video completo antes de la operación
- Posibilidad de prueba de manejo"""
    },
    {
        "section_number": "5.3",
        "title": "Cotización Profesional",
        "content": """# Etapa 3: Cotización Profesional

## Plantilla obligatoria

Toda cotización formal enviada al cliente debe incluir:
- Descripción completa del vehículo (marca, modelo, año, versión, km)
- Precio de lista
- Condiciones de financiación (si aplica): cuotas, tasa, requisitos
- Diferenciales incluidos (garantía, documentación, etc.)
- Validez de la cotización (máx. 48hs)
- Datos de contacto del vendedor

## SLA de cotización

**La cotización debe ser enviada dentro de las 2 horas de solicitada** por el cliente.

Si el vendedor no tiene toda la información para cotizar (ej: necesita confirmar disponibilidad, precio de financiación), le avisa al cliente y da un tiempo estimado.

## Lo que no se cotiza

- Precios sin confirmar disponibilidad
- Condiciones de financiación sin pre-evaluación
- Precios "de palabra" que después no se pueden sostener

## Regla: una cotización es un compromiso

Si cotizaste un precio, ese precio tiene que poder mantenerse. Si hay un error, corrígelo antes de que el cliente lo tome como definitivo. No después."""
    },
    {
        "section_number": "5.4",
        "title": "Negociación y Seguimiento Consultivo",
        "content": """# Etapa 4: Negociación y Seguimiento Consultivo

## Reglas de negociación

1. **Construí valor antes de hablar de precio.** Si el cliente pregunta el precio antes de que hayas explicado qué incluye la propuesta, respondé el precio pero volvé a construir valor.

2. **Ante presión de precio: retrocedé en el proceso.** Si el cliente dice "está caro", no reaccionés bajando el precio. Preguntá qué es lo que más valúa, y trabajá desde ahí.

3. **Nunca rompas el piso de precio sin autorización.** Si necesitás hacer una excepción, escalá al encargado.

## Cadencia de seguimiento

| Momento | Acción |
|---------|--------|
| D0 | Envío de cotización + confirmación de recepción |
| D1 | Seguimiento si no hubo respuesta |
| D3 | Segundo seguimiento si sigue sin respuesta |
| D7 | Cierre de etapa: marcar como "seguimiento extendido" o "perdido" |

## Manejo de objeciones principales

**"Me parece caro"**
→ "Este modelo tiene condiciones especiales. Puedo hacerte una simulación de cuota para ver cómo queda con financiación."

**"Lo voy a pensar"**
→ "Entiendo. ¿Qué es lo que te genera dudas? Así te ayudo a resolverlas antes de que cambie la disponibilidad."

**"Lo vi más barato en otro lado"**
→ "Te lo creo. Además del precio, ¿qué más estás valuando? Puedo mostrarte qué incluye nuestra propuesta que tal vez no esté en la otra."

**"No sé si el financiamiento me sale"**
→ "Te hago una pre-consulta ahora. En menos de 24 hs te confirmo si califica y con qué condiciones."

## El seguimiento no es insistencia

Seguimiento con criterio = recordar que existís con algo de valor.
Insistencia = mandar "¿qué decidiste?" tres veces por semana.

Si el cliente no responde después de D3, cambiá el enfoque: mandá algo de valor (un modelo nuevo que llegó, una condición que mejoró), no una pregunta de cierre."""
    },
    {
        "section_number": "5.5",
        "title": "Cierre de Venta — SDR + Seña",
        "content": """# Etapa 5: Cierre de Venta

## Confirmaciones previas al cierre

Antes de pedir la seña, el vendedor debe confirmar:
1. El cliente vio el vehículo (presencialmente o con fotos/video completo)
2. El cliente conoce el precio final y las condiciones
3. El cliente sabe qué documentación necesita para la operación
4. Si hay financiación: el cliente tiene pre-aprobación o sabe que está en proceso

## El SDR (Señal De Reserva)

El SDR es el primer paso formal de la operación. Implica:
- Reserva del vehículo a nombre del comprador
- Compromiso de precio por parte de Vázquez Auto
- Inicio del proceso de documentación

**El SDR no es reembolsable salvo en casos específicos definidos por la Dirección.**

## SLA de cierre

Una vez que el cliente confirma que quiere avanzar, la seña debe quedar comprometida dentro de las 24 horas.

Si el cliente necesita más tiempo, se acuerda una fecha concreta y se registra en el CRM."""
    },
    {
        "section_number": "5.6",
        "title": "Gestión y Cancelación Total",
        "content": """# Etapa 6: Gestión y Cancelación Total

## Gates obligatorios antes de la entrega

1. **Documentación completa:** DNI, comprobante de domicilio, documentación del vehículo en regla.
2. **Libre de deuda confirmado:** El vehículo no puede entregarse con deudas pendientes.
3. **Transferencia iniciada o completada:** Según el tipo de operación.
4. **Pago total confirmado:** Ya sea contado o primera cuota de financiación.

## Cancelaciones

Si el cliente cancela después de firmado el SDR, se aplica la política de cancelación vigente (definida por la Dirección). El vendedor nunca ofrece excepciones a esta política sin autorización.

Si Vázquez Auto cancela la operación (ej: el vehículo tiene un problema que no puede resolverse), se devuelve el 100% de lo abonado sin demora."""
    },
    {
        "section_number": "5.7",
        "title": "Entrega de la Unidad",
        "content": """# Etapa 7: Entrega de la Unidad

## Protocolo de entrega

La entrega es el momento más importante de la experiencia de compra. El cliente debe irse sintiéndose acompañado y seguro.

**Checklist de entrega:**
- [ ] Vehículo limpio y en condiciones
- [ ] Documentación completa entregada al cliente (tarjeta verde o cédula azul, manual del vehículo)
- [ ] Explicación de la garantía (condiciones, qué cubre, qué no, cómo acceder)
- [ ] Revisión de funcionamiento básico con el cliente presente (luces, A/C, vidrios, llave)
- [ ] Datos de contacto del vendedor entregados para postventa
- [ ] Foto del cliente con el vehículo (con permiso)

## Lo que no se hace en la entrega

- No se entrega un vehículo con deudas pendientes ni problemas sin resolver.
- No se apura la entrega si el cliente tiene dudas.
- No se da información incorrecta sobre la garantía para no generar expectativas falsas."""
    },
    {
        "section_number": "5.8",
        "title": "Postventa Cumplida",
        "content": """# Etapa 8: Postventa Cumplida

## Seguimiento postventa

**D+2 de la entrega:** El vendedor contacta al cliente para verificar que todo esté bien con el vehículo y que no tenga preguntas pendientes.

**D+7 de la entrega:** Segundo contacto para confirmar satisfacción. Si el cliente tiene algún inconveniente, el vendedor lo escala al encargado inmediatamente.

## Por qué importa el postventa

Un cliente que se siente acompañado después de la compra:
- Vuelve cuando necesita cambiar el auto.
- Recomienda Vázquez Auto a conocidos.
- Deja reseñas positivas.
- No genera problemas ni reclamos por malentendidos que podrían haberse resuelto antes.

El postventa no es un trámite. Es la diferencia entre un cliente de una sola vez y un cliente de por vida."""
    },
    {
        "section_number": "6",
        "title": "Gestión de Leads en CRM",
        "content": """# Gestión de Leads en CRM

## La Regla de Oro del CRM

**Si no está en el CRM, no existe.**

Cada lead, cada interacción, cada cambio de estado debe quedar registrado. El CRM es la memoria del equipo. Un lead sin registro es una venta perdida sin análisis posible.

## Pipeline de 7 etapas

1. **Nuevo** — Lead recibido, no contactado aún.
2. **Contactado** — Primer contacto realizado.
3. **Calificado** — Se conoce la necesidad y la capacidad de compra.
4. **Cotizado** — Se envió propuesta formal.
5. **Negociando** — El cliente está evaluando la propuesta.
6. **Señado** — SDR firmado y seña entregada.
7. **Entregado** — Operación completada.

## Clasificación de leads

- **Caliente:** Tiene urgencia real, presupuesto definido, intención clara. Seguimiento diario.
- **Tibio:** Interesado pero sin urgencia o con dudas. Seguimiento cada 2-3 días.
- **Frío:** Sin urgencia, sin presupuesto claro, o sin respuesta repetida. Seguimiento semanal.

## Motivos de cierre (cuando se pierde un lead)

Registrar siempre uno de estos motivos:
- Compró en otro lugar
- Precio no competitivo
- No calificó para financiación
- Sin respuesta (lead fantasma)
- Postergó la compra indefinidamente
- Cambió de necesidad

## Buenas prácticas

- Actualizá el estado del lead el mismo día que cambia.
- No dejés leads en "Cotizado" más de 7 días sin actualizar.
- Usá las notas del CRM para registrar objeciones y acuerdos."""
    },
    {
        "section_number": "7",
        "title": "Indicadores y Rutina del Encargado",
        "content": """# Indicadores Clave y Rutina del Encargado

## Indicadores semanales del equipo

| Indicador | Frecuencia | Referencia |
|-----------|-----------|-----------|
| Leads nuevos | Semanal | — |
| Leads contactados en <30min | Semanal | >90% |
| Tasa de cotización | Semanal | >60% de calificados |
| Tasa de cierre | Mensual | Según target |
| Tiempo promedio D0-D7 | Semanal | <7 días |
| Leads perdidos con motivo registrado | Semanal | 100% |

## Rutina del Encargado

**Diaria:**
- Revisar leads nuevos sin contactar.
- Verificar leads en "Cotizado" sin actividad en las últimas 48hs.
- Disponible para escalar situaciones del equipo.

**Semanal:**
- Reunión de pipeline con el equipo (30 min máximo).
- Revisión de leads perdidos: ¿qué se podría haber hecho diferente?
- Feedback individual a vendedores con bajo rendimiento.

**Mensual:**
- Reporte a la Dirección: tasa de cierre, ticket promedio, leads por fuente.
- Evaluación de formación: ¿qué necesita el equipo para mejorar?"""
    },
    {
        "section_number": "8",
        "title": "Condiciones Administrativas",
        "content": """# Condiciones Administrativas

## SDR — Señal De Reserva

El SDR reserva el vehículo durante un plazo definido (generalmente 72hs hábiles para gestionar financiación o documentación).

El monto del SDR se descuenta del precio total de la operación.

**El SDR no es reembolsable** salvo en los casos expresamente definidos por la Dirección: falla mecánica grave no declarada, documentación en irregular estado, o cancelación por parte de Vázquez Auto.

## Formas de pago aceptadas

- Transferencia bancaria
- Efectivo (con recibo oficial)
- Cheque (previa aprobación del encargado)
- Financiación a través de entidades bancarias o financieras habilitadas

## Aclaraciones al cliente

Antes de cerrar, el vendedor debe asegurarse de que el cliente entiende:
1. Que el precio cotizado incluye / no incluye (especificar) ciertos ítems.
2. Las condiciones de la garantía de usados selecto.
3. Los plazos estimados de transferencia y documentación.
4. Qué pasa si hay un problema con la unidad después de la entrega.

## WhatsApp como canal de venta

El WhatsApp es un canal válido y frecuente de comunicación con clientes. Aplican las mismas reglas de profesionalismo que cualquier otro canal:
- Respuesta dentro de los SLA definidos.
- Sin abreviaturas o lenguaje informal que comprometan la imagen.
- Sin promesas no autorizadas."""
    },
    {
        "section_number": "9",
        "title": "Límites y Reglas No Negociables",
        "content": """# Límites y Reglas No Negociables

Estas reglas no tienen excepciones. No importa la presión del cliente, del entorno o del momento.

## Lo que nunca se hace

1. **No se entrega un vehículo con deuda pendiente.** Nunca. Sin importar la urgencia del cliente o el acuerdo verbal previo.

2. **No se prometen condiciones no autorizadas.** Si el encargado o la Dirección no aprobó una condición especial (precio, financiación, plazo), no se promete.

3. **No se omite información relevante al cliente.** Si el vehículo tiene un historial de accidente, una reparación significativa o cualquier condición que el comprador razonablemente querría saber, se informa.

4. **No se presiona al cliente para cerrar.** Se construye valor, se hace seguimiento, se resuelven objeciones. No se presiona.

5. **No se trabaja con un lead que no está en el CRM.** Toda gestión empieza con el registro.

6. **No se da precio sin disponibilidad confirmada.** Confirmar antes de cotizar.

## Por qué estas reglas son innegociables

Cada vez que se rompe una de estas reglas, se daña la reputación de Vázquez Auto. Y la reputación es lo que hace que los clientes elijan Vázquez Auto sobre otras opciones.

Una venta ganada al costo de romper estas reglas vale mucho menos que lo que cuesta recuperar la confianza perdida."""
    },
    {
        "section_number": "10",
        "title": "Anexos y Políticas",
        "content": """# Anexos y Políticas

## Política de garantía — Usados Selecto

Los vehículos usados selecto de Vázquez Auto incluyen:
- **Garantía de 3 meses** en motor y caja de velocidades.
- El vehículo se entrega transferido y libre de deuda.
- Historia clínica disponible para el comprador.
- Fotos y video completo del vehículo antes de la operación.

La garantía no cubre: consumibles (neumáticos, frenos, batería), roturas por uso inadecuado, o daños causados por el propietario después de la entrega.

## Política de cancelación

Aplica la política vigente definida por la Dirección en el momento de la operación. El vendedor no puede modificar ni interpretar esta política sin autorización expresa.

## Canales de escalada

Ante una situación que supera la autoridad del vendedor:
1. El vendedor comunica al cliente que va a consultar con su encargado.
2. Escala al encargado con el contexto completo.
3. El encargado define la respuesta o escala a Dirección si es necesario.
4. El vendedor vuelve al cliente con la respuesta acordada.

**El vendedor nunca dice "no sé" sin acompañarlo de "pero lo averiguo y te confirmo".**

## Contacto y referencias

Para consultas sobre políticas, condiciones especiales o situaciones no contempladas en este manual, el canal es el encargado de sucursal. Para situaciones que requieren decisión de Dirección, el encargado es el intermediario."""
    },
]

QUESTION_GUIDE = [
    # Perfil: precio
    {"profile_type": "precio", "category": "indagacion", "question": "¿Además del precio, qué más estás valuando?", "expected_answer": "Te lo creo. Además del precio, ¿qué más estás valuando? Puedo mostrarte qué incluye nuestra propuesta que tal vez no esté en la otra.", "manual_reference": "5.4", "order_index": 1},
    {"profile_type": "precio", "category": "objecion", "question": "Lo vi más barato en otro lado", "expected_answer": "Te lo creo. Además del precio, ¿qué más estás valuando? Puedo mostrarte qué incluye nuestra propuesta que tal vez no esté en la otra.", "manual_reference": "5.4", "order_index": 2},
    {"profile_type": "precio", "category": "construccion", "question": "¿Qué incluye un usado selecto de Vázquez?", "expected_answer": "Garantía 3 meses motor/caja, transferido + libre deuda, historia clínica, fotos/video completo, y posibilidad de prueba de manejo.", "manual_reference": "5.2", "order_index": 3},
    {"profile_type": "precio", "category": "objecion", "question": "Me parece caro", "expected_answer": "Este modelo tiene condiciones especiales. Puedo hacerte una simulación de cuota para ver cómo queda con financiación.", "manual_reference": "5.4", "order_index": 4},

    # Perfil: indeciso
    {"profile_type": "indeciso", "category": "indagacion", "question": "¿Qué es lo que te genera dudas?", "expected_answer": "Entiendo. ¿Qué es lo que te genera dudas? Así te ayudo a resolverlas antes de que cambie la disponibilidad.", "manual_reference": "5.4", "order_index": 1},
    {"profile_type": "indeciso", "category": "objecion", "question": "Lo voy a pensar", "expected_answer": "Entiendo. ¿Qué es lo que te genera dudas? Así te ayudo a resolverlas antes de que cambie la disponibilidad.", "manual_reference": "5.4", "order_index": 2},
    {"profile_type": "indeciso", "category": "herramienta", "question": "¿Cómo podés ayudarlo a tomar la decisión?", "expected_answer": "Ofrecerle una simulación de cuotas y un resumen escrito para que pueda consultarlo con quien necesite.", "manual_reference": "5.3", "order_index": 3},

    # Perfil: informado
    {"profile_type": "informado", "category": "validacion", "question": "¿Cómo respondés cuando el cliente trae información de internet?", "expected_answer": "Validar lo que es correcto, corregir con datos concretos lo que no, y ofrecer evidencia: historia clínica, documentación, specs reales del vehículo.", "manual_reference": "5.2", "order_index": 1},
    {"profile_type": "informado", "category": "diferencial", "question": "¿Qué tiene Vázquez que no tiene lo que el cliente encontró online?", "expected_answer": "Garantía documentada, respaldo documental completo (historia clínica, libre deuda), acompañamiento postventa real, y prueba de manejo antes de decidir.", "manual_reference": "5.2", "order_index": 2},

    # Perfil: agro
    {"profile_type": "agro", "category": "tecnica", "question": "¿Qué datos necesitás saber antes de recomendar un vehículo para el campo?", "expected_answer": "Tipo de terreno, km anuales estimados, si es uso mixto o exclusivo campo, si necesita tracción 4x4, y si requiere financiación.", "manual_reference": "5.2", "order_index": 1},
    {"profile_type": "agro", "category": "servicio", "question": "¿Qué pasa si se rompe lejos?", "expected_answer": "Vázquez Auto ofrece garantía documentada en usados selecto (3 meses motor/caja) y la historia clínica del vehículo para respaldar cada reparación previa.", "manual_reference": "5.7", "order_index": 2},

    # Perfil: credito
    {"profile_type": "credito", "category": "pre_evaluacion", "question": "¿Cómo evaluás si un cliente puede acceder a crédito?", "expected_answer": "Preguntá situación laboral, antigüedad en el trabajo, si está en relación de dependencia o es monotributista, e ingresos aproximados.", "manual_reference": "5.1", "order_index": 1},
    {"profile_type": "credito", "category": "objecion", "question": "No sé si el financiamiento me sale", "expected_answer": "Te hago una pre-consulta ahora. En menos de 24 hs te confirmo si califica y con qué condiciones.", "manual_reference": "5.4", "order_index": 2},

    # Perfil: primera_compra
    {"profile_type": "primera_compra", "category": "proceso", "question": "¿Cómo explicás el proceso a alguien que nunca compró un auto?", "expected_answer": "Explicar las 8 etapas en lenguaje simple: desde el primer contacto hasta la postventa. Qué papeles necesita, qué firma, qué pasa en cada paso.", "manual_reference": "5.1", "order_index": 1},
    {"profile_type": "primera_compra", "category": "diferencial", "question": "¿Por qué comprar en Vázquez siendo la primera vez?", "expected_answer": "Transparencia documental total, acompañamiento en cada etapa, garantía en usados selecto, y un vendedor que explica todo sin apuro.", "manual_reference": "1", "order_index": 2},

    # Objeciones generales
    {"profile_type": "general", "category": "objecion", "question": "Me parece caro", "expected_answer": "Este modelo tiene condiciones especiales. Puedo hacerte una simulación de cuota para ver cómo queda con financiación.", "manual_reference": "5.4", "order_index": 1},
    {"profile_type": "general", "category": "objecion", "question": "Lo voy a pensar", "expected_answer": "Entiendo. ¿Qué es lo que te genera dudas? Así te ayudo a resolverlas antes de que cambie la disponibilidad.", "manual_reference": "5.4", "order_index": 2},
    {"profile_type": "general", "category": "objecion", "question": "Lo vi más barato en otro lado", "expected_answer": "Te lo creo. Además del precio, ¿qué más estás valuando? Puedo mostrarte qué incluye nuestra propuesta que tal vez no esté en la otra.", "manual_reference": "5.4", "order_index": 3},
    {"profile_type": "general", "category": "objecion", "question": "No sé si el financiamiento me sale", "expected_answer": "Te hago una pre-consulta ahora. En menos de 24 hs te confirmo si califica y con qué condiciones.", "manual_reference": "5.4", "order_index": 4},
]


def seed_users(admin):
    """Crea usuarios via REST API directa para evitar problemas de trigger."""
    import httpx, json
    print("Creando usuarios...")
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    for u in USERS:
        # 1. Verificar si ya existe en profiles
        try:
            existing = admin.table("profiles").select("id").eq("email", u["email"]).execute()
            if existing.data:
                print(f"  [ya existe] {u['full_name']}")
                continue
        except Exception:
            pass

        # 2. Crear usuario en Auth via REST
        try:
            resp = httpx.post(
                f"{url}/auth/v1/admin/users",
                headers=headers,
                json={
                    "email": u["email"],
                    "password": u["password"],
                    "email_confirm": True,
                    "user_metadata": {"full_name": u["full_name"], "role": u["role"]}
                },
                timeout=20,
            )
            if resp.status_code not in (200, 201):
                body = resp.json()
                msg = body.get("message", body.get("msg", str(body)))
                if "already" in msg.lower():
                    print(f"  [ya existe] {u['full_name']}")
                    continue
                print(f"  ERROR auth {u['full_name']}: {msg[:100]}")
                continue

            user_id = resp.json().get("id")
            if not user_id:
                print(f"  ERROR: no user_id para {u['full_name']}")
                continue

        except Exception as e:
            print(f"  ERROR auth {u['full_name']}: {e}")
            continue

        # 3. Insertar profile directamente
        try:
            admin.table("profiles").upsert({
                "id": user_id,
                "full_name": u["full_name"],
                "email": u["email"],
                "role": u["role"],
                "is_active": True,
                "must_change_password": False,
            }).execute()
            print(f"  OK {u['full_name']} ({u['role']})")
        except Exception as e:
            print(f"  ERROR profile {u['full_name']}: {e}")


def seed_manual(admin):
    print("Cargando secciones del manual...")
    for s in MANUAL_SECTIONS:
        try:
            existing = admin.table("manual_sections").select("id").eq("section_number", s["section_number"]).execute().data
            if existing:
                admin.table("manual_sections").update({
                    "title": s["title"],
                    "content": s["content"],
                }).eq("id", existing[0]["id"]).execute()
            else:
                admin.table("manual_sections").insert({
                    "section_number": s["section_number"],
                    "title": s["title"],
                    "content": s["content"],
                    "quiz_questions": [],
                }).execute()
            print(f"  OK Seccion {s['section_number']}: {s['title']}")
        except Exception as e:
            print(f"  ⚠ Sección {s['section_number']}: {e}")


def seed_question_guide(admin):
    print("Cargando guía de preguntas...")
    try:
        admin.table("question_guide").delete().neq("id", 0).execute()
    except Exception:
        pass
    for q in QUESTION_GUIDE:
        try:
            admin.table("question_guide").insert(q).execute()
        except Exception as e:
            print(f"  ⚠ {q['question'][:40]}: {e}")
    print(f"  OK {len(QUESTION_GUIDE)} preguntas cargadas")


def main():
    admin = get_admin_client()
    print("=== Seed Portal Vázquez Auto ===")
    seed_users(admin)
    seed_manual(admin)
    seed_question_guide(admin)
    print("\n✅ Seed completado.")
    print("\nUsuarios creados:")
    for u in USERS:
        print(f"  {u['email']} / {u['password']} ({u['role']})")


if __name__ == "__main__":
    main()
