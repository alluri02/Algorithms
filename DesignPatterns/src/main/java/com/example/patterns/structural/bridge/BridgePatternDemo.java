package com.example.patterns.structural.bridge;

/**
 * Bridge Pattern Demo
 * Demonstrates how to separate abstraction from implementation
 */
public class BridgePatternDemo {
    
    public static void demonstrateBridgePattern() {
        System.out.println("=== Bridge Pattern Demo ===");
        
        // Create different devices
        Device tv = new Television();
        Device radio = new Radio();
        
        // Use basic remote with TV
        System.out.println("\n--- Basic Remote with TV ---");
        RemoteControl basicRemote = new RemoteControl(tv) {};
        basicRemote.togglePower();
        basicRemote.volumeUp();
        basicRemote.channelUp();
        
        // Use advanced remote with TV
        System.out.println("\n--- Advanced Remote with TV ---");
        AdvancedRemoteControl advancedRemote = new AdvancedRemoteControl(tv);
        advancedRemote.setChannel(5);
        advancedRemote.displayStatus();
        
        // Switch to radio with same remote
        System.out.println("\n--- Advanced Remote with Radio ---");
        AdvancedRemoteControl radioRemote = new AdvancedRemoteControl(radio);
        radioRemote.togglePower();
        radioRemote.volumeUp();
        radioRemote.mute();
        radioRemote.displayStatus();
        
        System.out.println("\nBridge Pattern allows us to use different remotes with different devices independently!");
    }
    
    public static void main(String[] args) {
        demonstrateBridgePattern();
    }
}
