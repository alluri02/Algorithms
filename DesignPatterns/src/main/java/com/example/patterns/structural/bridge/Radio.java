package com.example.patterns.structural.bridge;

/**
 * Concrete implementation - Radio
 */
public class Radio implements Device {
    private boolean on = false;
    private int volume = 50;
    private int channel = 101; // FM frequency

    @Override
    public boolean isEnabled() {
        return on;
    }

    @Override
    public void enable() {
        on = true;
        System.out.println("Radio is now ON");
    }

    @Override
    public void disable() {
        on = false;
        System.out.println("Radio is now OFF");
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
        System.out.println("Radio Volume set to " + this.volume);
    }

    @Override
    public int getChannel() {
        return channel;
    }

    @Override
    public void setChannel(int channel) {
        this.channel = channel;
        System.out.println("Radio Station set to " + channel + " FM");
    }

    @Override
    public void printStatus() {
        System.out.println("------------------------------------");
        System.out.println("| Radio Status:");
        System.out.println("| Power: " + (on ? "ON" : "OFF"));
        System.out.println("| Volume: " + volume + "%");
        System.out.println("| Station: " + channel + " FM");
        System.out.println("------------------------------------");
    }
}
