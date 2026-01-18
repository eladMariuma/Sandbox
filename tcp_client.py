import socket
import requests

HOST = "127.0.0.1"
PORT = 8000

def recv_line(sock: socket.socket):
    buf = b""
    while '\n' not in buf:
        chunk =  sock.recv(1024)
        if not chunk:
            raise ConnectionError("Connection closed by remote host")
        buf += chunk
    line, rest = buf.split(b"\n", 1)
    return line.decode("utf8")

if __name__ == "__main__":
    try:
        with socket.create_connection((HOST, PORT), timeout=3) as sock:
            sock.sendall("Hello world".encode("utf8"))
            print(recv_line(sock))
    except Exception as e:
        print(e)

    access_token = "SOME_ACCESS_TOKEN"
    with requests.Session() as session:
        session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        })
        data = session.get(f"http://google.com")
        print(f"Data from google {data.content}") # As is <class 'bytes'>
        print(f"Data from google {data.text}") # Try to make it str
        print(f"Data from google {data.headers}") # מידע על המידע
        print(f"Data from google {data.status_code}") # Hopefully 200
        """
        4xx (בעיה בבקשה)

            400 Bad Request = שלחת משהו לא תקין (JSON לא תקין/חסר שדות וכו’)
            
            401 Unauthorized = חסר אימות (למשל אין/לא נכון Authorization)
            
            403 Forbidden = יש אימות אבל אין הרשאה
            
            404 Not Found = לא קיים URL כזה
            
            405 Method Not Allowed = endpoint קיים אבל מתודה לא מתאימה (POST במקום GET)
            
            429 Too Many Requests = יותר מדי בקשות (Rate limit)
            
            5xx (בעיה בשרת)
            
            500 = שגיאה כללית בשרת
            
            502 = gateway/proxy בעיה (למשל Cloud Run מאחורי proxy)
            
            503 = השרת זמנית לא זמין / עומס
            
            504 = timeout בדרך לשרת
        """
