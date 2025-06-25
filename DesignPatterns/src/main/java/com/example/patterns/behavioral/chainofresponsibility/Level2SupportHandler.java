package com.example.patterns.behavioral.chainofresponsibility;

/**
 * Chain of Responsibility Pattern - Concrete Handler
 * Level 2 support handles technical issues
 */
public class Level2SupportHandler extends SupportHandler {
    
    @Override
    public void handleRequest(SupportTicket ticket) {
        System.out.println("\n--- Level 2 Support Processing ---");
        System.out.println("Ticket: " + ticket);
        
        if (canHandle(ticket)) {
            System.out.println("✓ Level 2 Support: Handling ticket " + ticket.getId());
            handleTicket(ticket);
        } else {
            System.out.println("→ Level 2 Support: Cannot handle ticket " + ticket.getId() + 
                             " - escalating to next level");
            passToNext(ticket);
        }
    }
    
    private boolean canHandle(SupportTicket ticket) {
        return (ticket.getType() == SupportTicket.Type.TECHNICAL_ISSUE || 
                ticket.getType() == SupportTicket.Type.GENERAL_INQUIRY) &&
               (ticket.getPriority() == SupportTicket.Priority.LOW || 
                ticket.getPriority() == SupportTicket.Priority.MEDIUM);
    }
    
    private void handleTicket(SupportTicket ticket) {
        System.out.println("  • Analyzing technical logs");
        System.out.println("  • Running diagnostic tests");
        System.out.println("  • Providing technical solution");
        System.out.println("  • Creating knowledge base article");
        System.out.println("  • Ticket " + ticket.getId() + " resolved by Level 2 Support");
    }
}
