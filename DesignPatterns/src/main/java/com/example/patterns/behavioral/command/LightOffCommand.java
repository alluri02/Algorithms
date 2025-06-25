package com.example.patterns.behavioral.command;

/**
 * Command Pattern - Concrete Command
 * Command to turn light off
 */
public class LightOffCommand implements Command {
    private Light light;
    private boolean wasOn;
    private int previousBrightness;
    
    public LightOffCommand(Light light) {
        this.light = light;
    }
    
    @Override
    public void execute() {
        wasOn = light.isOn();
        previousBrightness = light.getBrightness();
        light.turnOff();
    }
    
    @Override
    public void undo() {
        if (wasOn) {
            light.setBrightness(previousBrightness);
        }
    }
    
    @Override
    public String getDescription() {
        return "Turn " + light.getLocation() + " light OFF";
    }
}
