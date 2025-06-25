package com.example.patterns.structural.facade;

/**
 * Facade Pattern - Facade class
 * Provides a simplified interface to the complex subsystem
 */
public class ComputerFacade {
    private CPU cpu;
    private Memory memory;
    private HardDrive hardDrive;
    
    public ComputerFacade() {
        this.cpu = new CPU();
        this.memory = new Memory();
        this.hardDrive = new HardDrive();
    }
    
    public void start() {
        System.out.println("ComputerFacade: Starting computer...");
        cpu.freeze();
        memory.load(0, hardDrive.read(0, 1024));
        cpu.jump(0);
        cpu.execute();
        System.out.println("ComputerFacade: Computer started successfully!");
    }
    
    public void shutdown() {
        System.out.println("ComputerFacade: Shutting down computer...");
        cpu.freeze();
        memory.clear();
        System.out.println("ComputerFacade: Computer shut down successfully!");
    }
    
    public void restart() {
        System.out.println("ComputerFacade: Restarting computer...");
        shutdown();
        try {
            Thread.sleep(1000); // Simulate restart delay
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        start();
    }
}
