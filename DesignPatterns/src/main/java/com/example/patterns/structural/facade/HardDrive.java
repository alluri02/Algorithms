package com.example.patterns.structural.facade;

/**
 * Facade Pattern - Subsystem class
 * Hard drive operations
 */
public class HardDrive {
    
    public byte[] read(long lba, int size) {
        System.out.println("HardDrive: Reading " + size + " bytes from sector " + lba);
        return new byte[size];
    }
    
    public void write(long lba, byte[] data) {
        System.out.println("HardDrive: Writing " + data.length + " bytes to sector " + lba);
    }
}
