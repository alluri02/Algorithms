package com.example.patterns.behavioral.mediator;

/**
 * Mediator Pattern - Concrete Colleague
 * Regular chat user
 */
public class RegularUser extends User {
    
    public RegularUser(ChatMediator mediator, String name) {
        super(mediator, name);
    }
    
    @Override
    public void send(String message) {
        System.out.println(name + " is sending: " + message);
        mediator.sendMessage(message, this);
    }
    
    @Override
    public void receive(String message, String fromUser) {
        System.out.println("  → " + name + " received from " + fromUser + ": " + message);
    }
}
