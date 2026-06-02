"""Genera quizzes para todas las secciones del manual usando Anthropic API."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

from supabase_client import get_admin_client
from utils.quiz_generator import generate_quiz_questions
import json

client = get_admin_client()
sections = client.table("manual_sections").select("id,title,content,quiz_questions").order("id").execute().data
print(f"Total secciones: {len(sections)}")

for s in sections:
    has_q = s.get("quiz_questions") and len(s["quiz_questions"]) > 0
    status = "OK" if has_q else "VACIO"
    print(f"  [{status}] {s['id']}: {s['title']}")

print("\nGenerando quizzes para secciones sin preguntas...")
for s in sections:
    has_q = s.get("quiz_questions") and len(s["quiz_questions"]) > 0
    if True:  # regenerar todas
        print(f"  Generando: {s['title']}...", end=" ", flush=True)
        try:
            questions = generate_quiz_questions(s["title"], s["content"])
            if questions:
                client.table("manual_sections").update({"quiz_questions": questions}).eq("id", s["id"]).execute()
                print(f"OK ({len(questions)} preguntas)")
            else:
                print("Sin preguntas generadas")
        except Exception as e:
            print(f"ERROR: {e}")

print("\nListo.")
