from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from secrets import token_urlsafe
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.auth import get_current_user
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import Token, LoginRequest, RegisterRequest
from app.schemas.user import User as UserSchema
from app.services.email import send_verification_email, send_welcome_email

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register(
    user_data: RegisterRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Register a new user and send verification email."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Generate verification token
    verification_token = token_urlsafe(32)
    token_expires = datetime.now(timezone.utc) + timedelta(hours=24)

    # Create new user (inactive until email verified)
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        is_active=False,  # Requires email verification
        is_admin=False,
        email_verified=False,
        verification_token=verification_token,
        verification_token_expires=token_expires
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send verification email in background
    background_tasks.add_task(
        send_verification_email,
        email=new_user.email,
        verification_token=verification_token,
        full_name=new_user.full_name
    )

    return new_user


@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Authenticate a user and return a JWT token."""
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()

    # Verify user exists and password is correct
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if email is verified
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email address before logging in. Check your inbox for the verification link."
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your account has been deactivated. Please contact support."
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserSchema)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information."""
    return current_user


@router.post("/verify-email")
def verify_email(
    token: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Verify user email address with token."""
    # Find user by verification token
    user = db.query(User).filter(User.verification_token == token).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )

    # Check if token has expired
    if user.verification_token_expires and user.verification_token_expires < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token has expired. Please request a new one."
        )

    # Check if already verified
    if user.email_verified:
        return {"message": "Email already verified"}

    # Activate user account
    user.email_verified = True
    user.is_active = True
    user.verification_token = None
    user.verification_token_expires = None

    db.commit()

    # Send welcome email
    background_tasks.add_task(
        send_welcome_email,
        email=user.email,
        full_name=user.full_name
    )

    return {"message": "Email verified successfully. You can now log in."}


@router.post("/resend-verification")
def resend_verification(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Resend verification email."""
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )

    # Generate new verification token
    verification_token = token_urlsafe(32)
    token_expires = datetime.now(timezone.utc) + timedelta(hours=24)

    user.verification_token = verification_token
    user.verification_token_expires = token_expires

    db.commit()

    # Send verification email
    background_tasks.add_task(
        send_verification_email,
        email=user.email,
        verification_token=verification_token,
        full_name=user.full_name
    )

    return {"message": "Verification email sent. Please check your inbox."}


@router.post("/logout")
def logout():
    """Logout endpoint (token invalidation should be handled client-side)."""
    return {"message": "Successfully logged out"}
