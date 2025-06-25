package com.example.patterns.behavioral.command;

/**
 * Command Pattern - Concrete Command
 * Command to turn light on
 */
public class LightOnCommand implements Command {
    private Light light;
    private boolean wasOn;
    private int previousBrightness;
    
    public LightOnCommand(Light light) {
        this.light = light;
    }
    
    @Override
    public void execute() {
        wasOn = light.isOn();
        previousBrightness = light.getBrightness();
        light.turnOn();
    }
    
    @Override
    public void undo() {
        if (wasOn) {
            light.setBrightness(previousBrightness);
        } else {
            light.turnOff();
        }
    }
    
    @Override
    public String getDescription() {
        return "Turn " + light.getLocation() + " light ON";
    }
}
