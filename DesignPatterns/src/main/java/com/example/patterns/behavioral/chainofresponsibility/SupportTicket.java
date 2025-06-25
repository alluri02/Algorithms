package com.example.patterns.behavioral.chainofresponsibility;

/**
 * Chain of Responsibility Pattern - Request object
 * Represents a support ticket that needs to be handled
 */
public class SupportTicket {
    public enum Priority {
        LOW, MEDIUM, HIGH, CRITICAL
    }
    
    public enum Type {
        GENERAL_INQUIRY, TECHNICAL_ISSUE, BILLING_ISSUE, SECURITY_INCIDENT
    }
    
    private String id;
    private String description;
    private Priority priority;
    private Type type;
    private String customerName;
    
    public SupportTicket(String id, String description, Priority priority, Type type, String customerName) {
        this.id = id;
        this.description = description;
        this.priority = priority;
        this.type = type;
        this.customerName = customerName;
    }
    
    // Getters
    public String getId() { return id; }
    public String getDescription() { return description; }
    public Priority getPriority() { return priority; }
    public Type getType() { return type; }
    public String getCustomerName() { return customerName; }
    
    @Override
    public String toString() {
        return "Ticket[" + id + "] - " + type + " (" + priority + "): " + description + 
               " [Customer: " + customerName + "]";
    }
}
