from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql://postgres:admin@localhost/tickets_orm"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = DeclarativeBase()

class Base(DeclarativeBase):
    pass

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(100), unique= True, index = False)

    seats = relationship("EventSeat", back_populates= "event", cascade="all, delete")
    tickets = relationship("EventTicket", back_populates= "event", cascade="all, delete")

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key = True, index = True)
    seat_name = Column(String(100), unique= True, index = False)

    events = relationship("EventSeat", back_populates= "seat", cascade="all, delete")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_name = Column(String(100), unique=True, index=False)
    is_booked = Column(Boolean, nullable=False, default=False)

    events = relationship("EventTicket", back_populates="ticket", cascade="all, delete")

class EventSeat(Base):
    __tablename__ = "events_seats"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    seat_id = Column(Integer, ForeignKey("seats.id", ondelete="CASCADE"))

    event = relationship("Event", back_populates="seats")
    seat = relationship("Seat", back_populates="events")

class EventTicket(Base):
    __tablename__ = "events_tickets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"))

    event = relationship("Event", back_populates="tickets")
    ticket = relationship("Ticket", back_populates="events")



def init_db():
    Base.metadata.create_all(engine)

def get_all_events():
    with SessionLocal() as session:
        return session.query(Event).all()

def get_all_seats():
    with SessionLocal() as session:
        return session.query(Seat).all()

def get_all_tickets():
    with SessionLocal() as session:
        return session.query(Ticket).all()

def create_event(title):
    with SessionLocal() as session:
        event = Event(title=title)
        session.add(event)
        session.commit()

def create_seat(seat_name):
    with SessionLocal() as session:
        seat = Seat(seat_name=seat_name)
        session.add(seat)
        session.commit()

def create_ticket(ticket_name):
    with SessionLocal() as session:
        ticket = Ticket(ticket_name=ticket_name, is_booked=False)
        session.add(ticket)
        session.commit()

def get_event_info_by_id(event_id):
    with SessionLocal() as session:
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None
        return {
            "event_info": event,
            "seats": [es.seat.seat_name for es in event.seats],
            "tickets": [et.ticket.ticket_name for et in event.tickets],
        }

def search_event(event_title):
    with SessionLocal() as session:
        return session.query(Event).filter(Event.title.ilike(f"%{event_title}%")).all()

def delete_event(event_title):
    with SessionLocal() as session:
        event = session.query(Event).filter(Event.title==event_title).first()
        session.delete(event)
        session.commit()

def edit_event(event_title, new_event_title):
    with SessionLocal() as session:
        event = session.query(Event).filter(Event.title==event_title).first()
        event.title = new_event_title
        session.commit()

def delete_seat(seat_name):
    with SessionLocal() as session:
        seat = session.query(Seat).filter(Seat.seat_name==seat_name).first()
        session.delete(seat)
        session.commit()

def edit_seat(seat_name, new_seat_name):
    with SessionLocal() as session:
        seat = session.query(Seat).filter(Seat.seat_name==seat_name).first()
        seat.seat_name = new_seat_name
        session.commit()

def get_all_tickets_by_booking_status(is_booked):
    with SessionLocal() as session:
        return session.query(Ticket).filter(Ticket.is_booked == is_booked).all()

def edit_ticket_booking(ticket_id, is_booked):
    with SessionLocal() as session:
        ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
        ticket.is_booked = is_booked
        session.commit()