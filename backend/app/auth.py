from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import bcrypt
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXP_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(HASH_ALGORITHM), bcrypt.gensalt()).decode(HASH_ALGORITHM)

def check_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(HASH_ALGORITHM), hashed.encode(HASH_ALGORITHM))

def create_access_token(data: dir)-> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXP_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return payload.get("sub")

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
    ) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        user_id = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user