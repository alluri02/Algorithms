package com.example.patterns.behavioral.command;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for Command Pattern implementation
 */
public class CommandPatternTest {
    
    private Light light;
    private RemoteControl remote;
    
    @BeforeEach
    void setUp() {
        light = new Light("Test Room");
        remote = new RemoteControl(1);
    }
    
    @Test
    void testLightOperations() {
        assertFalse(light.isOn());
        assertEquals(0, light.getBrightness());
        
        light.turnOn();
        assertTrue(light.isOn());
        assertEquals(100, light.getBrightness());
        
        light.setBrightness(50);
        assertTrue(light.isOn());
        assertEquals(50, light.getBrightness());
        
        light.turnOff();
        assertFalse(light.isOn());
        assertEquals(0, light.getBrightness());
    }
    
    @Test
    void testLightCommands() {
        Command lightOn = new LightOnCommand(light);
        Command lightOff = new LightOffCommand(light);
        
        assertFalse(light.isOn());
        
        lightOn.execute();
        assertTrue(light.isOn());
        assertEquals(100, light.getBrightness());
        
        lightOff.execute();
        assertFalse(light.isOn());
        assertEquals(0, light.getBrightness());
    }
    
    @Test
    void testUndoFunctionality() {
        Command lightOn = new LightOnCommand(light);
        Command lightOff = new LightOffCommand(light);
        
        // Initially off
        assertFalse(light.isOn());
        
        // Turn on and undo
        lightOn.execute();
        assertTrue(light.isOn());
        lightOn.undo();
        assertFalse(light.isOn());
        
        // Turn on, then off, then undo off
        lightOn.execute();
        assertTrue(light.isOn());
        lightOff.execute();
        assertFalse(light.isOn());
        lightOff.undo();
        assertTrue(light.isOn());
    }
    
    @Test
    void testDimCommand() {
        Command dimCommand = new LightDimCommand(light, 30);
        
        dimCommand.execute();
        assertTrue(light.isOn());
        assertEquals(30, light.getBrightness());
        
        dimCommand.undo();
        assertFalse(light.isOn());
        assertEquals(0, light.getBrightness());
    }
    
    @Test
    void testRemoteControl() {
        Command lightOn = new LightOnCommand(light);
        Command lightOff = new LightOffCommand(light);
        
        remote.setCommand(0, lightOn, lightOff);
        
        remote.onButtonPressed(0);
        assertTrue(light.isOn());
        
        remote.offButtonPressed(0);
        assertFalse(light.isOn());
        
        remote.undoButtonPressed();
        assertTrue(light.isOn());
    }
    
    @Test
    void testCommandDescription() {
        Command lightOn = new LightOnCommand(light);
        assertNotNull(lightOn.getDescription());
        assertTrue(lightOn.getDescription().contains("Test Room"));
        assertTrue(lightOn.getDescription().contains("ON"));
    }
}
