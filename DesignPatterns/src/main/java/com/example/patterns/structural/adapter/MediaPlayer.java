package com.example.patterns.structural.adapter;

/**
 * MediaPlayer interface that our main class expects
 */
public interface MediaPlayer {
    void play(String audioType, String fileName);
}
