from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, HttpUrl
import qrcode
from io import BytesIO

app = FastAPI(title="Pokemon Card Dealers Proposal API")

# In-memory store for simplicity; replace with your database in production.
proposals = []

# Pydantic model for proposal data.
class Proposal(BaseModel):
    item_name: str
    sale_link: HttpUrl
    adjustment: float  # Value adjustment (could be positive or negative)
    productsInProposal: list
    
class Product(BaseModel):
    item_name: str
    uniqueID: int  # Unique identifier for each card
    adjustment: float
    ebay_url: HttpUrl
    tcgplayer_url: HttpUrl
    pricecharting_url: HttpUrl

@app.post("/proposals", status_code=status.HTTP_201_CREATED)
def create_proposal(proposal: Proposal):
    # Assign an ID based on list length.
    proposal_data = proposal.dict()
    proposal_data["id"] = len(proposals) + 1
    proposals.append(proposal_data)
    return proposal_data

@app.get("/proposals/{proposal_id}")
def get_proposal(proposal_id: int):
    # Retrieve a proposal by its id.
    for proposal in proposals:
        if proposal["id"] == proposal_id:
            return proposal
    raise HTTPException(status_code=404, detail="Proposal not found")

@app.get("/proposals/{proposal_id}/qrcode")
def get_proposal_qrcode(proposal_id: int):
    # Generate a QR code that encodes the URL to view the proposal details.
    for proposal in proposals:
        if proposal["id"] == proposal_id:
            # Example URL; replace with your actual domain and endpoint.
            proposal_url = f"http://yourdomain.com/proposals/{proposal_id}"
            # Create a QR code using the qrcode library.
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(proposal_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            return StreamingResponse(buf, media_type="image/png")
    raise HTTPException(status_code=404, detail="Proposal not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
