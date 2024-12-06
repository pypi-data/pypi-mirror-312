"""Create QR use case."""

from datetime import date, timedelta

from sincpro_payments_sdk.apps.common.domain import CurrencyType
from sincpro_payments_sdk.apps.qr import DataTransferObject, Feature, qr
from sincpro_payments_sdk.apps.qr.domain.bnb.qr import QRImage


class CommandCreateQR(DataTransferObject):
    """Command to create a QR code."""

    amount: float
    currency: str
    description: str
    extra_reference: str
    single_use: bool = True
    expiration_date: date | None = None


class ResponseCreateQR(QRImage):
    """Response from creating a QR code."""


@qr.feature(CommandCreateQR)
class CreateQR(Feature):
    """Create QR code."""

    def execute(self, command: CommandCreateQR) -> ResponseCreateQR:
        """Create QR code."""
        currency = CurrencyType(command.currency)
        qr_expiration_date = command.expiration_date or date.today() + timedelta(weeks=1)
        response_api = self.bnb_qr_adapter.generate_qr(
            currency=currency,
            gloss=command.description,
            amount=command.amount,
            extra_metadata=command.extra_reference,
            expiration_date=qr_expiration_date,
            single_use=command.single_use,
            destination_account=1,
        )

        return ResponseCreateQR.model_validate(response_api)
