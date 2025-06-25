package com.example.patterns.structural.bridge;

/**
 * Bridge Pattern - Device Interface (Implementation)
 * Separates abstraction (Remote) from implementation (Device)
 */
public interface Device {
    boolean isEnabled();
    void enable();
    void disable();
    int getVolume();
    void setVolume(int volume);
    int getChannel();
    void setChannel(int channel);
    void printStatus();
}
