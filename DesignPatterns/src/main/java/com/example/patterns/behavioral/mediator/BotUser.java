package com.example.patterns.behavioral.mediator;

/**
 * Mediator Pattern - Concrete Colleague
 * Bot user with automated responses
 */
public class BotUser extends User {
    
    public BotUser(ChatMediator mediator, String name) {
        super(mediator, name);
    }
    
    @Override
    public void send(String message) {
        System.out.println("🤖 " + name + " (Bot) is sending: " + message);
        mediator.sendMessage(message, this);
    }
    
    @Override
    public void receive(String message, String fromUser) {
        System.out.println("  → 🤖 " + name + " (Bot) received from " + fromUser + ": " + message);
        
        // Auto-respond to certain keywords
        if (message.toLowerCase().contains("help")) {
            autoRespond("I'm here to help! Available commands: /time, /weather, /joke");
        } else if (message.toLowerCase().contains("/time")) {
            autoRespond("Current time: " + java.time.LocalTime.now());
        } else if (message.toLowerCase().contains("/weather")) {
            autoRespond("Today's weather: Sunny, 25°C");
        } else if (message.toLowerCase().contains("/joke")) {
            autoRespond("Why do programmers prefer dark mode? Because light attracts bugs! 😄");
        }
    }
    
    private void autoRespond(String response) {
        // Simulate thinking time
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        System.out.println("🤖 " + name + " (Bot) auto-responding...");
        mediator.sendMessage(response, this);
    }
}
