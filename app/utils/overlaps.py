import json
from typing import Dict
from sqlalchemy.orm import Session
from app.model.user import Allocation

def calculate_fund_overlaps(db: Session) -> Dict:
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

    allocations = db.query(
        Allocation.mutualfund_name,
        Allocation.stock_allocation
    ).all()

    nodes = [{"name": name, "fill": color} for name, color in mutual_fund_colors.items()]
    nodes += [{"name": name, "fill": color} for name, color in stock_colors.items()]

    links = []
    for allocation in allocations:
        fund_name = allocation.mutualfund_name
        stock_allocation = allocation.stock_allocation

        if isinstance(stock_allocation, str):  
            stock_allocation = json.loads(stock_allocation)

        fund_index = next((i for i, node in enumerate(nodes) if node["name"] == fund_name), None)
        if fund_index is None:
            print(f"Skipping unknown fund: {fund_name}")  # Debugging line
            continue  

        for stock_name, allocation_percentage in stock_allocation.items():
            stock_index = next((i for i, node in enumerate(nodes) if node["name"] == stock_name), None)
            if stock_index is None:
                print(f"Skipping unknown stock: {stock_name}")  # Debugging line
                continue  

            links.append({
                "source": fund_index,
                "target": stock_index,
                "value": allocation_percentage,
                "stroke": stock_colors.get(stock_name, "#000000")
            })

    return {"nodes": nodes, "links": links}
