package com.example.patterns.behavioral.chainofresponsibility;

/**
 * Chain of Responsibility Pattern - Concrete Handler
 * Level 3 support handles complex and high-priority issues
 */
public class Level3SupportHandler extends SupportHandler {
    
    @Override
    public void handleRequest(SupportTicket ticket) {
        System.out.println("\n--- Level 3 Support Processing ---");
        System.out.println("Ticket: " + ticket);
        
        if (canHandle(ticket)) {
            System.out.println("✓ Level 3 Support: Handling ticket " + ticket.getId());
            handleTicket(ticket);
        } else {
            System.out.println("→ Level 3 Support: Cannot handle ticket " + ticket.getId() + 
                             " - escalating to next level");
            passToNext(ticket);
        }
    }
    
    private boolean canHandle(SupportTicket ticket) {
        return (ticket.getType() == SupportTicket.Type.TECHNICAL_ISSUE ||
                ticket.getType() == SupportTicket.Type.BILLING_ISSUE) &&
               (ticket.getPriority() == SupportTicket.Priority.HIGH ||
                ticket.getPriority() == SupportTicket.Priority.MEDIUM);
    }
    
    private void handleTicket(SupportTicket ticket) {
        System.out.println("  • Conducting deep system analysis");
        System.out.println("  • Coordinating with development team");
        System.out.println("  • Implementing complex solution");
        System.out.println("  • Scheduling follow-up calls");
        System.out.println("  • Ticket " + ticket.getId() + " resolved by Level 3 Support");
    }
}
