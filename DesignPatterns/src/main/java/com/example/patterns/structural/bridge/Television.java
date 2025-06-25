package com.example.patterns.structural.bridge;

/**
 * Concrete implementation - Television
 */
public class Television implements Device {
    private boolean on = false;
    private int volume = 30;
    private int channel = 1;

    @Override
    public boolean isEnabled() {
        return on;
    }

    @Override
    public void enable() {
        on = true;
        System.out.println("Television is now ON");
    }

    @Override
    public void disable() {
        on = false;
        System.out.println("Television is now OFF");
    }

    @Override
    public int getVolume() {
        return volume;
    }

    @Override
    public void setVolume(int volume) {
        if (volume > 100) {
            this.volume = 100;
        } else if (volume < 0) {
            this.volume = 0;
        } else {
            this.volume = volume;
        }
        System.out.println("TV Volume set to " + this.volume);
    }

    @Override
    public int getChannel() {
        return channel;
    }

    @Override
    public void setChannel(int channel) {
        this.channel = channel;
        System.out.println("TV Channel set to " + channel);
    }

    @Override
    public void printStatus() {
        System.out.println("------------------------------------");
        System.out.println("| Television Status:");
        System.out.println("| Power: " + (on ? "ON" : "OFF"));
        System.out.println("| Volume: " + volume + "%");
        System.out.println("| Channel: " + channel);
        System.out.println("------------------------------------");
    }
}
