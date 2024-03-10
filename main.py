import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_sec = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def show(self):
        pass

    def available(self):
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class Reservation:
    def __init__(self, customer, hotel):
        self.customer = customer
        self.hotel = hotel

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here is your booking data:
        Name: {self.customer}
        Hotel name: {self.hotel.name}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration,
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True


class Security(CreditCard):
    def check_password(self, user_password):
        password = df_sec.loc[df_sec["number"] == self.number, "password"].squeeze()
        if password == user_password:
            return True


class Spa:
    def __init__(self, customer, hotel):
        self.customer = customer
        self.hotel = hotel

    def generate(self):
        content = f"""
         Thank you for your SPA reservation!
         Here is your SPA booking data:
         Name: {self.customer}
         Hotel name: {self.hotel.name}
         """
        return content


print(df)
hotel_id = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_id)
if hotel.available():
    credit_card = Security(number="12345678123456")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.check_password(user_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation = Reservation(customer=name, hotel=hotel)
            print(reservation.generate())
            question = input("Do you want to book a spa package? ")
            if question == "yes":
                spa = Spa(customer=name, hotel=hotel)
                print(spa.generate())
        else:
            print("Credit card authentication failed")
    else:
        print("There was a problem with your payment")
else:
    print("Hotel is not free")