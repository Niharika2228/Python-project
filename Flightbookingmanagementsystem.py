
import csv

# Flight Class
class Flight:

    def __init__(self, flight_no, origin,
                 destination, seats, fare):

        self.flight_no = flight_no
        self.origin = origin
        self.destination = destination
        self.seats = int(seats)
        self.fare = float(fare)

    # Display Flight Details
    def display(self):

        print(
            f"{self.flight_no} | "
            f"{self.origin} -> {self.destination} | "
            f"Seats: {self.seats} | "
            f"Fare: Rs. {self.fare:.0f} per seat"
        )

    # Book Seats
    def book_seats(self, count):

        if count < 1:
            return False, "Number of seats must be at least 1."

        if self.seats == 0:
            return False, f"Flight {self.flight_no} is full."

        if count > self.seats:
            return False, (
                f"Only {self.seats} seat(s) available "
                f"on {self.flight_no}."
            )

        self.seats -= count

        total = count * self.fare

        return True, total

    # Cancel Seats
    def cancel_seats(self, count):

        self.seats += count


# Booking Management System
class BookingManager:

    def __init__(self):

        self.flights = []
        self.bookings = []
        self.booking_counter = 1

    # Load Flights from CSV
    def load_flights(self):

        try:

            with open(
                "flights.csv",
                "r",
                newline=""
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:

                    flight = Flight(
                        row["FlightNo"],
                        row["Origin"],
                        row["Destination"],
                        row["Seats"],
                        row["Fare"]
                    )

                    self.flights.append(flight)

            print("Flights loaded successfully.")

        except FileNotFoundError:

            print("Error: flights.csv file not found.")

        except (KeyError, ValueError):

            print("Error: Invalid CSV data.")

    # Search Flights
    def search_flights(self, origin, destination):

        found = False

        for flight in self.flights:

            if (
                flight.origin.lower() == origin.lower()
                and
                flight.destination.lower() == destination.lower()
            ):

                flight.display()
                found = True

        if not found:

            print("No flights found.")

    # Book Flight
    def book_flight(self, flight_no, passenger, seats):

        flight = None

        for f in self.flights:

            if f.flight_no.lower() == flight_no.lower():

                flight = f
                break

        if flight is None:

            print("Flight not found.")
            return

        success, result = flight.book_seats(seats)

        if not success:

            print(result)
            return

        booking_id = "BK" + str(self.booking_counter)

        self.booking_counter += 1

        booking = {
            "id": booking_id,
            "passenger": passenger,
            "flight": flight,
            "seats": seats,
            "total": result
        }

        self.bookings.append(booking)

        print(
            f"Booking confirmed. ID: {booking_id} | "
            f"{passenger} | {flight.flight_no} | "
            f"{seats} seat(s) | "
            f"Total: Rs. {result:.0f} | "
            f"Seats left: {flight.seats}"
        )

    # Cancel Booking
    def cancel_booking(self, booking_id):

        for booking in self.bookings:

            if booking["id"].lower() == booking_id.lower():

                flight = booking["flight"]

                flight.cancel_seats(booking["seats"])

                self.bookings.remove(booking)

                print(
                    f"Booking {booking_id} cancelled. "
                    f"Seats left on {flight.flight_no}: "
                    f"{flight.seats}"
                )

                return

        print("Booking ID not found.")


# Main Program
def main():

    manager = BookingManager()

    manager.load_flights()

    while True:

        print("\n===== FLIGHT BOOKING SYSTEM =====")

        print("1. Search Flights")
        print("2. Book Flight")
        print("3. Cancel Booking")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            origin = input("Enter Origin: ")

            destination = input("Enter Destination: ")

            manager.search_flights(origin, destination)

        elif choice == "2":

            flight_no = input("Enter Flight Number: ")

            passenger = input("Enter Passenger Name: ")

            try:

                seats = int(input("Enter Number of Seats: "))

                manager.book_flight(
                    flight_no,
                    passenger,
                    seats
                )

            except ValueError:

                print("Please enter a valid seat number.")

        elif choice == "3":

            booking_id = input("Enter Booking ID: ")

            manager.cancel_booking(booking_id)

        elif choice == "4":

            print("Thank you for using Flight Booking System.")

            break

        else:

            print("Invalid choice. Please try again.")


if __name__ == "__main__":

    main()
