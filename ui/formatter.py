def format_answer(content_type: str, text: str) -> str:
    text = text.strip()

    if content_type == "hook":
        return (
            "🔥 *ХУК*\n\n"
            f"«{text}»"
        )

    if content_type == "script":
        return (
            "🎬 *СЦЕНАРИЙ ДЛЯ ВИДЕО*\n\n"
            f"{text}"
        )

    if content_type == "ads":
        return (
            "📢 *РЕКЛАМНЫЙ СКРИПТ*\n\n"
            f"{text}"
        )

    return text
