package com.example.patterns.behavioral.mediator;

/**
 * Mediator Pattern - Colleague abstract class
 * Base class for all chat participants
 */
public abstract class User {
    protected ChatMediator mediator;
    protected String name;
    
    public User(ChatMediator mediator, String name) {
        this.mediator = mediator;
        this.name = name;
    }
    
    public abstract void send(String message);
    public abstract void receive(String message, String fromUser);
    
    public String getName() {
        return name;
    }
}
