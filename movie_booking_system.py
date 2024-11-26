import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error


# MySQL Connection Setup
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Your MySQL host
            user='root',  # Your MySQL username
            password='admin',  # Your MySQL password
            database='movie_ticket_booking'
        )
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None


# Fetch available movies
def get_movies():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT movie_id, title FROM movies")
    movies = cursor.fetchall()
    connection.close()
    return movies


# Fetch available shows for a selected movie
def get_shows(movie_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"SELECT show_id, theater_id, show_time, seats_available FROM shows WHERE movie_id = {movie_id}")
    shows = cursor.fetchall()
    connection.close()
    return shows


# User login function
def login_user(username, password):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, username, password, email FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    connection.close()
    return user  # Now returns user_id, username, password, email


# Register a new user
def register_user(username, password, email):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Registration Failed", "Username already exists.")
    else:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
        connection.commit()
        messagebox.showinfo("Registration Success", "User registered successfully!")
    connection.close()


# Booking tickets
def book_ticket(user_id, show_id, number_of_tickets):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT seats_available FROM shows WHERE show_id = %s", (show_id,))
    show = cursor.fetchone()

    if show[0] >= number_of_tickets:
        new_seat_count = show[0] - number_of_tickets
        cursor.execute("UPDATE shows SET seats_available = %s WHERE show_id = %s", (new_seat_count, show_id))
        cursor.execute(
            "INSERT INTO bookings (user_id, show_id, number_of_tickets, booking_time, payment_status) VALUES (%s, %s, %s, NOW(), 'Pending')",
            (user_id, show_id, number_of_tickets))
        connection.commit()
        messagebox.showinfo("Booking Success", "Tickets booked successfully!")
    else:
        messagebox.showerror("Booking Failed", "Not enough seats available.")

    connection.close()


# Main Tkinter GUI
class MovieTicketBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Ticket Booking System")

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.email = tk.StringVar()

        # Create frames for login and registration
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        # Login form elements
        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame, textvariable=self.username)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, textvariable=self.password, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.login_frame, text="Register", command=self.show_register_frame).grid(row=3, column=0, columnspan=2)

        self.register_frame = None

    def login(self):
        user = login_user(self.username.get(), self.password.get())
        if user:
            self.user_id = user[0]  # Store the user_id for further use
            self.current_user_details(user)  # Display username, password, and email
            self.show_movies(self.user_id)  # Pass user_id to show movies
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_register_frame(self):
        # Hide login frame
        self.login_frame.pack_forget()

        # Create registration form
        self.register_frame = tk.Frame(self.root)
        self.register_frame.pack(pady=20)

        tk.Label(self.register_frame, text="Username:").grid(row=0, column=0)
        tk.Entry(self.register_frame, textvariable=self.username).grid(row=0, column=1)

        tk.Label(self.register_frame, text="Password:").grid(row=1, column=0)
        tk.Entry(self.register_frame, textvariable=self.password, show="*").grid(row=1, column=1)

        tk.Label(self.register_frame, text="Email:").grid(row=2, column=0)
        tk.Entry(self.register_frame, textvariable=self.email).grid(row=2, column=1)

        tk.Button(self.register_frame, text="Register", command=self.register).grid(row=3, column=0, columnspan=2)

    def register(self):
        username = self.username.get()
        password = self.password.get()
        email = self.email.get()

        if username and password and email:
            register_user(username, password, email)
            self.register_frame.pack_forget()
            self.login_frame.pack(pady=20)  # Go back to the login screen
        else:
            messagebox.showerror("Registration Failed", "All fields must be filled!")

    def current_user_details(self, user):
        user_id, username, password, email = user

        tk.Label(self.root, text=f"Logged in as: {username}").pack(pady=10)
        tk.Label(self.root, text=f"Password: {password}").pack(pady=10)
        tk.Label(self.root, text=f"Email: {email}").pack(pady=10)

    def show_movies(self, user_id):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        self.user_id = user_id

        tk.Label(self.root, text="Select a Movie").pack(pady=10)

        movies = get_movies()

        self.movie_var = tk.StringVar()
        self.movie_var.set(movies[0][0])

        movie_menu = tk.OptionMenu(self.root, self.movie_var, *[movie[0] for movie in movies])
        movie_menu.pack(pady=10)

        tk.Button(self.root, text="View Shows", command=self.show_shows).pack(pady=10)

    def show_shows(self):
        movie_id = self.movie_var.get()

        shows = get_shows(movie_id)

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Select a Show").pack(pady=10)

        self.show_var = tk.StringVar()
        self.show_var.set(shows[0][0])

        show_menu = tk.OptionMenu(self.root, self.show_var, *[show[0] for show in shows])
        show_menu.pack(pady=10)

        tk.Label(self.root, text="Enter Number of Tickets:").pack(pady=10)

        self.num_tickets = tk.IntVar()
        tk.Entry(self.root, textvariable=self.num_tickets).pack(pady=10)

        tk.Button(self.root, text="Book Tickets", command=self.book_ticket).pack(pady=10)

    def book_ticket(self):
        show_id = self.show_var.get()
        num_tickets = self.num_tickets.get()
        book_ticket(self.user_id, show_id, num_tickets)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieTicketBookingApp(root)
    root.mainloop()
