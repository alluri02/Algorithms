package com.example.patterns.behavioral.chainofresponsibility;

/**
 * Chain of Responsibility Pattern - Concrete Handler
 * Security team handles critical security incidents
 */
public class SecurityTeamHandler extends SupportHandler {
    
    @Override
    public void handleRequest(SupportTicket ticket) {
        System.out.println("\n--- Security Team Processing ---");
        System.out.println("Ticket: " + ticket);
        
        if (canHandle(ticket)) {
            System.out.println("✓ Security Team: Handling ticket " + ticket.getId());
            handleTicket(ticket);
        } else {
            System.out.println("→ Security Team: Cannot handle ticket " + ticket.getId() + 
                             " - escalating to next level");
            passToNext(ticket);
        }
    }
    
    private boolean canHandle(SupportTicket ticket) {
        return ticket.getType() == SupportTicket.Type.SECURITY_INCIDENT ||
               ticket.getPriority() == SupportTicket.Priority.CRITICAL;
    }
    
    private void handleTicket(SupportTicket ticket) {
        System.out.println("  • SECURITY ALERT: Immediate response initiated");
        System.out.println("  • Isolating affected systems");
        System.out.println("  • Conducting security audit");
        System.out.println("  • Implementing security patches");
        System.out.println("  • Notifying stakeholders");
        System.out.println("  • Documenting incident response");
        System.out.println("  • Ticket " + ticket.getId() + " resolved by Security Team");
    }
}
