from http import HTTPStatus
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def ping():
    return jsonify({'message': 'Server is up'}), HTTPStatus.OK

@app.route('/events', methods=['GET'])
def get_all_events():
    events = db.get_all_events()
    return jsonify({'events': events}), HTTPStatus.OK

@app.route('/seats', methods=['GET'])
def get_all_seats():
    seats = db.get_all_seats()
    return jsonify({'seats': seats}), HTTPStatus.OK

@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    tickets = db.get_all_tickets()
    return jsonify({'tickets': tickets}), HTTPStatus.OK

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event_by_id(event_id):
    return jsonify({'message': 'в разработке'}), HTTPStatus.NOT_IMPLEMENTED

@app.route('/events', methods=['POST'])
def create_event():
    try:
        event = request.get_json()
    except Exception as e:
        return jsonify({'error': f"error during reading request body: {e}"}), HTTPStatus.BAD_REQUEST
    if event is None:
        return jsonify({'error': 'body is required'}), HTTPStatus.BAD_REQUEST
    elif event ['title'] is None or event ['title'] == '':
        return jsonify({'error': 'title is required'}), HTTPStatus.BAD_REQUEST

    db.create_event(event['title'])

    return jsonify({'message': 'posts created is successfully'}), HTTPStatus.CREATED

@app.route('/seats', methods=['POST'])
def create_seat():
    try:
        seat = request.get_json()
    except Exception as e:
        return jsonify({'error': f"error during reading request body: {e}"}), HTTPStatus.BAD_REQUEST
    if seat is None:
        return jsonify({'error': 'body is required'}), HTTPStatus.BAD_REQUEST
    elif seat ['seat_name'] is None or seat ['seat_name'] == '':
        return jsonify({'error': 'seat_name is required'}), HTTPStatus.BAD_REQUEST

    db.create_seat(seat['seat_name'])

    return jsonify({'message': 'posts created is successfully'}), HTTPStatus.CREATED

@app.route('/tickets', methods=['POST'])
def create_ticket():
    try:
        ticket = request.get_json()
    except Exception as e:
        return jsonify({'error': f"error during reading request body: {e}"}), HTTPStatus.BAD_REQUEST
    if ticket is None:
        return jsonify({'error': 'body is required'}), HTTPStatus.BAD_REQUEST
    elif ticket ['ticket_name'] is None or ticket ['ticket_name'] == '':
        return jsonify({'error': 'ticket_name is required'}), HTTPStatus.BAD_REQUEST

    db.create_ticket(ticket['ticket_name'])

    return jsonify({'message': 'posts created is successfully'}), HTTPStatus.CREATED

@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    return jsonify({'message': 'в разработке'}), HTTPStatus.NOT_IMPLEMENTED

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    return jsonify({'message': 'в разработке'}), HTTPStatus.NOT_IMPLEMENTED

@app.route('/seats/<int:seat_id>', methods=['DELETE'])
def delete_seat(seat_id):
    return jsonify({'message': 'в разработке'}), HTTPStatus.NOT_IMPLEMENTED

@app.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):

    return jsonify({'message': 'в разработке'}), HTTPStatus.NOT_IMPLEMENTED


def main():
    try:
        db.init_db()
        print("DB initialized successfully")
    except Exception as e:
        print(f"Error during DB initialization: {e}")

    try:
        app.run(port=5001)
    except Exception as e:
        print(f"Error during Server initialization: {e}")

main()




def print_menu():
    print("Выберете нужную команду: ")
    print("0. Выход")
    print("1. Показать список мероприятий") #+
    print("2. Показать список мест") #+
    print("3. Показать список билетов") #+
    print("4. Показать детальную информацию по id мероприятия") #+
    print("5. Добавить мероприятие") #+ def create_event
    print("6. Поиск мероприятия по названию")
    print("7. Удаление мероприятия") #+
    print("8. Редактирование мероприятия")
    print("9. Добавить место(seat)")
    print("10. Удалить место(seat)")
    print("11. Редактирование места(seat)")
    print("12. Поиск места по названию")
    print("13. Поиск билета по названию")
    print("14. Добавить бронирование билета")
    print("15. Отменить бронирование билета")
    print("16. Добавить билет")


def app():
    db.init_db()
    print("База данных инициализирована!")
    print("Вас приветствует сервис резервирования билетов!")
    while True:
        print_menu()
        cmd = int(input("Введите номер команды: "))

        if cmd == 0:
            print("До скорой встречи")
            break
        elif cmd == 1:
            print("=" * 20)
            print("\nСписок мероприятий: ")
            events = db.get_all_events()
            for event in events:
                print(f"ID: {event.id} - Title: {event.title}.")
            print("=" * 20)

        elif cmd == 2:
            print("=" * 20)
            print("\nСписок мест: ")
            seats = db.get_all_seats()
            for seat in seats:
                print(f"ID: {seat.id} - Seat: {seat.seat_name}.")
            print("=" * 20)

        elif cmd == 3:
            print("=" * 20)
            print("\nСписок билетов: ")
            tickets = db.get_all_tickets()
            for ticket in tickets:
                print(f"ID: {ticket.id} - Ticket: {ticket.ticket_name}.")
            print("=" * 20)

        elif cmd == 4:
            print("=" * 20)
            print("\nИнформация по мероприятию: ")
            event_id = int(input("Введите id мероприятия: "))
            event_details = db.get_event_info_by_id(event_id)
            if event_details is None:
                print("Нет такого мероприятия!")
            else:
                event_info = event_details["event_info"]
                print(f' ID: {event_info.id} - Название: {event_info.title}')

                seats = event_details["seats"]
                print("Места: ")
                for seat in seats:
                    print(seat, end=" | ")

                tickets = event_details["tickets"]
                print("\nБилеты: ")
                for ticket in tickets:
                    print(ticket, end=" | ")
                print()
            print("=" * 20)

        elif cmd == 5:
            print("=" * 20)
            print("Добавление нового мероприятия: ")
            title = input("Введите название мероприятия: ")
            try:
                db.create_event(title)
                print("Мероприятие успешно создано!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")
            print("=" * 20)

        elif cmd == 6:
            print("=" * 20)
            event_name = input("Введите название или часть название мероприятия: ")

            events = db.search_event(event_name)
            for event in events:
                print(f"ID: {event.id} - Title: {event.title}.")
            print("=" * 20)

        elif cmd == 7:
            print("=" * 20)
            event_title = input("Введите название мероприятия, которое нужно удалить: ")
            try:
                db.delete_event(event_title)
                print("Мероприятие успешно удалено!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")

        elif cmd == 8:
            print("=" * 20)
            event_title = input("Введите название мероприятия, которое нужно отредактировать: ")
            new_event_title = input("Введите новое название мероприятия: ")
            try:
                db.edit_event(event_title, new_event_title)
                print("Мероприятие успешно отредактировано!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")

        elif cmd == 9:
            print("=" * 20)
            print("Добавление нового места: ")
            seat_name = input("Введите номер места: ")
            try:
                db.create_seat(seat_name)
                print("Номер места успешно добавлен!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")
            print("=" * 20)

        elif cmd == 10:
            print("=" * 20)
            seat_name = input("Введите номер места, которое нужно удалить: ")
            try:
                db.delete_seat(seat_name)
                print("Номер места успешно удален!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")

        elif cmd == 11:
            print("=" * 20)
            seat_name = input("Введите номер места, которое нужно отредактировать: ")
            new_seat_name = input("Введите новый номер места(seat): ")
            try:
                db.edit_seat(seat_name, new_seat_name)
                print("Номер места(seat) успешно отредактирован!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")

        elif cmd == 12:
            print("=" * 20)
            query = input("Введите название или часть названия места: ")

            seats = db.search_seat(query)
            for seat in seats:
                print(f"ID: {seat[0]} - Title: {seat[1]}.")
            print("=" * 20)

        elif cmd == 13:
            print("=" * 20)
            query = input("Введите название или часть названия билета: ")

            tickets = db.search_ticket(query)
            for ticket in tickets:
                print(f"ID: {ticket[0]} - Title: {ticket[1]}.")
            print("=" * 20)

        elif cmd == 14:
            print("=" * 20)
            print("\nСписок билетов: ")
            tickets = db.get_all_tickets_by_booking_status(False)
            for ticket in tickets:
                print(f"ID: {ticket.id} - Ticket: {ticket.ticket_name}.")
            print("=" * 20)
            ticket_id = input("Введите билет (id) для бронирования: ")
            db.edit_ticket_booking(ticket_id, True)
            print("Вы забронировали билет!")
            print("=" * 20)

        elif cmd == 15:
            print("=" * 20)
            print("\nСписок билетов: ")
            tickets = db.get_all_tickets_by_booking_status(True)
            for ticket in tickets:
                print(f"ID: {ticket.id} - Ticket: {ticket.ticket_name}.")
            print("=" * 20)
            ticket_id = input("Введите билет (id) для бронирования: ")
            db.edit_ticket_booking(ticket_id, False)
            print("Вы отменили бронь билета!")
            print("=" * 20)

        elif cmd == 16:
            print("=" * 20)
            print("Добавление нового билета: ")
            title = input("Введите название билета: ")
            try:
                db.create_ticket(title)
                print("Билет успешно создан!")
            except Exception as e:
                print(f"Что-то пошло не так! {e}")
            print("=" * 20)

        else:
            print("Вы ввели несуществующую команду. Попробуйте еще раз!")

app()