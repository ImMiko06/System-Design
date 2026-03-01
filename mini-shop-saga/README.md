# Mini Shop - Saga Pattern (Single Service)

This project implements the Saga pattern (orchestration) inside a single Python service for an e-commerce checkout workflow.

## Steps
1. Inventory (reserve) — compensate: release reservation  
2. Payment (charge) — compensate: refund  
3. Shipping (create) — compensate: cancel shipment  

## Rule
Steps execute in order. If any step fails, all previously completed steps are compensated in reverse order.