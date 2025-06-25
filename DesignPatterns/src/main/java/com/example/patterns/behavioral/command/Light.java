package com.example.patterns.behavioral.command;

/**
 * Command Pattern - Receiver
 * The smart home light that receives commands
 */
public class Light {
    private String location;
    private boolean isOn;
    private int brightness;
    
    public Light(String location) {
        this.location = location;
        this.isOn = false;
        this.brightness = 0;
    }
    
    public void turnOn() {
        isOn = true;
        brightness = 100;
        System.out.println(location + " light is ON (brightness: " + brightness + "%)");
    }
    
    public void turnOff() {
        isOn = false;
        brightness = 0;
        System.out.println(location + " light is OFF");
    }
    
    public void setBrightness(int brightness) {
        if (brightness < 0) brightness = 0;
        if (brightness > 100) brightness = 100;
        
        this.brightness = brightness;
        this.isOn = brightness > 0;
        
        if (isOn) {
            System.out.println(location + " light brightness set to " + brightness + "%");
        } else {
            System.out.println(location + " light is OFF");
        }
    }
    
    public boolean isOn() {
        return isOn;
    }
    
    public int getBrightness() {
        return brightness;
    }
    
    public String getLocation() {
        return location;
    }
}
