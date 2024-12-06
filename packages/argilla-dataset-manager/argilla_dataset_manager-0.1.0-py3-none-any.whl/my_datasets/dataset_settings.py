import argilla as rg

def get_dataset_settings():
    """
    Define dataset settings.

    Returns:
        Argilla Settings object.
    """
    settings = rg.Settings(
        guidelines=(
            "Review each entry to confirm the relevancy and accuracy of the fields. "
            "Provide edits or updates where needed. Determine if the response satisfactorily answers the user's question. "
            "For example, a satisfactory response directly addresses the user's query with accurate information, while an unsatisfactory response may be off-topic or contain inaccuracies."
        ),
        fields=[
            rg.TextField(
                name="prompt",
                title="User's Question (Prompt)",
                use_markdown=False,
            ),
            rg.TextField(
                name="response",
                title="Agent's Response",
                use_markdown=False,
            ),
            rg.TextField(
                name="context",
                title="Context of the Conversation",
                use_markdown=False,
            ),
            rg.TextField(
                name="keywords",
                title="Keywords Associated with the Entry",
                use_markdown=False,
            ),
            rg.TextField(
                name="category",
                title="Category of the Entry",
                use_markdown=False,
            ),
            rg.TextField(
                name="references",
                title="References (e.g., links, documents)",
                use_markdown=False,
            ),
        ],
        questions=[
            rg.LabelQuestion(
                name="is_response_satisfactory",
                title="Would this response be 100% satisfactory to the user's question?",
                labels=["Yes", "No"],
            )
        ],
        metadata=[
            rg.TermsMetadataProperty(
                name="conversation_date",
                title="Date of Conversation",
            ),
            rg.TermsMetadataProperty(
                name="source_platform",
                title="Source Platform",
            ),
        ],
        allow_extra_metadata=True,
    )
    return settings