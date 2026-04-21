from fastapi import APIRouter

from app.shared.schemas import CreateLeads
from app.shared.database import LeadsModel, SessionDep


leads = APIRouter()




@leads.post("/lead")
async def post_lead(data: CreateLeads, session: SessionDep):
    new_lead = LeadsModel(
        time = data.time,
        name = data.name,
        contact = data.contact,
        text = data.text,
    )
    session.add(new_lead)
    await session.commit()
    await session.refresh(new_lead)
    return {"id": new_lead.id, "status": "ok"}