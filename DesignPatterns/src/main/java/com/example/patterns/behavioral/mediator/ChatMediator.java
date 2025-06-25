package com.example.patterns.behavioral.mediator;

/**
 * Mediator Pattern - Mediator interface
 * Defines communication contract between components
 */
public interface ChatMediator {
    void sendMessage(String message, User user);
    void addUser(User user);
    void removeUser(User user);
    void notifyUsers(String message, User excludeUser);
}
