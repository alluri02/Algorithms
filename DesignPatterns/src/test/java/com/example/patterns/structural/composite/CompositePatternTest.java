package com.example.patterns.structural.composite;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for Composite Pattern implementation
 */
public class CompositePatternTest {
    
    private File file1;
    private File file2;
    private Directory directory;
    private Directory rootDirectory;
    
    @BeforeEach
    void setUp() {
        file1 = new File("document.txt", 1024);
        file2 = new File("image.jpg", 2048);
        directory = new Directory("Documents");
        rootDirectory = new Directory("Root");
    }
    
    @Test
    void testFileProperties() {
        assertEquals("document.txt", file1.getName());
        assertEquals(1024, file1.getSize());
        
        assertEquals("image.jpg", file2.getName());
        assertEquals(2048, file2.getSize());
    }
    
    @Test
    void testDirectoryOperations() {
        assertEquals("Documents", directory.getName());
        assertEquals(0, directory.getSize()); // Empty directory
        assertTrue(directory.getComponents().isEmpty());
        
        // Add files to directory
        directory.addComponent(file1);
        directory.addComponent(file2);
        
        assertEquals(2, directory.getComponents().size());
        assertEquals(3072, directory.getSize()); // 1024 + 2048
        
        // Remove a file
        directory.removeComponent(file1);
        assertEquals(1, directory.getComponents().size());
        assertEquals(2048, directory.getSize());
    }
    
    @Test
    void testNestedDirectories() {
        // Create nested structure
        directory.addComponent(file1);
        rootDirectory.addComponent(directory);
        rootDirectory.addComponent(file2);
        
        assertEquals(2, rootDirectory.getComponents().size());
        assertEquals(3072, rootDirectory.getSize()); // 1024 + 2048
        
        // Add another directory
        Directory subDir = new Directory("SubDir");
        File file3 = new File("video.mp4", 4096);
        subDir.addComponent(file3);
        rootDirectory.addComponent(subDir);
        
        assertEquals(3, rootDirectory.getComponents().size());
        assertEquals(7168, rootDirectory.getSize()); // 1024 + 2048 + 4096
    }
    
    @Test
    void testUniformInterface() {
        // Both File and Directory implement FileSystemComponent
        FileSystemComponent component1 = file1;
        FileSystemComponent component2 = directory;
        
        assertNotNull(component1.getName());
        assertNotNull(component2.getName());
        assertTrue(component1.getSize() >= 0);
        assertTrue(component2.getSize() >= 0);
    }
}
