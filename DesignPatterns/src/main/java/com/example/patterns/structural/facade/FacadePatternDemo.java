package com.example.patterns.structural.facade;

/**
 * Facade Pattern Demo
 * Demonstrates how to provide a simplified interface to a complex subsystem
 */
public class FacadePatternDemo {
    
    public static void demonstrateFacadePattern() {
        System.out.println("=== Facade Pattern Demo ===");
        
        // Without facade - complex interaction with subsystems
        System.out.println("\n--- Without Facade (Complex) ---");
        CPU cpu = new CPU();
        Memory memory = new Memory();
        HardDrive hardDrive = new HardDrive();
        
        // Client needs to know all the details
        System.out.println("Manual startup process:");
        cpu.freeze();
        memory.load(0, hardDrive.read(0, 1024));
        cpu.jump(0);
        cpu.execute();
        
        // With facade - simplified interface
        System.out.println("\n--- With Facade (Simplified) ---");
        ComputerFacade computer = new ComputerFacade();
        
        System.out.println("\nSimple operations:");
        computer.start();
        
        System.out.println();
        computer.restart();
        
        System.out.println();
        computer.shutdown();
        
        System.out.println("\nFacade Pattern hides the complexity of the subsystem and provides a simple interface!");
    }
    
    public static void main(String[] args) {
        demonstrateFacadePattern();
    }
}
