package com.example.patterns.structural.facade;

/**
 * Facade Pattern - Subsystem class
 * CPU operations
 */
public class CPU {
    
    public void freeze() {
        System.out.println("CPU: Freezing processor");
    }
    
    public void jump(long position) {
        System.out.println("CPU: Jumping to position " + position);
    }
    
    public void execute() {
        System.out.println("CPU: Executing instructions");
    }
}
