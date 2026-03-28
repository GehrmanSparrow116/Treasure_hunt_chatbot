import uvicorn
import webbrowser

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8000/docs")
    # Using 0.0.0.0 ensures it listens on all interfaces (IPv4)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)