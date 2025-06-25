package com.example.patterns.structural.bridge;

/**
 * Bridge Pattern - Refined Abstraction
 * Advanced remote with additional features
 */
public class AdvancedRemoteControl extends RemoteControl {

    public AdvancedRemoteControl(Device device) {
        super(device);
    }

    public void mute() {
        device.setVolume(0);
        System.out.println("Device muted");
    }

    public void setChannel(int channel) {
        device.setChannel(channel);
        System.out.println("Channel set to: " + channel);
    }

    public void displayStatus() {
        System.out.println("--------------------");
        System.out.println("| Remote Control Status |");
        System.out.println("| Power: " + (device.isEnabled() ? "ON" : "OFF"));
        System.out.println("| Volume: " + device.getVolume() + "%");
        System.out.println("| Channel: " + device.getChannel());
        System.out.println("--------------------");
    }
}
