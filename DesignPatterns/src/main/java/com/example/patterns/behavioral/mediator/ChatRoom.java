package com.example.patterns.behavioral.mediator;

import java.util.ArrayList;
import java.util.List;

/**
 * Mediator Pattern - Concrete Mediator
 * Chat room that manages communication between users
 */
public class ChatRoom implements ChatMediator {
    private List<User> users;
    private String roomName;
    
    public ChatRoom(String roomName) {
        this.roomName = roomName;
        this.users = new ArrayList<>();
    }
    
    @Override
    public void addUser(User user) {
        users.add(user);
        System.out.println(user.getName() + " joined the chat room: " + roomName);
        notifyUsers(user.getName() + " has joined the chat", user);
    }
    
    @Override
    public void removeUser(User user) {
        users.remove(user);
        System.out.println(user.getName() + " left the chat room: " + roomName);
        notifyUsers(user.getName() + " has left the chat", user);
    }
    
    @Override
    public void sendMessage(String message, User user) {
        System.out.println("\n[" + roomName + "] " + user.getName() + ": " + message);
        
        // Send message to all other users
        for (User u : users) {
            if (u != user) {
                u.receive(message, user.getName());
            }
        }
    }
    
    @Override
    public void notifyUsers(String message, User excludeUser) {
        System.out.println("\n[" + roomName + " - System]: " + message);
        
        for (User u : users) {
            if (u != excludeUser) {
                u.receive("[System] " + message, "System");
            }
        }
    }
    
    public void broadcastSystemMessage(String message) {
        System.out.println("\n[" + roomName + " - Admin]: " + message);
        
        for (User u : users) {
            u.receive("[Admin] " + message, "Admin");
        }
    }
    
    public List<User> getUsers() {
        return new ArrayList<>(users);
    }
    
    public String getRoomName() {
        return roomName;
    }
    
    public int getUserCount() {
        return users.size();
    }
}
