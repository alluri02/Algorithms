package com.example.patterns.behavioral.mediator;

/**
 * Mediator Pattern - Concrete Colleague
 * Premium user with additional features
 */
public class PremiumUser extends User {
    
    public PremiumUser(ChatMediator mediator, String name) {
        super(mediator, name);
    }
    
    @Override
    public void send(String message) {
        System.out.println("⭐ " + name + " (Premium) is sending: " + message);
        mediator.sendMessage(message, this);
    }
    
    @Override
    public void receive(String message, String fromUser) {
        System.out.println("  → ⭐ " + name + " (Premium) received from " + fromUser + ": " + message);
    }
    
    // Premium feature: send private message (using mediator)
    public void sendPrivateMessage(String message, User targetUser) {
        System.out.println("⭐ " + name + " (Premium) sending private message to " + targetUser.getName());
        targetUser.receive("[Private] " + message, name);
    }
}
