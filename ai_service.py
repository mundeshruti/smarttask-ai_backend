import re

def improve_task_description(title: str, notes: str = "") -> str:
    """
    Improve a task description locally using rule-based logic.
    Returns a natural description without extra headings.
    No external API or language model is required.
    """

    title = re.sub(r"\s+", " ", title).strip().rstrip(". ")
    notes = re.sub(r"\s+", " ", notes).strip()

    if not title:
        raise ValueError("Task title cannot be empty.")

    normalized_title = title.lower()

    task_rules = [
        (
            r"^(create|build|develop|implement)\b\s*",
            lambda match, text: (
                f"Create and implement "
                f"{text[match.end():].strip() or text}."
            ),
        ),
        (
            r"^(fix|resolve|debug)\b\s*",
            lambda match, text: f"Investigate and resolve: {text}.",
        ),
        (
            r"^(test|testing|validate)\b\s*",
            lambda match, text: (
                f"Test and validate "
                f"{text[match.end():].strip() or text}."
            ),
        ),
        (
            r"^(update|improve|enhance|optimize)\b\s*",
            lambda match, text: (
                f"Improve and refine "
                f"{text[match.end():].strip() or text}."
            ),
        ),
        (
            r"^(study|learn|research|explore)\b\s*",
            lambda match, text: (
                f"Study and understand "
                f"{text[match.end():].strip() or text}."
            ),
        ),
        (
            r"^(integrate|integration)\b\s*",
            lambda match, text: (
                f"Integrate "
                f"{text[match.end():].strip() or text}."
            ),
        ),
    ]

    description = None

    for pattern, formatter in task_rules:
        match = re.match(pattern, normalized_title, flags=re.IGNORECASE)
        if match:
            description = formatter(match, title)
            break

    if description is None:
        description = title
        if not description.endswith((".", "!", "?")):
            description += "."

    # Include notes naturally, without adding a heading.
    if notes and notes.lower() not in description.lower():
        description = f"{description.rstrip('.')} — {notes}"

    return description
