package com.example.patterns.behavioral.mediator;

/**
 * Mediator Pattern Demo
 * Demonstrates how mediator centralizes complex communications and control logic
 */
public class MediatorPatternDemo {
    
    public static void demonstrateMediatorPattern() {
        System.out.println("=== Mediator Pattern Demo ===");
        
        // Create chat room (mediator)
        ChatRoom chatRoom = new ChatRoom("Design Patterns Discussion");
        
        // Create users (colleagues)
        User alice = new RegularUser(chatRoom, "Alice");
        User bob = new PremiumUser(chatRoom, "Bob");
        User charlie = new RegularUser(chatRoom, "Charlie");
        User helpBot = new BotUser(chatRoom, "HelpBot");
        
        System.out.println("\n--- Users Joining Chat Room ---");
        chatRoom.addUser(alice);
        chatRoom.addUser(bob);
        chatRoom.addUser(charlie);
        chatRoom.addUser(helpBot);
        
        System.out.println("\n--- Regular Chat Messages ---");
        alice.send("Hello everyone! How are you doing?");
        
        bob.send("Hi Alice! I'm doing great. Working on some design patterns.");
        
        charlie.send("Hey all! What design patterns are we discussing today?");
        
        System.out.println("\n--- Bot Interaction ---");
        alice.send("I need help with the Observer pattern");
        
        charlie.send("What's the current /time?");
        
        bob.send("Can you tell me a /joke?");
        
        System.out.println("\n--- Premium User Features ---");
        if (bob instanceof PremiumUser) {
            ((PremiumUser) bob).sendPrivateMessage("Hey Alice, want to discuss the Mediator pattern privately?", alice);
        }
        
        System.out.println("\n--- System Announcements ---");
        chatRoom.broadcastSystemMessage("Reminder: Design patterns workshop starts in 30 minutes!");
        
        System.out.println("\n--- User Leaving ---");
        chatRoom.removeUser(charlie);
        
        alice.send("Goodbye Charlie! See you later.");
        
        System.out.println("\n--- Final Chat Room Status ---");
        System.out.println("Chat Room: " + chatRoom.getRoomName());
        System.out.println("Active Users: " + chatRoom.getUserCount());
        for (User user : chatRoom.getUsers()) {
            System.out.println("  - " + user.getName());
        }
        
        System.out.println("\n--- Mediator Pattern Benefits ---");
        System.out.println("✓ Centralized communication control");
        System.out.println("✓ Loose coupling between components");
        System.out.println("✓ Easy to add new user types");
        System.out.println("✓ Complex interactions simplified");
        
        System.out.println("\nMediator Pattern promotes loose coupling by preventing objects from referring to each other explicitly!");
    }
    
    public static void main(String[] args) {
        demonstrateMediatorPattern();
    }
}
