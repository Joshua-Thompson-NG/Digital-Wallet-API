import enum
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CurrencyEnum(str, enum.Enum):
    USD = "USD"
    EUR = "EUR"
    NGN = "NGN"
    GHS = "GHS"

class TransactionEnum(str, enum.Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"

class Wallet(Base):
    __tablename__ = "wallets"

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    account_number:Mapped[str] = mapped_column(String(50), unique=True,
                                               nullable=False, index=True)
    owner_name:Mapped[str] = mapped_column(String(100), nullable=False)
    currency:Mapped[CurrencyEnum] = mapped_column(Enum(CurrencyEnum), nullable=False)

    balance:Mapped[Decimal] = mapped_column(Numeric(12,2), 
                                            default=("0.00"), nullable=False)
    hashed_pin:Mapped[str] = mapped_column(String(255), nullable=False)
    is_frozen:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationship 1:M
    transactions: Mapped[list["Transaction"]] = relationship(  # noqa: F821
        "Transaction",
        back_populates="wallet",
        cascade="all, delete-orphan",
        order_by="desc(Transaction.timestamp)",
    )

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False, index=True)

    transaction_type: Mapped[TransactionEnum] = mapped_column(Enum(TransactionEnum), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    reference_account: Mapped[str | None] = mapped_column(String(50), nullable=True)  # Counterparty account number on transfers
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Inverse relationship: Many Transactions -> 1 Wallet
    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="transactions")


