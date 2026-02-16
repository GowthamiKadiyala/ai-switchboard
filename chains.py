import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from personas import PERSONAS

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)


# =========================
# SINGLE PERSONA REWRITE
# =========================
def rewrite_with_persona(text, persona_key):
    persona_instruction = PERSONAS.get(persona_key)

    if not persona_instruction:
        return "Persona not found."

    prompt = ChatPromptTemplate.from_messages([
        ("system", persona_instruction),
        ("human", "Rewrite this text in your voice:\n\n{text}")
    ])

    formatted_prompt = prompt.format_messages(text=text)

    response = llm.invoke(formatted_prompt)
    return response.content


# =========================
# MULTI-PERSONA REWRITE
# =========================
def multi_rewrite(text, personas):
    results = {}

    for persona in personas:
        results[persona] = rewrite_with_persona(text, persona)

    return results


# =========================
# DEBATE MODE
# =========================
def debate(topic, persona_a, persona_b):
    persona_a_instruction = PERSONAS.get(persona_a)
    persona_b_instruction = PERSONAS.get(persona_b)

    if not persona_a_instruction or not persona_b_instruction:
        return {"error": "Invalid persona"}

    # Round 1 — Opening
    prompt_a_open = ChatPromptTemplate.from_messages([
        ("system", persona_a_instruction),
        ("human", f"You are debating: '{topic}'. Give your opening argument.")
    ])

    prompt_b_open = ChatPromptTemplate.from_messages([
        ("system", persona_b_instruction),
        ("human", f"You are debating: '{topic}'. Give your opening argument.")
    ])

    a_open = llm.invoke(prompt_a_open.format_messages()).content
    b_open = llm.invoke(prompt_b_open.format_messages()).content

    # Round 2 — Rebuttal
    prompt_a_rebuttal = ChatPromptTemplate.from_messages([
        ("system", persona_a_instruction),
        ("human", f"Your opponent said:\n{b_open}\n\nRespond strongly.")
    ])

    prompt_b_rebuttal = ChatPromptTemplate.from_messages([
        ("system", persona_b_instruction),
        ("human", f"Your opponent said:\n{a_open}\n\nRespond strongly.")
    ])

    a_rebuttal = llm.invoke(prompt_a_rebuttal.format_messages()).content
    b_rebuttal = llm.invoke(prompt_b_rebuttal.format_messages()).content

    # Judge
    judge_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a neutral debate judge."),
        ("human", f"""
Topic: {topic}

{persona_a} opening:
{a_open}

{persona_b} opening:
{b_open}

{persona_a} rebuttal:
{a_rebuttal}

{persona_b} rebuttal:
{b_rebuttal}

Who won and why?
""")
    ])

    judge_result = llm.invoke(judge_prompt.format_messages()).content

    return {
        "round_1": {
            persona_a: a_open,
            persona_b: b_open
        },
        "round_2": {
            persona_a: a_rebuttal,
            persona_b: b_rebuttal
        },
        "judge": judge_result
    }
