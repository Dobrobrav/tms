from tasks.domain.attachments.attachment_entity import AttachmentEntity
from tasks.models import TaskAttachmentModel


class AttachmentRepository:
    def set(self, attachment_entity: AttachmentEntity) -> int:
        attachment_already_stored = bool(attachment_entity.attachment_id)
        if attachment_already_stored:
            TaskAttachmentModel.objects.filter(pk=attachment_entity.attachment_id).update(
                filename=attachment_entity.filename
            )
            return attachment_entity.attachment_id

        return TaskAttachmentModel.objects.create(
            filename=attachment_entity.filename,
        ).pk
