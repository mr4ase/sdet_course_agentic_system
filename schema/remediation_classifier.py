# schema\remediation_classifier.py

from pydantic import BaseModel, Field


class RemediationClassifier(BaseModel):
    remediation_is_needed: bool = Field(
        description="Просит ли ученик в сообщении помощи, чтобы ему объяснили текущую тему еще более подробно. Оцени смысл сообщения студента. Если по смыслу видно, что студент просит помощи - то выставь значение True, если помощь не требуется - то False"
    )
