from typing import List, Dict
from sqlalchemy.orm import Session
from app.model.user import Allocation

def calculate_fund_overlaps(db: Session) -> Dict:
    # Predefined colors for mutual funds and stocks
    mutual_fund_colors = {
        "ICICI Prudential Bluechip Fund": "#ff9800",
        "HDFC Top 100 Fund": "#c2185b",
        "SBI Bluechip Fund": "#2196f3",
        "Axis Bluechip Fund": "#4caf50",
        "Mirae Asset Large Cap Fund": "#ff5722",
    }

    stock_colors = {
        "Reliance Industries": "#008000",
        "HDFC Bank": "#c4a000",
        "TCS": "#00bcd4",
        "Infosys": "#8a2be2",
        "ICICI Bank": "#ff4081",
        "Kotak Mahindra Bank": "#795548",
        "Bajaj Finance": "#ffeb3b",
        "Larsen & Toubro": "#03a9f4",
        "State Bank of India (SBI)": "#9c27b0",
    }

    # Fetch all allocations with mutual fund names and stock allocations
    allocations = db.query(
        Allocation.mutualfund_name,
        Allocation.stock_allocation
    ).all()

    # Create nodes list
    nodes = []
    for fund_name, color in mutual_fund_colors.items():
        nodes.append({"name": fund_name, "fill": color})

    for stock_name, color in stock_colors.items():
        nodes.append({"name": stock_name, "fill": color})

    # Create links list
    links = []
    for allocation in allocations:
        fund_name = allocation.mutualfund_name
        stock_allocation = allocation.stock_allocation

        # Find the index of the mutual fund in the nodes list
        fund_index = next(i for i, node in enumerate(nodes) if node["name"] == fund_name)

        for stock_name, allocation_percentage in stock_allocation.items():
            # Find the index of the stock in the nodes list
            stock_index = next(i for i, node in enumerate(nodes) if node["name"] == stock_name)

            # Add the link
            links.append({
                "source": fund_index,
                "target": stock_index,
                "value": allocation_percentage,
                "stroke": stock_colors[stock_name]
            })

    return {"nodes": nodes, "links": links}