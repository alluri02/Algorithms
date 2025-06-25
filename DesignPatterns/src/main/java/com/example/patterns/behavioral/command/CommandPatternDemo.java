package com.example.patterns.behavioral.command;

import java.util.Arrays;

/**
 * Command Pattern Demo
 * Demonstrates command execution, undo, and macro commands
 */
public class CommandPatternDemo {
    
    public static void demonstrateCommandPattern() {
        System.out.println("=== Command Pattern Demo ===");
        
        // Create receiver objects
        Light livingRoomLight = new Light("Living Room");
        Light kitchenLight = new Light("Kitchen");
        Light bedroomLight = new Light("Bedroom");
        
        // Create command objects
        Command livingRoomLightOn = new LightOnCommand(livingRoomLight);
        Command livingRoomLightOff = new LightOffCommand(livingRoomLight);
        Command kitchenLightOn = new LightOnCommand(kitchenLight);
        Command kitchenLightOff = new LightOffCommand(kitchenLight);
        Command bedroomLightDim = new LightDimCommand(bedroomLight, 30);
        
        // Create invoker
        RemoteControl remote = new RemoteControl(3);
        
        // Set commands
        remote.setCommand(0, livingRoomLightOn, livingRoomLightOff);
        remote.setCommand(1, kitchenLightOn, kitchenLightOff);
        remote.setCommand(2, bedroomLightDim, new LightOffCommand(bedroomLight));
        
        System.out.println(remote);
        
        System.out.println("\n--- Basic Command Execution ---");
        remote.onButtonPressed(0);  // Turn on living room light
        remote.onButtonPressed(1);  // Turn on kitchen light
        remote.onButtonPressed(2);  // Dim bedroom light
        
        System.out.println("\n--- Undo Operations ---");
        remote.undoButtonPressed(); // Undo bedroom dim
        remote.undoButtonPressed(); // Undo kitchen light on
        remote.undoButtonPressed(); // Undo living room light on
        
        System.out.println("\n--- Turn Off Lights ---");
        remote.offButtonPressed(0); // Turn off living room light
        remote.offButtonPressed(1); // Turn off kitchen light
        
        System.out.println("\n--- Macro Command Demo ---");
        // Create macro command to turn on all lights
        MacroCommand allLightsOn = new MacroCommand(Arrays.asList(
            new LightOnCommand(livingRoomLight),
            new LightOnCommand(kitchenLight),
            new LightDimCommand(bedroomLight, 75)
        ));
        
        MacroCommand allLightsOff = new MacroCommand(Arrays.asList(
            new LightOffCommand(livingRoomLight),
            new LightOffCommand(kitchenLight),
            new LightOffCommand(bedroomLight)
        ));
        
        System.out.println("Executing 'All Lights On' macro:");
        remote.executeCustomCommand(allLightsOn);
        
        System.out.println("\nUndoing 'All Lights On' macro:");
        remote.undoButtonPressed();
        
        System.out.println("\nExecuting 'All Lights Off' macro:");
        remote.executeCustomCommand(allLightsOff);
        
        System.out.println("\nCommand Pattern allows decoupling invoker from receiver and supports undo operations!");
    }
    
    public static void main(String[] args) {
        demonstrateCommandPattern();
    }
}
