from email import message
import requests
import smtplib 
from datetime import datetime
import time
# Coordinates of Maltepe/İstanbul 

LOCAL_DIFF = 3
MY_LAT =-50.0730
MY_LONG = 120.5299
message_positive = " Passing through your location. You can look up to sky. "
message_negative = " No need to check , You cant see now . "
def send_mail(message) : 
    my_email = "mctwebd@gmail.com"      
    my_password = input(f"input your password for {my_email} : ")
    with smtplib.SMTP("smtp.gmail.com",port=587) as connector:
        connector.starttls()   
        connector.login(user=my_email,password=my_password)
        connector.sendmail(
            from_addr= my_email,
            to_addrs= ["can.tanriverdi01@gmail.com" ,"pinarcokugras@gmail.com"],
            msg=f"Subject:Iss Location alert ! \n\n {message} " 
        ) 
def iss_locations(): 
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])  
    iss_longitude = float(data["iss_position"]["longitude"])
    return (iss_latitude+5,iss_latitude-5,iss_longitude+5,iss_longitude-5)
#Your position is within +5 or -5 degrees of the ISS position.
def day_time(): 
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + LOCAL_DIFF # +3 converts UTC to istanbul local
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + LOCAL_DIFF
    return (sunrise,sunset)
time_now = datetime.now()


sun_tuple = day_time()   
sunrise = sun_tuple[0]
sunset = sun_tuple[1]
time_now = datetime.now() 
position_tuple = iss_locations()
latitude_status  = MY_LAT <= position_tuple[0] and MY_LAT >= position_tuple[1] 
longitude_status = MY_LONG <= position_tuple[2] and MY_LONG >= position_tuple[3] 
print(latitude_status)
print(longitude_status)
current_hour = int(time_now.hour)
if latitude_status == True and longitude_status == True : 
    print("here")
    print(sunset)
    print(sunrise)
    print(current_hour >= sunset or current_hour <= sunrise)
    if current_hour >= sunset or current_hour <= sunrise : 
        print("herehere")
        send_mail(message_positive)
else : 
    send_mail(message_negative)







