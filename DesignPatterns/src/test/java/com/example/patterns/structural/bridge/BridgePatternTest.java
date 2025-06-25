package com.example.patterns.structural.bridge;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for Bridge Pattern implementation
 */
public class BridgePatternTest {
    
    private Television tv;
    private Radio radio;
    
    @BeforeEach
    void setUp() {
        tv = new Television();
        radio = new Radio();
    }
    
    @Test
    void testDeviceOperations() {
        // Test TV
        assertFalse(tv.isEnabled());
        assertEquals(50, tv.getVolume());
        assertEquals(1, tv.getChannel());
        
        tv.enable();
        assertTrue(tv.isEnabled());
        
        tv.setVolume(75);
        assertEquals(75, tv.getVolume());
        
        tv.setChannel(5);
        assertEquals(5, tv.getChannel());
        
        // Test Radio
        assertFalse(radio.isEnabled());
        assertEquals(30, radio.getVolume());
        assertEquals(1, radio.getChannel());
        
        radio.enable();
        assertTrue(radio.isEnabled());
    }
    
    @Test
    void testRemoteControlWithDifferentDevices() {
        RemoteControl tvRemote = new RemoteControl(tv) {};
        RemoteControl radioRemote = new RemoteControl(radio) {};
        
        // Test TV remote
        tvRemote.togglePower();
        assertTrue(tv.isEnabled());
        
        tvRemote.volumeUp();
        assertEquals(60, tv.getVolume());
        
        tvRemote.channelUp();
        assertEquals(2, tv.getChannel());
        
        // Test Radio remote
        radioRemote.togglePower();
        assertTrue(radio.isEnabled());
        
        radioRemote.volumeUp();
        assertEquals(40, radio.getVolume());
    }
    
    @Test
    void testAdvancedRemoteControl() {
        AdvancedRemoteControl advancedRemote = new AdvancedRemoteControl(tv);
        
        advancedRemote.togglePower();
        assertTrue(tv.isEnabled());
        
        advancedRemote.setChannel(10);
        assertEquals(10, tv.getChannel());
        
        advancedRemote.mute();
        assertEquals(0, tv.getVolume());
    }
}
