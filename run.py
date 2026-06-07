from app import create_app
from app.core.config import Config

app = create_app()



print(Config.SQLALCHEMY_DATABASE_URI)
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
