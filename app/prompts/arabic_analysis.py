"""
Prompts for Arabic word analysis.
"""

SYSTEM_PROMPT = "You are an expert in Arabic morphology."


def get_analysis_prompt(word: str) -> str:
    """
    Get the prompt for analyzing an Arabic word.

    Args:
        word: The Arabic word to analyze

    Returns:
        str: The formatted prompt
    """
    return f"""
    Given the Arabic word "{word}", analyze it and provide:
    1. The morphological pattern (الوزن)
    2. The root verb (الفعل)
    3. The type of the word (نوع الكلمة) (e.g., noun, verb, adjective)
    4. The singular/plural form (العدد)
    5. The gender (الجنس)
    6. The tense (الزمن) if it's a verb
    7. The derivation type (نوع الاشتقاق) (e.g., اسم فاعل, اسم مفعول)
    8. The meaning of the root verb (معنى الجذر)
    9. The diacritical marks (الحركات)
    10. An example of usage (مثال الاستخدام)

    Provide the response in JSON format with these exact keys in Arabic:
    {{
        "الكلمة": "{word}",
        "الوزن": "the pattern",
        "الفعل": "the root verb",
        "نوع الكلمة": "type of the word",
        "العدد": "singular/plural",
        "الجنس": "gender",
        "الزمن": "tense",
        "نوع الاشتقاق": "derivation type",
        "معنى الجذر": "meaning of the root verb",
        "الحركات": "diacritical marks",
        "مثال الاستخدام": "example of usage"
    }}
    """
