package com.example.patterns.behavioral.chainofresponsibility;

/**
 * Chain of Responsibility Pattern Demo
 * Demonstrates how requests are passed through a chain of handlers
 */
public class ChainOfResponsibilityPatternDemo {
    
    public static void demonstrateChainOfResponsibilityPattern() {
        System.out.println("=== Chain of Responsibility Pattern Demo ===");
        
        // Create the chain of handlers
        SupportHandler level1 = new Level1SupportHandler();
        SupportHandler level2 = new Level2SupportHandler();
        SupportHandler level3 = new Level3SupportHandler();
        SupportHandler security = new SecurityTeamHandler();
        
        // Set up the chain
        level1.setNextHandler(level2);
        level2.setNextHandler(level3);
        level3.setNextHandler(security);
        
        // Create various support tickets
        SupportTicket[] tickets = {
            new SupportTicket("TKT-001", "How to reset password?", 
                            SupportTicket.Priority.LOW, SupportTicket.Type.GENERAL_INQUIRY, "John Doe"),
            
            new SupportTicket("TKT-002", "Application crashing on startup", 
                            SupportTicket.Priority.MEDIUM, SupportTicket.Type.TECHNICAL_ISSUE, "Jane Smith"),
            
            new SupportTicket("TKT-003", "Database connection timeout", 
                            SupportTicket.Priority.HIGH, SupportTicket.Type.TECHNICAL_ISSUE, "Bob Johnson"),
            
            new SupportTicket("TKT-004", "Suspicious login attempts detected", 
                            SupportTicket.Priority.CRITICAL, SupportTicket.Type.SECURITY_INCIDENT, "Alice Wilson"),
            
            new SupportTicket("TKT-005", "Billing discrepancy in invoice", 
                            SupportTicket.Priority.MEDIUM, SupportTicket.Type.BILLING_ISSUE, "Mike Brown"),
            
            new SupportTicket("TKT-006", "System completely down", 
                            SupportTicket.Priority.CRITICAL, SupportTicket.Type.TECHNICAL_ISSUE, "Sarah Davis")
        };
        
        // Process each ticket through the chain
        for (SupportTicket ticket : tickets) {
            System.out.println("\n" + "=".repeat(50));
            System.out.println("Processing: " + ticket);
            level1.handleRequest(ticket);
        }
        
        System.out.println("\n" + "=".repeat(50));
        System.out.println("--- Chain of Responsibility Benefits ---");
        System.out.println("✓ Decouples sender from receiver");
        System.out.println("✓ Allows dynamic chain modification");
        System.out.println("✓ Each handler has single responsibility");
        System.out.println("✓ Requests are handled by appropriate level");
        
        System.out.println("\nChain of Responsibility Pattern allows passing requests through a chain of handlers!");
    }
    
    public static void main(String[] args) {
        demonstrateChainOfResponsibilityPattern();
    }
}
