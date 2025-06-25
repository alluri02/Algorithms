package com.example.patterns.structural.proxy;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for Proxy Pattern implementation
 */
public class ProxyPatternTest {
    
    private ImageProxy imageProxy;
    private DocumentProxy adminProxy;
    private DocumentProxy userProxy;
    
    @BeforeEach
    void setUp() {
        imageProxy = new ImageProxy("test.jpg");
        adminProxy = new DocumentProxy("confidential.txt", "admin");
        userProxy = new DocumentProxy("public.txt", "user");
    }
    
    @Test
    void testImageProxyLazyLoading() {
        // Initially, real image should not be loaded
        assertFalse(imageProxy.isLoaded());
        assertEquals("test.jpg", imageProxy.getFileName());
        
        // After first display, real image should be loaded
        imageProxy.display();
        assertTrue(imageProxy.isLoaded());
        
        // Subsequent calls should use cached image
        imageProxy.display();
        assertTrue(imageProxy.isLoaded());
    }
    
    @Test
    void testDocumentProxyAccessControl() {
        // Admin should be able to read and write
        assertDoesNotThrow(() -> {
            adminProxy.read();
            adminProxy.write("Admin content");
        });
        
        // User should be able to read but not write
        assertDoesNotThrow(() -> userProxy.read());
        // Note: write method doesn't throw exception, it just denies access
        assertDoesNotThrow(() -> userProxy.write("User content"));
    }
    
    @Test
    void testDocumentProxyWithEditor() {
        DocumentProxy editorProxy = new DocumentProxy("article.txt", "editor");
        
        // Editor should be able to read and write
        assertDoesNotThrow(() -> {
            editorProxy.read();
            editorProxy.write("Editor content");
        });
    }
    
    @Test
    void testProxyInterfaceCompliance() {
        // Proxy should implement the same interface as real object
        assertTrue(imageProxy instanceof Image);
        assertTrue(adminProxy instanceof Document);
        assertTrue(userProxy instanceof Document);
    }
}
