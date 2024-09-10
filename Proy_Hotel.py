import tkinter as tk
import re
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox

#variables globales
editing_mode = False
clients = []
clientId = 1
# Client = {
#     'Id' : n,
#     'name' : str with len < 60,
#     'address' : str,
#     'email' : str type mail,
#     'phoneNumber' : lada de pais +10 digits
# }
reservations = []
reservationId = 1
# Reservation = {
#     'Id' : n,
#     'clientId' : n,
#     'roomId' : n,
#     'reservationDate' : "MM/DD/YYYY",
#     'reservationHour' : "HH:MM",
#     'leaveDate' : "MM/DD/YYYY",
#     'price' : 0 no negativo
# }
rooms = []
roomId = 1
#Room = {
#     'Id' : n, autoIncrement
#     'roomNumber' : 0,
#     'state' : (Libre,Reservado,Cancelado)
# }

def createClient(name, address, email, phoneNumber):
    global clientId
    newClient = {
        'Id' : clientId,
        'name' : name,
        'address' : address,
        'email' : email,
        'phoneNumber' : phoneNumber
    }
    clients.append(newClient)
    clientId += 1

# Buscar cliente por ID
def search_client(client_id):
    for client in clients:
        if client['Id'] == client_id:
            return client
    return None

#Buscar cliente por Nombre
def search_client_by_name(name):
    # Crear una lista para almacenar clientes que coincidan con el nombre
    matching_clients = []
    
    for client in clients:
        # Comparar el nombre proporcionado con el nombre del cliente en la lista
        if client['name'].lower() == name.lower():
            matching_clients.append(client)
    
    # Retornar la lista de clientes que coinciden con el nombre proporcionado
    return matching_clients

# Actualizar cliente
def update_client(client_id, name=None, address=None, email=None, phoneNumber=None):
    client = search_client(client_id)
    if client:
        if name is not None:
            client['name'] = name
        if address is not None:
            client['address'] = address
        if email is not None:
            client['email'] = email
        if phoneNumber is not None:
            client['phoneNumber'] = phoneNumber
        return True
    return False

# Eliminar cliente
def delete_client(client_id):
    global clients
    clients = [client for client in clients if client['Id'] != client_id]




def createRoom(roomNumber):
    global roomId
    newRoom = {
        'Id' : roomId,
        'roomNumber' : roomNumber,
        'state' : "Libre"
    }
    rooms.append(newRoom)
    roomId += 1

# Buscar habitación por ID
def search_room_by_id(roomId):
    for room in rooms:
        if room['Id'] == roomId:
            return room
    return None

#Buscar habitacion por nombre
def search_room_by_roomNumber(roomNumber):
    for room in rooms:
        if room['roomNumber'] == roomNumber:
            return room
    return None

# Actualizar habitación
def update_room(roomId, roomNumber=None, state=None):
    room = search_room_by_id(roomId)
    if room:
        if roomNumber is not None:
            room['roomNumber'] = roomNumber
        if state is not None:
            room['state'] = state
        return True
    return False




def createReservation(clientId, roomId, reservationDate, reservationHour, leaveDate, price):
    global reservationId
    newReservation = {
        'Id': reservationId,
        'clientId': int(clientId),  # Asegurarse de que sea entero
        'roomId': roomId,
        'reservationDate': reservationDate,
        'reservationHour': reservationHour,
        'leaveDate': leaveDate,
        'price': price
    }
    reservations.append(newReservation)
    update_room(roomId, None, "Reservado")
    reservationId += 1

# Buscar reserva por ID
def search_reservation(reservation_id):
    for reservation in reservations:
        if reservation['Id'] == reservation_id:
            return reservation
    return None

def search_reservation_by_client_name(client_name):
    matching_clients = search_client_by_name(client_name)
    matching_reservations = []

    for client in matching_clients:
        for reservation in reservations:
            if reservation['clientId'] == client['Id']:  # Ensure clientId is correctly matched
                matching_reservations.append(reservation)
    return matching_reservations

# Actualizar reserva
def update_reservation(reservation_id, clientId=None, roomId=None, reservationDate=None, reservationHour=None, leaveDate=None, price=None):
    reservation = search_reservation(reservation_id)
    if reservation:
        if clientId is not None:
            reservation['clientId'] = int(clientId)  # Ensure clientId is an integer
        if roomId is not None:
            reservation['roomId'] = roomId
        if reservationDate is not None:
            reservation['reservationDate'] = reservationDate
        if reservationHour is not None:
            reservation['reservationHour'] = reservationHour
        if leaveDate is not None:
            reservation['leaveDate'] = leaveDate
        if price is not None:
            reservation['price'] = price
        return True
    return False

# Eliminar reserva
def delete_reservation(reservation_id):
    global reservations
    reservation = search_reservation(reservation_id)
    if reservation:
        # Poner en estado libre la habitación al eliminar la reservación
        update_room(int(reservation['roomId']), None, "Libre")
        reservations = [res for res in reservations if res['Id'] != reservation_id]
        return True
    return False

def create_client_interface(root):
    # Marco principal
    client_frame = ttk.Frame(root)
    client_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    
    # Variables para los campos de texto
    id_var = tk.StringVar()
    name_var = tk.StringVar()
    address_var = tk.StringVar()
    email_var = tk.StringVar()
    phone_var = tk.StringVar()

    # Función para buscar cliente por ID
    def search_client_by_id():
        global editing_mode
        try:
            client_id = int(id_var.get())  # Obtenemos el ID ingresado
            client = search_client(client_id)  # Usamos la función de búsqueda
            if client:
                name_var.set(client['name'])
                address_var.set(client['address'])
                email_var.set(client['email'])
                phone_var.set(client['phoneNumber'])
                editing_mode = True
            else:
                messagebox.showinfo("No encontrado", "Cliente no encontrado")
                editing_mode = False
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero")

    # Función para deshabilitar elementos cuando se presiona "Nuevo"
    def disable_elements():
        id_label.config(state="disabled")
        id_entry.config(state="disabled")
        search_button.config(state="disabled")
        new_button.config(state="disabled")
        edit_button.config(state="disabled")
        delete_button.config(state="disabled")

    # Función para habilitar elementos cuando se presiona "Cancelar"
    def enable_elements():
        id_label.config(state="normal")
        id_entry.config(state="normal")
        search_button.config(state="normal")
        new_button.config(state="normal")
        edit_button.config(state="normal")
        delete_button.config(state="normal")

    # Función para validar los datos del cliente
    def validate_data(name, address, phone, email):
        global editing_mode
        client_registered = search_client_by_name(name)
        if(editing_mode):
            if len(name) > 50 or name == "":
                return "El nombre no puede exceder los 50 caracteres ni estar vacio."
            if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+ # \d+$', address):
                return "La dirección debe estar conformada por: 'nombre de calle # numero de calle'."
            if not re.match(r'^\+\d{12}$', phone):
                return "El teléfono debe ser númerico, tener 13 caracteres e iniciar con '+'."
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return "El correo electrónico no tiene un formato válido (variable@example.com)."
        else:
            if client_registered:
                if client_registered[0]['email'] == email or client_registered[0]['phoneNumber'] == phone:
                    return "Los datos del cliente ya han sido registrados para otro cliente."
            if len(name) > 50 or name == "":
                return "El nombre no puede exceder los 50 caracteres ni estar vacio."
            if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+ # \d+$', address):
                return "La dirección debe estar conformada por: 'nombre de calle # numero de calle'."
            if not re.match(r'^\+\d{12}$', phone):
                return "El teléfono debe ser númerico, tener 13 caracteres e iniciar con '+'."
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return "El correo electrónico no tiene un formato válido (variable@example.com)."
        return None
    
     # Función para el botón "Nuevo"
    def on_new():
        disable_elements()
        global editing_mode
        editing_mode = False
        # Limpiar campos
        id_var.set('')
        name_var.set('')
        address_var.set('')
        email_var.set('')
        phone_var.set('')

    # Función para el botón "Cancelar"
    def on_cancel():
        enable_elements()
        global editing_mode
        editing_mode = False
        # Limpiar campos
        id_var.set('')
        name_var.set('')
        address_var.set('')
        email_var.set('')
        phone_var.set('')

    # Función para el botón "Salvar"
    def on_save():
        name = name_var.get()
        address = address_var.get()
        phone = phone_var.get()
        email = email_var.get()
        
        error_message = validate_data(name, address, phone, email)
        if error_message:
            messagebox.showerror("Error de validación", error_message)
            return
        
        if editing_mode:
            client_id = int(id_var.get())
            if update_client(client_id, name, address, email, phone):
                messagebox.showinfo("Éxito", "Cliente actualizado exitosamente")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el cliente")
        else:
            createClient(name, address, email, phone)
            messagebox.showinfo("Éxito", "Cliente guardado exitosamente")
        
        enable_elements()
        id_var.set('')
        name_var.set('')
        address_var.set('')
        email_var.set('')
        phone_var.set('')

    # Función para el botón "Editar"
    def on_edit():
        global editing_mode
        if not editing_mode:
            messagebox.showwarning("Advertencia", "Primero busque un cliente para editar.")
            return
        
        disable_elements()
        save_button.config(state="normal")
        cancel_button.config(state="normal")
        
        # Permitir modificaciones en los campos de texto
        id_entry.config(state="disabled")
        search_button.config(state="disabled")
        new_button.config(state="disabled")
        edit_button.config(state="disabled")
        delete_button.config(state="disabled")
    
    # Función para el botón "Eliminar"
    def on_delete():
        if not editing_mode:
            messagebox.showwarning("Advertencia", "Primero busque un cliente para eliminar.")
            return
        
        client_id = int(id_var.get())
        delete_client(client_id)
        messagebox.showinfo("Éxito", "Cliente eliminado exitosamente")
        enable_elements()
        id_var.set('')
        name_var.set('')
        address_var.set('')
        email_var.set('')
        phone_var.set('')
        
    # Primera fila
    id_label = ttk.Label(client_frame, text="Ingrese Id del Cliente:")
    id_label.grid(row=0, column=0, sticky="e")
    id_entry = ttk.Entry(client_frame, textvariable=id_var)
    id_entry.grid(row=0, column=1, padx=5)
    search_button = ttk.Button(client_frame, text="Buscar", command=search_client_by_id)
    search_button.grid(row=0, column=2, padx=5)

    # Segunda fila (ID)
    ttk.Label(client_frame, text="ID:").grid(row=1, column=0, sticky="e")
    id_entry_show = ttk.Entry(client_frame, textvariable=id_var, state="disabled")
    id_entry_show.grid(row=1, column=1, padx=5)

    # Tercera fila (Nombre y Email)
    ttk.Label(client_frame, text="Nombre:").grid(row=2, column=0, sticky="e")
    ttk.Entry(client_frame, textvariable=name_var).grid(row=2, column=1, padx=5)
    client_frame.grid_columnconfigure(2, minsize=20)  # Espaciado
    ttk.Label(client_frame, text="Email:").grid(row=2, column=3, sticky="e")
    ttk.Entry(client_frame, textvariable=email_var).grid(row=2, column=4, padx=5)

    # Cuarta fila (Dirección)
    ttk.Label(client_frame, text="Dirección:").grid(row=3, column=0, sticky="e")
    ttk.Entry(client_frame, textvariable=address_var).grid(row=3, column=1, padx=5)

    # Quinta fila (Teléfono)
    ttk.Label(client_frame, text="Teléfono:").grid(row=4, column=0, sticky="e")
    ttk.Entry(client_frame, textvariable=phone_var).grid(row=4, column=1, padx=5)

    # Sexta fila - Botones
    button_frame = ttk.Frame(client_frame)
    button_frame.grid(row=5, column=0, columnspan=5, pady=10)
    
    new_button = ttk.Button(button_frame, text="Nuevo", command=on_new)
    new_button.grid(row=0, column=0, padx=5)
    
    save_button = ttk.Button(button_frame, text="Salvar", command=on_save)
    save_button.grid(row=0, column=1, padx=5)
    
    cancel_button = ttk.Button(button_frame, text="Cancelar", command=on_cancel)
    cancel_button.grid(row=0, column=2, padx=5)
    
    edit_button = ttk.Button(button_frame, text="Editar", command=on_edit)
    edit_button.grid(row=0, column=3, padx=5)
    
    delete_button = ttk.Button(button_frame, text="Eliminar", command=on_delete)
    delete_button.grid(row=0, column=4, padx=5)

    return client_frame





def create_reservations_interface(root):
    # Marco principal
    reservations_frame = ttk.Frame(root)
    reservations_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    
    # Variables para almacenar los datos de las reservaciones
    client_name_var = tk.StringVar()
    reservation_id_var = tk.StringVar()
    reservation_room_entry_var = tk.StringVar()
    reservation_date_entry_var = tk.StringVar()
    reservation_status_combobox_var = tk.StringVar()
    client_id_combobox_var = tk.StringVar()
    room_id_combobox_var = tk.StringVar()
    
    # Función para buscar la reservación por el nombre del cliente
    def search_reservation():
        global editing_mode
        client_name = client_name_var.get()
        matching_reservations = search_reservation_by_client_name(client_name)

        if matching_reservations:
            # Asumimos que solo mostramos la primera reserva encontrada
            reservation = matching_reservations[0]
            reservation_id_var.set(reservation['Id'])
            reservation_room_entry_var.set(reservation['roomId'])
            reservation_date_entry_var.set(reservation['reservationDate'])
            reservation_status_combobox_var.set("Reservado")  # Asumiendo que el estado es "Reservado"
            client_id_combobox_var.set(reservation['clientId'])
            room_id_combobox_var.set(reservation['roomId'])
            reservation_hour_entry.delete(0, tk.END)
            reservation_hour_entry.insert(0, reservation['reservationHour'])
            leave_date_entry.delete(0, tk.END)
            leave_date_entry.insert(0, reservation['leaveDate'])
            price_entry.delete(0, tk.END)
            price_entry.insert(0, reservation['price'])
            editing_mode = True
        else:
            clear_reservation_fields()
            messagebox.showinfo("Reservación no encontrada",
                                f"No se encontró una reservación para el cliente: {client_name}")
            editing_mode = False

    def on_edit_reservation():
        global editing_mode
        if not editing_mode:
            messagebox.showwarning("Advertencia", "Primero busque una reservación para editar.")
            return

        disable_reservation_buttons()
        reserve_button.config(state="normal")
        cancel_button.config(state="normal")

    # Función para limpiar los campos de texto
    def clear_reservation_fields():
        reservation_id_var.set("")
        reservation_room_entry_var.set("")
        reservation_date_entry_var.set("")
        reservation_status_combobox_var.set("")
        client_name_var.set("")
        client_id_combobox_var.set("")
        room_id_combobox_var.set("")
        reservation_hour_entry.delete(0, tk.END)  # Limpiar campo de hora de reservación
        leave_date_entry.delete(0, tk.END)  # Limpiar campo de fecha de salida
        price_entry.delete(0, tk.END)  # Limpiar campo de costo
    
    # Función para deshabilitar botones y campos
    def disable_reservation_buttons():
        client_name_entry.config(state="disabled")
        search_button.config(state="disabled")
        new_button.config(state="disabled")
        edit_button.config(state="disabled")

    def on_cancel_reservation():
        clear_reservation_fields()
        enable_reservation_buttons()
    
    # Función para habilitar botones y campos
    def enable_reservation_buttons():
        client_name_entry.config(state="normal")
        search_button.config(state="normal")
        new_button.config(state="normal")
        edit_button.config(state="normal")
    
    # Función para manejar el botón "Nueva Reservación"
    def new_reservation():
        disable_reservation_buttons()
        update_comboboxes()  # Actualiza los ComboBox después de deshabilitar los botones

    # Función para actualizar los ComboBox de IDs
    def update_comboboxes():
        # Actualiza el combo box de IDs de clientes
        client_ids = [client['Id'] for client in clients] if clients else []
        client_id_combobox['values'] = client_ids
        
        # Actualiza el combo box de IDs de habitaciones
        room_ids = [room['Id'] for room in rooms] if rooms else []
        room_id_combobox['values'] = room_ids

    # Función para crear una nueva reservación
    def create_reservation():
        global editing_mode
        try:
            if not client_id_combobox_var.get().isdigit():
                raise ValueError("El ID del cliente debe ser un número entero.")
            if not room_id_combobox_var.get().isdigit():
                raise ValueError("El ID de la habitación debe ser un número entero.")

            client_id = client_id_combobox_var.get()
            room_id = room_id_combobox_var.get()
            reservation_date = reservation_date_entry_var.get()
            reservation_hour = reservation_hour_entry.get()
            leave_date = leave_date_entry.get()
            price = price_entry.get()

            room = search_room_by_id(int(room_id))
            if room and room['state'] == "Reservado" and not editing_mode:
                messagebox.showerror("Error", "La habitación no está libre.")
                return

            error_message = validate_reservation(reservation_date, reservation_hour, leave_date, price)
            if error_message:
                messagebox.showerror("Error de validación", error_message)
                return

            if editing_mode:
                reservation_id = int(reservation_id_var.get())
                if update_reservation(reservation_id, client_id, room_id, reservation_date, reservation_hour,
                                      leave_date, price):
                    messagebox.showinfo("Éxito", "Reservación actualizada exitosamente")
                else:
                    messagebox.showerror("Error", "No se pudo actualizar la reservación")
                editing_mode = False
            else:
                createReservation(client_id, room_id, reservation_date, reservation_hour, leave_date, price)
                update_room(int(room_id), None, "Reservado")
                messagebox.showinfo("Éxito", "Reservación guardada exitosamente")

            clear_reservation_fields()
            enable_reservation_buttons()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la reservación: {e}")

    def validate_reservation(reservation_date, reservation_hour, leave_date, price):
        date_regex = r"^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/(\d{4})$"
        hour_regex = r"([01][0-9]|2[0-3]):[0-5][0-9]"
        price_regex = r"^\d+(\.\d{1,2})?$"


        if not re.match(date_regex, reservation_date):
            return "La fecha de reservación no tiene un formato válido (MM/DD/YYYY)."
        if not re.match(date_regex, leave_date):
            return "La fecha de salida no tiene un formato válido (MM/DD/YYYY)."
        if not re.match(hour_regex, reservation_hour):
            return "La hora no tiene un formato válido (HH:MM)."
        if not re.match(price_regex, price):
            return "El precio debe ser un número válido."

        # Conversión de fechas para comparación
        reservation_date_obj = datetime.strptime(reservation_date, "%m/%d/%Y")
        leave_date_obj = datetime.strptime(leave_date, "%m/%d/%Y")

        # Comprobación de que la fecha de salida es mayor a la de entrada
        if leave_date_obj <= reservation_date_obj:
            return "La fecha de salida debe ser mayor que la fecha de reservación."

        return None

    def cancel_reservation():
        try:
            reservation_id = int(reservation_id_var.get())
            if delete_reservation(reservation_id):
                messagebox.showinfo("Éxito", "Reservación cancelada exitosamente")
                clear_reservation_fields()
                enable_reservation_buttons()
            else:
                messagebox.showerror("Error", "No se pudo cancelar la reservación")
        except ValueError:
            messagebox.showerror("Error", "El ID de la reservación debe ser un número entero")

    # Primera fila
    ttk.Label(reservations_frame, text="Ingrese Reservación:").grid(row=0, column=0, sticky="e")
    client_name_entry = ttk.Entry(reservations_frame, textvariable=client_name_var)
    client_name_entry.grid(row=0, column=1, padx=5)
    
    search_button = ttk.Button(reservations_frame, text="Buscar Reservación", command=search_reservation)
    search_button.grid(row=0, column=2, padx=5)

    # Segunda fila
    ttk.Label(reservations_frame, text="Reservación ID:").grid(row=1, column=0, sticky="e")
    reservation_id_entry = ttk.Entry(reservations_frame, textvariable=reservation_id_var, state="disabled")
    reservation_id_entry.grid(row=1, column=1, padx=5)
    reservations_frame.grid_columnconfigure(2, minsize=20)
    ttk.Label(reservations_frame, text="Fecha Reservación(MM/DD/YYYY):").grid(row=1, column=3, sticky="e")
    reservation_date_entry = ttk.Entry(reservations_frame, textvariable=reservation_date_entry_var)
    reservation_date_entry.grid(row=1, column=4, padx=5)

    # Tercera fila
    ttk.Label(reservations_frame, text="Cliente ID:").grid(row=2, column=0, sticky="e")
    client_id_combobox = ttk.Combobox(reservations_frame, textvariable=client_id_combobox_var)
    client_id_combobox.grid(row=2, column=1, padx=5)
    reservations_frame.grid_columnconfigure(3, minsize=20)
    ttk.Label(reservations_frame, text="Fecha Salida(MM/DD/YYYY):").grid(row=2, column=3, sticky="e")
    leave_date_entry = ttk.Entry(reservations_frame)  # Añadido para fecha de salida
    leave_date_entry.grid(row=2, column=4, padx=5)

    # Cuarta fila
    ttk.Label(reservations_frame, text="Habitación ID:").grid(row=3, column=0, sticky="e")
    room_id_combobox = ttk.Combobox(reservations_frame, textvariable=room_id_combobox_var)
    room_id_combobox.grid(row=3, column=1, padx=5)
    reservations_frame.grid_columnconfigure(3, minsize=20)
    ttk.Label(reservations_frame, text="Hora Reservación(HH:MM):").grid(row=3, column=3, sticky="e")
    reservation_hour_entry = ttk.Entry(reservations_frame)  # Añadido para hora de reservación
    reservation_hour_entry.grid(row=3, column=4, padx=5)

    # Quinta fila
    ttk.Label(reservations_frame, text="Costo:").grid(row=4, column=0, sticky="e")
    price_entry = ttk.Entry(reservations_frame)  # Añadido para costo
    price_entry.grid(row=4, column=1, padx=5)

    # Sexta fila - Botones
    button_frame = ttk.Frame(reservations_frame)
    button_frame.grid(row=5, column=0, columnspan=5, pady=10)
    
    new_button = ttk.Button(button_frame, text="Nueva Reservación", command=new_reservation)
    new_button.grid(row=0, column=0, padx=5)
    
    reserve_button = ttk.Button(button_frame, text="Reservar", command=create_reservation)
    reserve_button.grid(row=0, column=1, padx=5)

    cancel_button = ttk.Button(button_frame, text="Cancelar Reservación", command=cancel_reservation)
    cancel_button.grid(row=0, column=2, padx=5)
    
    edit_button = ttk.Button(button_frame, text="Editar", command=on_edit_reservation)
    edit_button.grid(row=0, column=3, padx=5)

    cancel_attempt_button = ttk.Button(button_frame, text="Cancelar", command=on_cancel_reservation)
    cancel_attempt_button.grid(row=0, column=4, padx=5)

    # Actualizar los ComboBox al crear la interfaz
    update_comboboxes()

    return reservations_frame


def create_habitacion_interface(root):
    # Marco principal
    habitacion_frame = ttk.Frame(root)
    habitacion_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # Variables para los campos de texto
    room_number_var_search = tk.StringVar()
    room_number_var = tk.StringVar()
    room_id_var = tk.StringVar()
    estado_var = tk.StringVar()

    # Función para validar el número de habitación
    def validate_room_number(value):
        try:
            room_number = int(value)
            if room_number <= 0:
                raise ValueError
            return room_number
        except ValueError:
            messagebox.showerror("Error", "El número de habitación debe ser mayor a cero, ejem.[1,2,3...]")
            return None

    # Función para buscar habitación por número
    def search_room_by_number():
        room_number = validate_room_number(room_number_var_search.get())
        if room_number is not None:
            room = search_room_by_roomNumber(room_number)
            if room:
                room_number_var_search.set('')
                room_id_var.set(room['Id'])
                room_number_var.set(room['roomNumber'])
                estado_var.set(room['state'])
            else:
                messagebox.showinfo("No encontrado", "Habitación no encontrada")
                clear_fields()

    # Función para crear nueva habitación
    def create_new_room():
        room_number = validate_room_number(room_number_var.get())
        if room_number is not None:
            if search_room_by_roomNumber(room_number):
                messagebox.showwarning("Advertencia", "La habitación ya existe")
                return
            createRoom(room_number)
            messagebox.showinfo("Éxito", "Habitación creada exitosamente")
            clear_fields()

    # Función para editar habitación
    def edit_room():
        try:
            room_id = int(room_id_var.get())
            room_number = validate_room_number(room_number_var.get())
            state = estado_var.get()
            if room_number is not None and search_room_by_id(room_id):
                update_room(room_id, room_number, state)
                messagebox.showinfo("Éxito", "Habitación actualizada exitosamente")
                clear_fields()
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero válido")

    # Función para limpiar campos
    def clear_fields():
        room_number_var_search.set('')
        room_number_var.set('')
        room_id_var.set('')
        estado_var.set('Libre')

    # Primera fila
    ttk.Label(habitacion_frame, text="Ingrese Número de Habitación:").grid(row=0, column=0, sticky="e")
    ttk.Entry(habitacion_frame, textvariable=room_number_var_search).grid(row=0, column=1, padx=5)
    ttk.Button(habitacion_frame, text="Buscar", command=search_room_by_number).grid(row=0, column=2, padx=5)

    # Segunda fila
    ttk.Label(habitacion_frame, text="Habitación ID:").grid(row=1, column=0, sticky="e")
    ttk.Entry(habitacion_frame, textvariable=room_id_var, state="disabled").grid(row=1, column=1, padx=5)
    habitacion_frame.grid_columnconfigure(2, minsize=20)  # Espaciado
    ttk.Label(habitacion_frame, text="Seleccione Estado Habitación:").grid(row=1, column=3, sticky="e")
    estado_combobox = ttk.Combobox(habitacion_frame, textvariable=estado_var, values=["Libre", "Reservado", "Cancelado"])
    estado_combobox.grid(row=1, column=4, padx=5)

    # Tercera fila
    ttk.Label(habitacion_frame, text="Número:").grid(row=2, column=0, sticky="e")
    ttk.Entry(habitacion_frame, textvariable=room_number_var).grid(row=2, column=1, padx=5)

    # Cuarta fila - Botones
    button_frame = ttk.Frame(habitacion_frame)
    button_frame.grid(row=3, column=0, columnspan=5, pady=10)

    ttk.Button(button_frame, text="Nueva Habitación", command=create_new_room).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="Editar", command=edit_room).grid(row=0, column=1, padx=5)
    
    return habitacion_frame




def switch_frame(current_frame, new_frame):
    current_frame.grid_forget()  # Oculta el frame actual
    new_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)  # Muestra el nuevo frame
    return new_frame  # Retorna el nuevo frame como el actual

# Función para cambiar de frame
def switch_to_frame(new_frame, button):
    global current_frame, active_button
    current_frame = switch_frame(current_frame, new_frame)
    # Restablece el estilo del botón anterior
    active_button.configure(style="TButton")
    # Aplica el nuevo estilo al botón seleccionado
    button.configure(style="Active.TButton")
    active_button = button

root = tk.Tk()
root.title("Aplicacion Hotelera")

# Crear estilos para los botones
style = ttk.Style()
style.configure("TButton", padding=5)
style.configure("Active.TButton", background="#add8e6", padding=5)

# Marco de las pestañas
tab_frame = ttk.Frame(root)
tab_frame.grid(row=0, column=0, sticky="ew")

# Crear las interfaces
reservaciones_frame = create_reservations_interface(root)
habitacion_frame = create_habitacion_interface(root)
client_frame = create_client_interface(root)

# Botones de pestañas
btn_clientes = ttk.Button(tab_frame, text="Clientes", command=lambda: switch_to_frame(client_frame, btn_clientes))
btn_reservaciones = ttk.Button(tab_frame, text="Reservaciones", command=lambda: switch_to_frame(reservaciones_frame, btn_reservaciones))
btn_habitacion = ttk.Button(tab_frame, text="Habitación", command=lambda: switch_to_frame(habitacion_frame, btn_habitacion))

btn_clientes.grid(row=0, column=0, padx=5)
btn_reservaciones.grid(row=0, column=1, padx=5)
btn_habitacion.grid(row=0, column=2, padx=5)

# Inicializa el frame actual
current_frame = client_frame
active_button = btn_clientes
switch_to_frame(client_frame, btn_clientes)

root.mainloop()
