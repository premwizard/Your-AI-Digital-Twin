from typing import Dict, List, Optional
from app.services.personality import personality_brief, personality_tone
from app.services.memory import summarize_memories, summarize_conversations, compact_text
from app.services.future_self import future_profile_brief


def build_context(
    personality: Dict,
    memories: List[Dict],
    documents: List[Dict],
    future_profile: Dict,
    conversation_summary: str,
    mode: str,
    user_message: str,
) -> str:
    sections = [
        "You are a digital twin AI that must behave like the user, not a generic assistant.",
        "Use stored personality, memories, documents, goals, and prior conversations to answer in the user's voice.",
    ]

    if personality:
        sections.append("--- Personality Profile ---")
        sections.append(personality_brief(personality))
        sections.append(personality_tone(personality))

    if future_profile:
        sections.append("--- Future Self Goals ---")
        sections.append(future_profile_brief(future_profile))
        sections.append("Always keep the user's long-term goals and future self vision in mind.")

    if conversation_summary:
        sections.append("--- Recent Conversation Summary ---")
        sections.append(conversation_summary)

    if memories:
        sections.append("--- Relevant Memories ---")
        sections.append(summarize_memories(memories))

    if documents:
        sections.append("--- Training Documents ---")
        for document in documents[:4]:
            content = document.get("summary", document.get("content", "")).replace("\n", " ")
            sections.append(f"{document.get('title', 'Document')} ({document.get('document_type', 'unknown')}): {content[:220]}")

    mode_instruction = _select_mode_instruction(mode)
    if mode_instruction:
        sections.append("--- Response Guidelines ---")
        sections.append(mode_instruction)

    sections.append("--- User Query ---")
    sections.append(user_message)
    sections.append("--- End Context ---")

    context = "\n".join(sections)
    return compact_text(context)


def _select_mode_instruction(mode: str) -> Optional[str]:
    mode = (mode or "normal").lower()
    if mode == "career":
        return (
            "Give actionable career guidance. Reference the user's skills, goals, experiences, and learning path. "
            "Do not give generic advice; make it sound like the user's own voice."
        )
    if mode == "interview":
        return (
            "Answer as if you are responding to an interview question. Use the user's real projects, strengths, and experiences. "
            "Be concise, confident, and avoid vague, generic statements."
        )
    if mode == "future":
        return (
            "Speak from the perspective of the user's future self. Prioritize future role, timeline, and career vision. "
            "Use first-person perspective and project confidence in goal progress."
        )
    return (
        "Answer naturally in the user's voice. Use stored profile details, memories, and documents. "
        "Avoid generic AI-style phrasing and make the response feel personal."
    )
