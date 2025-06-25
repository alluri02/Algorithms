package com.example.patterns.behavioral.chainofresponsibility;

/**
 * Chain of Responsibility Pattern - Concrete Handler
 * Level 1 support handles basic inquiries
 */
public class Level1SupportHandler extends SupportHandler {
    
    @Override
    public void handleRequest(SupportTicket ticket) {
        System.out.println("\n--- Level 1 Support Processing ---");
        System.out.println("Ticket: " + ticket);
        
        if (canHandle(ticket)) {
            System.out.println("✓ Level 1 Support: Handling ticket " + ticket.getId());
            handleTicket(ticket);
        } else {
            System.out.println("→ Level 1 Support: Cannot handle ticket " + ticket.getId() + 
                             " - escalating to next level");
            passToNext(ticket);
        }
    }
    
    private boolean canHandle(SupportTicket ticket) {
        return ticket.getType() == SupportTicket.Type.GENERAL_INQUIRY && 
               ticket.getPriority() == SupportTicket.Priority.LOW;
    }
    
    private void handleTicket(SupportTicket ticket) {
        System.out.println("  • Providing general information");
        System.out.println("  • Checking FAQ database");
        System.out.println("  • Sending automated response");
        System.out.println("  • Ticket " + ticket.getId() + " resolved by Level 1 Support");
    }
}
