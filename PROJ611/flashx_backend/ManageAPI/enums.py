from enum import Enum

class InvoiceStatus(Enum):
    CREATED = 'created'
    WAITING = 'waiting'
    DELIVERING = 'delivering'
    COMPLETED = 'completed'
    CANCELED = 'canceled'