import re


def improve_task_description(title: str, notes: str = "") -> str:
    """
    Improve a task description locally using rule-based logic.
    No external API or language model is required.
    """

    title = re.sub(r"\s+", " ", title).strip().rstrip(". ")
    notes = re.sub(r"\s+", " ", notes).strip()

    if not title:
        raise ValueError("Task title cannot be empty.")

    normalized_title = title.lower()

    # Task keywords and their corresponding objective templates.
    task_rules = [
        (
            r"^(create|build|develop|implement)\b\s*",
            lambda match, text: f"Create and implement {text[match.end():].strip() or text}."
        ),
        (
            r"^(fix|resolve|debug)\b\s*",
            lambda match, text: f"Investigate and resolve: {text}."
        ),
        (
            r"^(test|testing|validate)\b\s*",
            lambda match, text: f"Test and validate {text[match.end():].strip() or text}."
        ),
        (
            r"^(update|improve|enhance|optimize)\b\s*",
            lambda match, text: f"Improve and refine {text[match.end():].strip() or text}."
        ),
        (
            r"^(study|learn|research|explore)\b\s*",
            lambda match, text: f"Study and understand {text[match.end():].strip() or text}."
        ),
        (
            r"^(integrate|integration)\b\s*",
            lambda match, text: f"Integrate {text[match.end():].strip() or text}."
        ),
    ]

    objective = None

    for pattern, formatter in task_rules:
        match = re.match(pattern, normalized_title, flags=re.IGNORECASE)
        if match:
            objective = formatter(match, title)
            break

    if objective is None:
        objective = f"Complete the task: {title}."

    # Build a concise description without unnecessary generic requirements.
    description = f"Objective:\n{objective}"

    if notes:
        description += f"\n\nAdditional Details:\n{notes}"

    return description