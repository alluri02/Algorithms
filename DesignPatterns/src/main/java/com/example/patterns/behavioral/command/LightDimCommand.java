package com.example.patterns.behavioral.command;

/**
 * Command Pattern - Concrete Command
 * Command to dim light
 */
public class LightDimCommand implements Command {
    private Light light;
    private int newBrightness;
    private int previousBrightness;
    
    public LightDimCommand(Light light, int brightness) {
        this.light = light;
        this.newBrightness = brightness;
    }
    
    @Override
    public void execute() {
        previousBrightness = light.getBrightness();
        light.setBrightness(newBrightness);
    }
    
    @Override
    public void undo() {
        light.setBrightness(previousBrightness);
    }
    
    @Override
    public String getDescription() {
        return "Set " + light.getLocation() + " light brightness to " + newBrightness + "%";
    }
}
