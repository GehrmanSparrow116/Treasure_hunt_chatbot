import uvicorn
import webbrowser

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8001/docs")
    # Using 127.0.0.1 ensures it listens on the localhost interface
    uvicorn.run("app:app", host="127.0.0.1", port=8001, reload=True)