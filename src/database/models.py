from typing import List, Optional
from sqlalchemy import  Integer, String, ForeignKey, REAL, Date, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = 'product'

    # id is code and a varchar
    code: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(REAL)
    photourl: Mapped[str] = mapped_column(String(200))
    
    def __repr__(self):
        return f'Producto {self.id_product} {self.name} {self.price} {self.photourl}'
    
class Client(Base):
    __tablename__ = 'client'

    id_client: Mapped[int] = mapped_column( primary_key=True)
    pid: Mapped[str] = mapped_column(String(30))
    dir: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[str] = mapped_column(String(100))
    
    def __repr__(self):
        return f'Cliente {self.name} {self.surname}'
    
    
class Invoice(Base):
    __tablename__ = 'invoice'

    id_invoice: Mapped[int] = mapped_column(primary_key=True)
    id_client: Mapped[int] = mapped_column(Integer, ForeignKey('client.id_client'))
    date: Mapped[Date] = mapped_column(Date)
    void: Mapped[bool] = mapped_column(Boolean, default=False)
    
    client: Mapped[Client] = relationship('Client', backref='invoices')
    
    def __repr__(self):
        return f'Factura {self.id_invoice} {self.date} {self.void}'

class InvoiceProduct(Base):
    __tablename__ = 'invoice_product'
    
    id_invoice: Mapped[int] = mapped_column(Integer, ForeignKey('invoice.id_invoice'))
    id_product: Mapped[str] = mapped_column(String(10), ForeignKey('product.code'))
    quantity: Mapped[int] = mapped_column(Integer)
    
    invoice: Mapped[Invoice] = relationship('Invoice', backref='products')
    
    product: Mapped[Product] = relationship('Product', backref='invoices')

class Bank(Base):
    __tablename__ = 'bank'
    
    id_bank: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    
    def __repr__(self):
        return f'Banco {self.name}'

class PaymentMethod(Base):
    __tablename__ = 'payment_method'
    
    id_method: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    
    def __repr__(self):
        return f'Metodo de pago {self.name}'
    
class Payment(Base):
    __tablename__ = 'payment'
    
    id_invoice: Mapped[int] = mapped_column(Integer, ForeignKey('invoice.id_invoice'))
    id_bank: Mapped[int] = mapped_column(Integer, ForeignKey('bank.id_bank'))
    id_method: Mapped[int] = mapped_column(Integer, ForeignKey('payment_method.id_method'))
    amount: Mapped[float] = mapped_column(REAL)
    
    invoice: Mapped[Invoice] = relationship('Invoice', backref='payments')
    bank: Mapped[Bank] = relationship('Bank', backref='payments')
    method: Mapped[PaymentMethod] = relationship('PaymentMethod', backref='payments')
    
    
    def __repr__(self):
        return f'Pago {self.id_payment} {self.date} {self.amount}'
    
table_name_map = {
    "product": Product,
    "client": Client,
    "invoice": Invoice,
    "invoice_product": InvoiceProduct,
    "bank": Bank,
    "payment_method": PaymentMethod,
    "payment": Payment
    
}
                                            

    
