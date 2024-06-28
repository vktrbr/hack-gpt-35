from src.llm_calls.call_dolphin import call_dolphin


def prepare_themes(prefix: str, topics: list, template: str = "{topic}"):
    """
    Prepare NSFW topics for the LLM model

    :return:
    """

    for topic in topics:
        request = template.format(topic=topic)

        call_dolphin(
            request,
            f"{prefix}-{topic.replace(' ', '-')}"
        )

    return "Themes prepared"
