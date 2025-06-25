package com.example.patterns.behavioral.chainofresponsibility;

/**
 * Chain of Responsibility Pattern - Handler interface
 * Defines the interface for handling requests
 */
public abstract class SupportHandler {
    protected SupportHandler nextHandler;
    
    public void setNextHandler(SupportHandler nextHandler) {
        this.nextHandler = nextHandler;
    }
    
    public abstract void handleRequest(SupportTicket ticket);
    
    protected void passToNext(SupportTicket ticket) {
        if (nextHandler != null) {
            nextHandler.handleRequest(ticket);
        } else {
            System.out.println("No handler available for ticket: " + ticket.getId());
            System.out.println("Ticket escalated to management");
        }
    }
}
