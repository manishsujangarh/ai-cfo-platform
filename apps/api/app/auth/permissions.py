from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.organization_members.repository import get_membership


def require_role(*roles):
    def dependency(
        organization_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
    ):
        membership = get_membership(
            db,
            organization_id,
            current_user.id,
        )

        if membership is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not a member",
            )

        if membership.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        return membership

    return dependency