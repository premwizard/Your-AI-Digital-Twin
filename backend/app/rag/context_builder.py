from typing import Dict, List


def assemble_context(personality: Dict, memories: List[Dict], documents: List[Dict]) -> str:
    chunks = ["AI Digital Twin Context Builder"]
    if personality:
        chunks.append("Personality profile:")
        chunks.append(str({
            "personality_type": personality.get("personality_type"),
            "communication_style": personality.get("communication_style"),
            "career_interests": personality.get("career_interests"),
            "goals": personality.get("goals"),
            "strengths": personality.get("strengths"),
            "weaknesses": personality.get("weaknesses"),
            "skills": personality.get("skills"),
        }))
    if memories:
        chunks.append("Memories:")
        for memory in memories[:5]:
            chunks.append(f"- {memory.get('title')}: {memory.get('content')}")
    if documents:
        chunks.append("Training documents:")
        for doc in documents[:3]:
            chunks.append(f"- {doc.get('title', 'Document')} ({doc.get('document_type')}): {doc.get('content', '')[:140]}...")
    chunks.append("End of context.")
    return "\n".join(chunks)
